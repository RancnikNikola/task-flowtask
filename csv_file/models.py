from django.db import models


# Create your models here.
class CsvFile(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.BooleanField(default=False)
