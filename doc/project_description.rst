Project Description
===================

OC Lettings is a property rental website originally delivered as a
monolithic Django application. It lets visitors browse rental properties
(lettings) and user profiles.

The application was restructured into three focused Django apps,
following the single-responsibility principle:

* ``lettings`` — manages properties (``Letting``) and their physical
  addresses (``Address``);
* ``profiles`` — manages user profiles (``Profile``);
* ``oc_lettings_site`` — project-level settings, base templates and the
  home page.

Data originally stored in the monolithic app was migrated using Django
migrations (``RunPython`` only, no raw SQL), and the legacy tables were
dropped via migrations as well. The site's appearance and functionality
are unchanged.

The project ships with a demonstration dataset: 6 lettings, 6 addresses
and 4 profiles, stored in a SQLite database versioned with the
repository.
