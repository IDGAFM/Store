# Generated by Django 4.2.2 on 2023-06-29 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginre', '0007_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
