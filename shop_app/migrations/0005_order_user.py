# Generated by Django 2.0.7 on 2018-07-30 20:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop_app', '0004_auto_20180725_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete='CASCADE', to=settings.AUTH_USER_MODEL),
        ),
    ]
