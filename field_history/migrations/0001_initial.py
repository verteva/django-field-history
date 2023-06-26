# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 17:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from field_history.models import OBJECT_ID_TYPE_SETTING, instantiate_object_id_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', instantiate_object_id_field(getattr(settings, OBJECT_ID_TYPE_SETTING, models.TextField))),
                ('field_name', models.CharField(max_length=500)),
                ('table_name', models.CharField(max_length=500)),
                ('old_value', models.TextField(blank=True, null=True)),
                ('new_value', models.TextField(blank=True, null=True)),
                ('serialized_data', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
        ),
    ]
