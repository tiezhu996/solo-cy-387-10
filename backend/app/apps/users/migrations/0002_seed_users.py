from django.contrib.auth.hashers import make_password
from django.db import migrations

DEMO_USERS = [
    ('landlord1', '房东'),
    ('tenant1', '租客'),
    ('tenant2', '租客'),
    ('worker1', '物业人员'),
]
DEMO_PASSWORD = '123456'


def seed_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('users', 'Profile')
    for username, role in DEMO_USERS:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.password = make_password(DEMO_PASSWORD)
            user.save()
        Profile.objects.get_or_create(user=user, defaults={'role': role})


def unseed_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=[name for name, _ in DEMO_USERS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_users, unseed_users),
    ]
