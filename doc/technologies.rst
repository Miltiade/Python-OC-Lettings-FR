Technologies
============

Application
-----------

* Python 3.12
* Django 3.0
* SQLite (development database)

Frontend
--------

* Bootstrap-based template set (styles bundled in the repository)

Testing & quality
-----------------

* pytest + pytest-django + pytest-cov (test coverage: 99%)
* flake8 (zero errors)

Production stack
----------------

* gunicorn — WSGI HTTP server
* whitenoise — static file serving
* Sentry — error tracking and logging
* Docker — containerization (image: ``smith9567/oc-lettings``)
* GitHub Actions — CI/CD pipeline
* Render — hosting
* Sphinx — this documentation (published on Read the Docs)
