Usage Guide
===========

Browse lettings
---------------

1. From the home page, click **Lettings**;
2. Browse the list of properties;
3. Click a letting to view its detail page (title, address).

Browse profiles
---------------

1. From the home page, click **Profiles**;
2. Browse the list of users;
3. Click a username to view the profile (favorite city).

Manage data (admin)
-------------------

1. Go to ``/admin/`` and log in with a superuser account;
2. Under **Lettings**, add/edit/delete addresses and lettings;
3. Under **Profiles**, add/edit/delete user profiles.

Trigger a deployment
--------------------

Pushing to ``master`` runs the full CI/CD chain: lint + tests +
coverage, Docker image build & push (tagged with the commit hash),
then a production deployment via the Render deploy hook. Only pushes
to ``master`` trigger containerization and deployment; pushes to other
branches run tests only.

Use cases
---------

* **Visitor** — browses lettings and profiles without an account;
* **CTO / administrator** — manages lettings, addresses and profiles
  through the Django admin (frequent user of the admin interface);
* **Developer** — verifies changes with ``flake8`` and ``pytest``
  before pushing, and relies on the CI pipeline for delivery.
