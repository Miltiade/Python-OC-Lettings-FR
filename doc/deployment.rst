Deployment
==========

Overview
--------

Production runs the Docker image published on Docker Hub
(``smith9567/oc-lettings``), hosted on Render. Deployment is fully
automated by GitHub Actions and triggered only by pushes to ``master``.

Pipeline (GitHub Actions)
-------------------------

1. **build-test** — every push, every branch: installs pinned
   dependencies, runs ``flake8``, runs ``pytest`` with coverage;
2. **dockerize** — only on ``master`` and only if tests pass: builds the
   image, tags it with the commit hash and ``latest``, pushes to
   Docker Hub;
3. **deploy** — only if dockerize succeeded: calls the Render deploy
   hook, which redeploys the service from the ``latest`` image.

Hosting (Render)
----------------

* Web service created from the existing image
  ``docker.io/smith9567/oc-lettings:latest`` (no Git connection —
  deployments are triggered exclusively by the CI hook);
* Region: Frankfurt; instance type: free;
* Environment variables: ``SECRET_KEY``, ``DEBUG=False``,
  ``ALLOWED_HOSTS=<service URL>``, ``SENTRY_DSN``.

Static files
------------

``whitenoise`` serves static files from the application (middleware in
``settings.py``); ``collectstatic`` runs at container startup, before
gunicorn binds to ``$PORT``. Admin styling therefore loads correctly
in production.

Run the image locally
---------------------

::

   docker pull smith9567/oc-lettings:latest
   docker run -d -p 8000:8000 --env-file .env -e DEBUG=False \
     -e ALLOWED_HOSTS=localhost,127.0.0.1 smith9567/oc-lettings:latest

Verification
------------

* Public URL: https://oc-lettings-spwm.onrender.com
* After a deploy, check: home page loads, lettings/profiles pages
  load, admin page is styled (static files) and accepts login.
  