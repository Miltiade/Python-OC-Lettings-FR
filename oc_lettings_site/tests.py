"""Tests for the core project app (homepage)."""


import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


def test_dummy():
    """Placeholder test asserting a trivial invariant."""
    assert 1


class BootstrapProdCommandTests(TestCase):
    """Tests for the bootstrap_prod management command."""

    def test_bootstrap_loads_fixture_on_fresh_db(self):
        """On a fresh database, the command loads the demo fixture."""
        User = get_user_model()
        self.assertEqual(User.objects.count(), 0)

        out = StringIO()
        call_command("bootstrap_prod", stdout=out)

        self.assertEqual(User.objects.count(), 5)
        self.assertIn("Fixtures loaded", out.getvalue())

    def test_bootstrap_skips_existing_db(self):
        """On a populated database, the command does nothing."""
        User = get_user_model()
        User.objects.create_user(username="someone", password="x")

        out = StringIO()
        call_command("bootstrap_prod", stdout=out)

        self.assertIn("bootstrap skipped", out.getvalue())
        self.assertEqual(User.objects.count(), 1)

    def test_bootstrap_sets_admin_password_from_env(self):
        """DJANGO_SUPERUSER_PASSWORD overrides the sanitized admin password."""
        User = get_user_model()
        with patch.dict(os.environ, {"DJANGO_SUPERUSER_PASSWORD": "s3cret-pw-48h"}):
            out = StringIO()
            call_command("bootstrap_prod", stdout=out)

        admin = User.objects.get(username="admin")
        self.assertTrue(admin.check_password("s3cret-pw-48h"))
