from django.db import models

# Create your models here.
from django.db import models


class RssiDataMore(models.Model):
    host = models.CharField(max_length=200)
    data = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.host


class RssiDataLess(models.Model):
    host = models.CharField(max_length=200)
    data = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.host


