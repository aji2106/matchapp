# Generated by Django 2.1.3 on 2018-12-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='numbers',
        ),
        migrations.AddField(
            model_name='member',
            name='friends',
            field=models.ManyToManyField(related_name='_member_friends_+', to='matchapp.Member'),
        ),
    ]