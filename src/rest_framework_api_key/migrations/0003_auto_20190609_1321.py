# Generated by Django 2.2.2 on 2019-06-23 19:52

from django.db import migrations, models


APP_NAME = "rest_framework_api_key"
MODEL_NAME = "apikey"
DEPENDENCIES = [(APP_NAME, "0002_auto_20190529_2243")]


def populate_prefix_hashed_key(apps, schema_editor) -> None:  # type: ignore
    model = apps.get_model(APP_NAME, MODEL_NAME)

    for api_key in model.objects.using(schema_editor.connection.alias).all():
        prefix, _, hashed_key = api_key.id.partition(".")
        api_key.prefix = prefix
        api_key.hashed_key = hashed_key
        api_key.save()

class Migration(migrations.Migration):

    dependencies = DEPENDENCIES

    operations = [
        migrations.AddField(
            model_name=MODEL_NAME,
            name='hashed_key',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name=MODEL_NAME,
            name='prefix',
            field=models.CharField(max_length=8, null=True, unique=True),
        ),
        migrations.RunPython(populate_prefix_hashed_key, migrations.RunPython.noop, elidable=True),
        migrations.AlterField(
            model_name=MODEL_NAME,
            name='hashed_key',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name=MODEL_NAME,
            name='id',
        ),
        migrations.AddField(
            model_name=MODEL_NAME,
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name=MODEL_NAME,
            name='prefix',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
