# Generated by Django 2.2.3 on 2019-07-30 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190730_0034'),
        ('profiles', '0002_profile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(related_name='favorited_by', to='events.Event'),
        ),
    ]
