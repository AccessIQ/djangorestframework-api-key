# Generated by Django 2.2.1 on 2019-06-09 13:21

from django.db import migrations, models

def split_prefix_hash(apps, schema_editor):
    APIKey = apps.get_model('rest_framework_api_key', 'APIKey')

    for api_key in APIKey.objects.all():
        prefix, _, hashed_key = api_key.id.partition('.')
        api_key.prefix = prefix
        api_key.hashed_key = hashed_key
        api_key.save()


def merge_prefix_hash(apps, schema_editor):
    APIKey = apps.get_model('rest_framework_api_key', 'APIKey')

    for api_key in APIKey.objects.all():
        api_key.pk = "{}.{}".format(api_key.prefix, api_key.hashed_key)
        api_key.save()


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_api_key', '0002_auto_20190529_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='hashed_key',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='prefix',
            field=models.CharField(max_length=8, null=True, unique=True),
        ),
        migrations.RunPython(split_prefix_hash, merge_prefix_hash),
        migrations.AlterField(
            model_name='apikey',
            name='hashed_key',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='prefix',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
