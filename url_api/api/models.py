from django.db import models

# Create your models here.

class Url(models.Model):
    full_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=63)