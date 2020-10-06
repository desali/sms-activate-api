from django.db import models


class Number(models.Model):
    number = models.CharField(max_length=500, unique=True)
    operation_id = models.IntegerField()
