from django.db import models


class Fileserver(models.Model):
    name = models.CharField(
        max_length=256
    )
    physicalprefix = models.CharField(
        max_length=30,
        help_text="A prefix on the fileserver, like D:\Shares")

    logicalprefix = models.CharField(
        max_length=30,
        help_text="A logical prefix the user sees, like O:"
    )

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(
        max_length=256
    )
    parent_folder = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE)
    fileserver = models.ForeignKey('Fileserver', null=True, blank=True, related_name='child', on_delete=models.CASCADE)

    def __str__(self):
        if self.fileserver is not None:
            # this is a root folder
            return  f"{self.fileserver.logicalprefix}\\{self.name}"
        if self.parent_folder is not None:
            return f"{self.parent_folder}\\{self.name}"
        return None
