# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core import serializers
from django.db import models

from .managers import FieldHistoryManager

OBJECT_ID_TYPE_SETTING = 'FIELD_HISTORY_OBJECT_ID_TYPE'


def instantiate_object_id_field(object_id_class_or_tuple=models.TextField):
    """
    Instantiates and returns a model field for FieldHistory.object_id.

    object_id_class_or_tuple may be either a Django model field class or a
    tuple of (model_field, kwargs), where kwargs is a dict passed to
    model_field's constructor.
    """
    if isinstance(object_id_class_or_tuple, (list, tuple)):
        object_id_class, object_id_kwargs = object_id_class_or_tuple
    else:
        object_id_class = object_id_class_or_tuple
        object_id_kwargs = {}

    if not issubclass(object_id_class, models.fields.Field):
        raise TypeError('settings.%s must be a Django model field or (field, kwargs) tuple' % OBJECT_ID_TYPE_SETTING)
    if not isinstance(object_id_kwargs, dict):
        raise TypeError('settings.%s kwargs must be a dict' % OBJECT_ID_TYPE_SETTING)

    return object_id_class(db_index=True, **object_id_kwargs)


class FieldHistory(models.Model):
    object_id = instantiate_object_id_field(getattr(settings, OBJECT_ID_TYPE_SETTING, models.TextField))
    content_type = models.ForeignKey('contenttypes.ContentType', db_index=True, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=500, db_index=True)  # Same as field
    object = GenericForeignKey()  # Same as parent
    field_name = models.CharField(max_length=500, db_index=True)  # Same as field
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    serialized_data = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)  # Same as created date
    user = models.CharField(max_length=50, null=True, blank=True)

    objects = FieldHistoryManager()

    class Meta:
        app_label = 'field_history'
        get_latest_by = 'date_created'

    def __str__(self):
        return u'{} field history for {}'.format(self.field_name, self.object)

    @property
    def field_value(self):
        instances = serializers.deserialize('json', self.serialized_data)
        instance = list(instances)[0].object
        return getattr(instance, self.field_name)
