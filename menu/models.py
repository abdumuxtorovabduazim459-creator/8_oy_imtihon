from django.db import models

class Food(models.Model):
    class Turi(models.TextChoices):
        ICHIMLIK = 'ichimlik', 'Ichimlik'
        OVQAT = 'ovqat', 'Ovqat'
        DESSERT = 'dessert', 'Dessert'
        SNACK = 'snack', 'Snack'

    class Status(models.TextChoices):
        MAVJUD = 'mavjud', 'Mavjud'
        YOQ = 'yoq', "Yo'q"

    nomi = models.CharField(max_length=255)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    turi = models.CharField(max_length=20, choices=Turi.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.MAVJUD)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomi