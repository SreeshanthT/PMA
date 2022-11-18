from django.contrib import admin

from PMA_api.models import (
    Passwords,SharePassword
)


# Register your models here.
admin.site.register(Passwords)
admin.site.register(SharePassword)
