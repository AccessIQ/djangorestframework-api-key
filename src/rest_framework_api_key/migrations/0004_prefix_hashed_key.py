# Generated by Django 2.2.2 on 2019-06-29 10:38

from django.db import migrations, models

APP_NAME = "rest_framework_api_key"
MODEL_NAME = "apikey"
DEPENDENCIES = [(APP_NAME, "0003_auto_20190623_1952")]


class Migration(migrations.Migration):

    dependencies = DEPENDENCIES
    # Blank operations to get custom verson of package on the same footing
    # as the latest version. We want to ensure that when we update to the
    # latest version, we already have the expected migrations applied and only
    # newer migrations will be added.
    operations = []
