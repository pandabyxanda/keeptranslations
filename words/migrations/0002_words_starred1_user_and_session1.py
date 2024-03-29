# Generated by Django 4.1.3 on 2023-01-23 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sessions', '0001_initial'),
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='starred1',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='User_And_Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='sessions.session')),
                ('user', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
