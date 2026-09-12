from django.db import models
from django.conf import settings
from menu.models import Food

class Order(models.Model):
    class Status(models.TextChoices):
        YARATILDI = 'YARATILDI', 'Yaratildi'
        TAYYORLANMOQDA = 'TAYYORLANMOQDA', 'Tayyorlanmoqda'
        YETKAZILMOQDA = 'YETKAZILMOQDA', 'Yetkazilmoqda'
        YETKAZILDI = 'YETKAZILDI', 'Yetkazildi'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    jami_summa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    manzil = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=20)
    long = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.YARATILDI)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    buyurtma = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ovqat = models.ForeignKey(Food, on_delete=models.PROTECT)
    soni = models.PositiveIntegerField()
    narxi = models.DecimalField(max_digits=10, decimal_places=2)  # Buyurtma paytidagi narx

    def __str__(self):
        return f"{self.ovqat.nomi} x {self.soni}"