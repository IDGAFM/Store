# Generated by Django 4.2.2 on 2023-06-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainprog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='storage',
            field=models.IntegerField(default=64, verbose_name='Память'),
        ),
    ]
