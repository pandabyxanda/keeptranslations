# Generated by Django 4.1.3 on 2022-12-01 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, verbose_name='words yahho')),
                ('translation', models.CharField(blank=True, max_length=255)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('starred', models.BooleanField(default=False)),
                ('learned', models.BooleanField(default=False)),
                ('learning_rating', models.IntegerField(default=10, blank=True)),
            ],
            options={
                'verbose_name': 'words__',
                'verbose_name_plural': 'words__',
                'ordering': ['-pk'],
            },
        ),
    ]
