import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django_runprod.gunicorn import run_gunicorn

class Command(BaseCommand):
    help = 'Runs the Django application using Gunicorn for production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--address',
            default='0.0.0.0:8000',
            help='The address and port to bind to (default: 0.0.0.0:8000)'
        )
        parser.add_argument(
            '--sentry',
            action='store_true',
            help='Enable Sentry integration'
        )
        parser.add_argument(
            '--sentry-env',
            default='production',
            help='Sentry environment (default: production)'
        )
        parser.add_argument(
            '--serve-static',
            action='store_true',
            help='Serve static files using WhiteNoise'
        )
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Enable auto-reload on code changes'
        )

    def handle(self, *args, **options):
        try:
            address = options['address']
            use_sentry = options['sentry']
            sentry_env = options['sentry_env']
            serve_static = options['serve_static']
            reload_ = options['reload']

            self.stdout.write(
                self.style.SUCCESS(f'Starting Gunicorn server on {address}')
            )
            
            if use_sentry:
                self.stdout.write(
                    self.style.SUCCESS(f'Sentry enabled with environment: {sentry_env}')
                )
            
            if serve_static:
                self.stdout.write(
                    self.style.SUCCESS('Static file serving enabled with WhiteNoise')
                )
            
            if reload_:
                self.stdout.write(
                    self.style.WARNING('Auto-reload enabled (not recommended for production)')
                )

            run_gunicorn(
                address=address,
                use_sentry=use_sentry,
                sentry_env=sentry_env,
                serve_static=serve_static,
                reload_=reload_
            )
        except Exception as e:
            raise CommandError(f'Error starting Gunicorn server: {str(e)}')
