from django.contrib import admin

from .models import Fileserver, PhysicalMountPoint, VirtualMountPoint, OrgFolder, PermissionFolder, Permission, User, \
    Role, RoleMembership

# Register your models here.
admin.site.register(Fileserver)
admin.site.register(PhysicalMountPoint)
admin.site.register(VirtualMountPoint)
admin.site.register(OrgFolder)
admin.site.register(PermissionFolder)
admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(RoleMembership)