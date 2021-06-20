from django.db import models
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 200000:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


# Create your models here.
class Picture(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.name
