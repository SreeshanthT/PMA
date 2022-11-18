from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from rest_framework.authtoken.models import Token
from django_lifecycle import (
    hook,BEFORE_SAVE
)

from PMA.utils import BaseContent

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Passwords(BaseContent):
    display_name = 'platform'
    platform = models.CharField(max_length=255)
    password = models.CharField("Password", max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['platform','password','user']
   
class SharePassword(BaseContent):
    shareby = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing_passwords',null=True)
    password = models.ForeignKey(Passwords,on_delete=models.CASCADE)
    shareto = models.ForeignKey(User,on_delete=models.CASCADE,related_name="incoming_password")
        
class Organizations(BaseContent):
    name = models.CharField("Organization",max_length=255)
    members = models.ManyToManyField(User,blank=True)
    password = models.CharField("Password", max_length=255)

    @hook(BEFORE_SAVE, when='password', has_changed=True)
    def set_password(self):
        self.password = make_password(self.password)
        
    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)


    