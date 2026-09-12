from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'nomi', 'narxi', 'turi', 'status', 'created_at']

class FoodUpdatePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['narxi']

class FoodUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['status']