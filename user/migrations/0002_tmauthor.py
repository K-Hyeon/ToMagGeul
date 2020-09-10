# Generated by Django 3.1.1 on 2020-09-09 12:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMAuthor',
            fields=[
                ('author_name', models.CharField(max_length=50, unique=True)),
                ('introduce', models.CharField(blank=True, max_length=500, null=True)),
                ('page_link', models.CharField(blank=True, max_length=300, null=True)),
                ('sns_link', models.CharField(blank=True, max_length=300, null=True)),
                ('portfolio', models.FileField(upload_to='portfolios')),
                ('opening_date', models.DateField(default=django.utils.timezone.now)),
                ('follower_num', models.PositiveIntegerField(default=0)),
                ('tomag_num', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.tmuser')),
            ],
        ),
    ]
