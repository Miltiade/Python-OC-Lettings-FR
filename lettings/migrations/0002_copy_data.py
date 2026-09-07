"""Data migration: copy Address and Letting rows from oc_lettings_site to lettings."""
from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """Copy all Address and Letting rows from the old app to the new one.

    Uses apps.get_model() to fetch HISTORICAL model classes (the ones as
    they existed at this point in migration history), never direct imports.
    Primary keys (id) are preserved so foreign keys keep pointing correctly.
    """
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')

    for old in OldAddress.objects.all():
        NewAddress.objects.create(
            id=old.id,
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        )

    for old in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old.id,
            title=old.title,
            address_id=old.address_id,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, migrations.RunPython.noop),
    ]