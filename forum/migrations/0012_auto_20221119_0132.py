# Generated by Django 2.2.28 on 2022-11-19 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('author', 'post_id')},
        ),
    ]
