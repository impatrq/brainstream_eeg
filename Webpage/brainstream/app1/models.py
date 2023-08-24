from django.db import models

class ejemplo(models.Model):
    numero = models.IntegerField()

class Datos(models.Model):
    valores = models.JSONField(default=list)