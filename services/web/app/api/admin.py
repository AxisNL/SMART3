from django.contrib import admin
from .models import Fileserver, Folder

# Register your models here.
admin.site.register(Fileserver)
admin.site.register(Folder)