import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

# 存量房源归属映射：按小区名挂到明确房东名下，未列出的默认归 landlord1。
LANDLORD_BY_COMMUNITY = {
    '海棠公寓': 'landlord1',
    '江畔花园': 'landlord1',
    '梧桐里': 'landlord2',
    '文汇里': 'landlord2',
}
DEFAULT_LANDLORD = 'landlord1'


def assign_landlords(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Property = apps.get_model('properties', 'Property')
    users = {u.username: u for u in User.objects.filter(username__in={'landlord1', 'landlord2'})}
    default = users[DEFAULT_LANDLORD]
    for prop in Property.objects.filter(landlord__isnull=True):
        owner = users.get(LANDLORD_BY_COMMUNITY.get(prop.community, DEFAULT_LANDLORD), default)
        prop.landlord = owner
        prop.save(update_fields=['landlord'])


class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0002_seed_properties'),
        ('users', '0003_seed_landlord2'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='landlord',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='properties',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_landlords, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='property',
            name='landlord',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='properties',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
