# Generated by Django 3.1.2 on 2020-10-27 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorialapp', '0003_auto_20201027_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]