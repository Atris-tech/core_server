# Generated by Django 3.0.1 on 2019-12-24 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0002_auto_20191224_2146'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='transcribe',
            table='transcribe_text',
        ),
    ]