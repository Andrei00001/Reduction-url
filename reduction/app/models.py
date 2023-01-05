from django.db import models

# Create your models here.


class URL(models.Model):
    url = models.CharField(max_length=512)
    reduction_url = models.CharField(max_length=512, unique=True)
