from django.db import models


class Update(models.Model):
    vcode = models.CharField(max_length=20)
    fname = models.CharField(max_length=20)
    flink = models.TextField()
