Programming Interfaces
======================

URL routes
----------

Each app exposes its own URL namespace, wired into the project
``ROOT_URLCONF``:

* ``/`` → ``oc_lettings_site.views.index`` (name: ``index``)
* ``/lettings/`` → ``lettings.views.index`` (name: ``lettings:index``)
* ``/lettings/<int:letting_id>/`` → ``lettings.views.letting`` (name: ``lettings:letting``)
* ``/profiles/`` → ``profiles.views.index`` (name: ``profiles:index``)
* ``/profiles/<str:username>/`` → ``profiles.views.profile`` (name: ``profiles:profile``)
* ``/admin/`` → Django admin


Views
-----

All views render a template and return an HTTP 200 response. Unknown
records return a custom 404 page. Unhandled exceptions return a custom
500 page and are reported to Sentry (when ``SENTRY_DSN`` is set).

Templates
---------

``oc_lettings_site`` owns ``templates/base.html`` and the home page
template. Each app keeps its page templates in its own
``templates/<app>/`` directory (``index.html``, ``letting.html``,
``profile.html``).

Error tracking
--------------

The ``sentry-sdk`` is initialized in ``settings.py`` from the
``SENTRY_DSN`` environment variable; Python logging is configured to
send records to Sentry alongside the console handler.
