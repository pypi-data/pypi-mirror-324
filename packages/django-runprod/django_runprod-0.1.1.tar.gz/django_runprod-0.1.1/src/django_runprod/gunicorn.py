import os

def run_gunicorn(address, use_sentry, sentry_env, serve_static=False, reload_=False):
    import sentry_sdk
    import multiprocessing
    from django.conf import settings
    from django.core.wsgi import get_wsgi_application
    from whitenoise import WhiteNoise
    from gunicorn.app.base import BaseApplication
    from sentry_sdk.integrations.django import DjangoIntegration

    application = get_wsgi_application()

    # Sentry integration
    if use_sentry:
        sentry_sdk.init(
            environment=sentry_env,
            dsn=settings.SENTRY_DSN,
            integrations=[DjangoIntegration()],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0,
            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True,
        )

    class GunicornApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        "bind": address,
        "workers": (multiprocessing.cpu_count() * 2) + 1,
        "accesslog": "-",
        "reload": reload_,
    }

    if serve_static:
        static_dir = os.path.join(settings.BASE_DIR, settings.STATIC_ROOT)
        application = WhiteNoise(application, root=static_dir)
        application.add_files(static_dir, prefix=settings.STATIC_URL)

    ret = GunicornApplication(application, options).run()
    return ret
