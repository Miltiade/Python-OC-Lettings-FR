"""Data migration: copy Profile rows from oc_lettings_site to profiles."""
from django.db import migrations

def copy_profiles_data(apps, schema_editor):
    """Copy all Profile rows from the old app to the new one.

    Uses apps.get_model() for historical model classes; preserves
    primary keys so the OneToOne relation to User stays valid.
    """
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for old in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old.id,
            user_id=old.user_id,
            favorite_city=old.favorite_city,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, migrations.RunPython.noop),
    ]
