from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_landlord2(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('users', 'Profile')
    user, created = User.objects.get_or_create(username='landlord2')
    if created:
        user.password = make_password('123456')
        user.save()
    Profile.objects.get_or_create(user=user, defaults={'role': '房东'})


def unseed_landlord2(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='landlord2').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_seed_users'),
    ]

    operations = [
        migrations.RunPython(seed_landlord2, unseed_landlord2),
    ]
