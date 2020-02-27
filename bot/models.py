from django.db import models

class Rates(models.Model):
    name = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=10, decimal_places=2)
