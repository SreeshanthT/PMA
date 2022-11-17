from django.apps import apps as django_apps
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models
from django.shortcuts import get_object_or_404

from django_lifecycle import LifecycleModelMixin

import json


class CustomQuerySet(models.QuerySet):
    def only_active(self, **kwargs):
        return self.filter(active=True, **kwargs)

class BaseContent(LifecycleModelMixin, models.Model):
    display_name = 'name'

    active = models.BooleanField('Status', default=True, choices=(
        (False, 'Inactive'),
        (True, 'Active')
    ))
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    display_order = models.PositiveIntegerField(default=0)
    objects = CustomQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(getattr(self, self.display_name, '') or self.id)

    def get_model_name(self):
        return self.content_type().model

    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_values(self, *args, **kwargs):
        try:
            return self.content_type().model_class().objects.filter(id=self.id).values(*args)[0]
        except Exception as e:
            print(e)
            return {}

    def as_dict(self):
        return json.loads(
            serializers.serialize("json", self.__class__.objects.filter(pk=self.id))
        )[0]['fields']

    def as_json(self):
        return self.get_values(fields=self.__class__._meta.get_fields(), json=True)

    def class_name(self):
        return self.__class__.__name__

    def permission_roles(self):
        try:
            PermissionRoles = django_apps.get_model('django_roles_permissions', 'PermissionRoles')
            return PermissionRoles.objects.get(content_type=self.content_type(), object_id=self.id)
        except:
            return None
        
def get_object_or_None(qs,**kwargs):
    try:
        return get_object_or_404(qs,**kwargs)
    except:
        return None