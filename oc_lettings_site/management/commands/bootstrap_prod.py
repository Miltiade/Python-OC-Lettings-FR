"""Bootstrap a fresh production database with demo data and ensure superuser access."""

import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    """Load demo data and create superuser if needed on a fresh database.

    This command is idempotent: if the database already contains data,
    it exits immediately without doing anything.

    On a fresh database:
      1. Loads the 'bootstrap_data' fixture (users, addresses, lettings, profiles)
      2. Overwrites the admin password from the DJANGO_SUPERUSER_PASSWORD
         environment variable (mandatory on Render, optional in CI tests).

    Logs are written to stdout/stderr so they appear in Render's logs.
    Never fails container startup — warnings are logged if required env vars are missing.
    """

    help = "Bootstrap a fresh production database with demo data."

    def handle(self, *args, **options):
        self.stdout.write("Checking if database is fresh...")

        # Detect freshness via the user table (lightweight query)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user;")
            user_count = cursor.fetchone()[0]

        if user_count > 0:
            self.stdout.write(
                self.style.SUCCESS("Existing data detected — bootstrap skipped.")
            )
            return

        self.stdout.write("Fresh database detected — loading fixtures...")
        call_command("loaddata", "bootstrap_data", verbosity=0)
        self.stdout.write(self.style.SUCCESS("Fixtures loaded."))

        # Override admin password from env var (Render requirement)
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        User = get_user_model()
        admin = User.objects.filter(username="admin").first()

        if password:
            if admin:
                admin.set_password(password)
                admin.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        "Admin password applied from DJANGO_SUPERUSER_PASSWORD."
                    )
                )
            else:
                self.stderr.write(
                    self.style.WARNING(
                        "DJANGO_SUPERUSER_PASSWORD provided but 'admin' user not found "
                        "(should exist after fixture load)."
                    )
                )
        else:
            # Fixture passwords are sanitized ("!"); warn loudly if we're running in prod.
            if os.environ.get("DATABASE_URL"):
                self.stderr.write(
                    self.style.WARNING(
                        "No DJANGO_SUPERUSER_PASSWORD set: admin login DISABLED on this deployment. "
                        "Please add this environment variable in Render dashboard to enable admin access."
                    )
                )
            else:
                # Running locally — no password override needed, fixture passwords remain unusable.
                self.stdout.write(
                    "Local environment — admin login disabled in test fixture."
                )

        self.stdout.write(self.style.SUCCESS("Bootstrap complete."))
        