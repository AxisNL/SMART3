from django.db import models


class Fileserver(models.Model):
    name = models.CharField(
        max_length=256
    )

    def __str__(self):
        return self.name


class PhysicalMountPoint(models.Model):
    """
        This is the physical path on a file server that hosts a fileshare
        """
    physicalprefix = models.CharField(
        max_length=30,
        help_text="A prefix on the fileserver, like D:\Shares")
    fileserver = models.ForeignKey('Fileserver', null=True, blank=True, related_name='child', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.physicalprefix} on {self.fileserver}"


class VirtualMountPoint(models.Model):
    logicalprefix = models.CharField(
        max_length=30,
        help_text="A logical prefix the user sees, like O:"
    )

    def __str__(self):
        return f"{self.logicalprefix}"


class OrgFolder(models.Model):
    name = models.CharField(
        max_length=256
    )
    physical_mountpoint = models.ForeignKey('PhysicalMountPoint',
                                            null=True,
                                            blank=True,
                                            on_delete=models.CASCADE)
    virtual_mountpoint = models.ForeignKey('VirtualMountPoint',
                                           null=True,
                                           blank=True,
                                           on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self',
                                      null=True,
                                      blank=True,
                                      related_name='child',
                                      on_delete=models.CASCADE)

    def __str__(self):
        if self.virtual_mountpoint is not None:
            # this is a root folder
            return f"{self.virtual_mountpoint.logicalprefix}\\{self.name}"
        if self.parent_folder is not None:
            return f"{self.parent_folder}\\{self.name}"
        return None


class PermissionFolder(models.Model):
    name = models.CharField(max_length=256)

    parent_folder = models.ForeignKey('OrgFolder',
                                      null=True,
                                      blank=True,
                                      on_delete=models.CASCADE)
    owner = models.ForeignKey('User',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.parent_folder}\\{self.name}"


class Permission(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    folder = models.ForeignKey('PermissionFolder', on_delete=models.CASCADE)

    READONLY = "R"
    READWRITE = "W"

    PERMISSION_CHOICES = {
        READONLY: "ReadOnly",
        READWRITE: "ReadWrite"
    }
    permission = models.CharField(
        max_length=1,
        choices=PERMISSION_CHOICES,
        default=READWRITE,
    )

    def __str__(self):
        return f"{self.folder}\\{self.role}"


class User(models.Model):
    name = models.CharField(max_length=256)
    sid = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class RoleMembership(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} role {self.role}"
