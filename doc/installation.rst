Installation
============

Prerequisites
-------------

* Python 3.12
* Git
* A virtual environment tool (``venv``, included in Python)

Steps
-----

1. Clone the repository::

       git clone https://github.com/Miltiade/Python-OC-Lettings-FR.git
       cd Python-OC-Lettings-FR

2. Create and activate a virtual environment::

       python -m venv venv
       source venv/bin/activate

3. Install dependencies (all versions are pinned)::

       pip install -r requirements.txt

4. Apply migrations::

       python manage.py migrate

   Note: the repository includes a SQLite database (``oc-lettings-site.sqlite3``)
   pre-populated with demo data. Migrations simply bring it up to date.

5. (Optional) Create a superuser for the admin interface::

       python manage.py createsuperuser

Environment variables
---------------------

The application reads the following environment variables:

* ``SECRET_KEY`` — Django secret key (required in production);
* ``DEBUG`` — ``True``/``False``, defaults to development behaviour;
* ``ALLOWED_HOSTS`` — comma-separated list of allowed hosts;
* ``SENTRY_DSN`` — Sentry Data Source Name (optional, enables error tracking).
