from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.CharField(max_length=80)),
                ('region', models.CharField(max_length=40)),
                ('layout', models.CharField(max_length=20)),
                ('area', models.IntegerField()),
                ('rent', models.IntegerField()),
                ('deposit', models.IntegerField()),
                ('payment', models.CharField(max_length=20)),
                ('facilities', models.JSONField(default=list)),
                ('description', models.TextField(default='')),
                ('photos', models.JSONField(default=list)),
                ('status', models.CharField(choices=[('待出租', '待出租'), ('已预约', '已预约'), ('已签约', '已签约'), ('已下架', '已下架')], default='待出租', max_length=20)),
                ('landlord_phone', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
