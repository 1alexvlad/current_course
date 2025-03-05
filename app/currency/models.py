from django.db import models

class CurrencyModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
