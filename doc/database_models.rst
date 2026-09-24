Database & Model Structure
==========================

The application uses Django's ORM on a SQLite database
(``oc-lettings-site.sqlite3``, versioned with the repository and shipped
with demo data: 6 addresses, 6 lettings, 4 profiles).

Models
------

``lettings.Address``
    Physical address of a property. Fields: ``number`` (positive int,
    max 9999), ``street``, ``city``, ``state`` (2 chars),
    ``zip_code`` (positive int, max 99999), ``country_iso_code``
    (3 chars). ``__str__`` returns ``"<number> <street>"``.

``lettings.Letting``
    A rental property. Fields: ``title`` (max 256 chars),
    ``address`` (OneToOne to ``Address``, cascade delete).
    ``__str__`` returns the title.

``profiles.Profile``
    User profile. Fields: ``user`` (OneToOne to ``auth.User``,
    cascade delete), ``favorite_city`` (CharField, optional).
    ``__str__`` returns the username.

Tables
------

Each model maps to a table created by Django migrations:

* ``lettings_address``, ``lettings_letting`` — owned by the
  ``lettings`` app;
* ``profiles_profile`` — owned by the ``profiles`` app.

Historical note
---------------

The data was originally stored in the monolithic ``oc_lettings_site``
app. During the restructuring, it was copied to the new apps with
Django data migrations (``RunPython``, no raw SQL) and the legacy
tables were dropped via migrations, with row counts verified at every
step (6/6/4 preserved).
