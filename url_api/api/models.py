from django.db import models

# This is apparently Google Chrome's maximum URL length. Do we need more? (The answer is, we might, but DO WE?)
url_max_len = 2048

class Url(models.Model):
    full_url = models.CharField(max_length=url_max_len, unique=True)
    short_url = models.CharField(max_length=63, unique=True)