# Generated by Django 3.0.8 on 2020-10-17 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('to', models.TextField(default='')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.TextField()),
                ('userAccount', models.TextField()),
                ('userPassword', models.TextField()),
                ('friends', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.TextField()),
                ('value', models.TextField()),
            ],
        ),
    ]
