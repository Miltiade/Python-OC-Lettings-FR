Quickstart
==========

Run the development server
--------------------------

::

   source venv/bin/activate
   python manage.py runserver

Then browse:

* Home page: http://localhost:8000/
* Lettings list: http://localhost:8000/lettings/
* Profiles list: http://localhost:8000/profiles/
* Admin interface: http://localhost:8000/admin/

Browse the demo data
--------------------

* Click a letting from the list to view its detail page;
* Click a profile from the list to view a user's profile;
* Log into the admin with a superuser account to view and edit
  lettings, addresses and profiles (model names appear under each app).

Quality gates
-------------

From the repository root::

   flake8
   pytest --cov
