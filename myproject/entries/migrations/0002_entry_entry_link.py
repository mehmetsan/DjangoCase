# Generated by Django 3.1.5 on 2021-01-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='entry_link',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
