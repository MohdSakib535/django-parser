# Generated by Django 3.2.5 on 2023-02-09 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='staff_name',
            new_name='name',
        ),
    ]