# Generated by Django 4.2.2 on 2023-06-30 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginre', '0010_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
