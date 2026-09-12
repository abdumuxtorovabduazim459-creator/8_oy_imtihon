from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import Food
from menu.serializers import FoodSerializer

class OrderItemInputSerializer(serializers.Serializer):
    ovqat_id = serializers.IntegerField()
    soni = serializers.IntegerField(min_value=1)

class OrderItemSerializer(serializers.ModelSerializer):
    ovqat = FoodSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'ovqat', 'soni', 'narxi']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'jami_summa', 'manzil', 'description', 'tel',
                  'long', 'lat', 'status', 'created_at', 'delivered_at', 'items']

class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    manzil = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    tel = serializers.CharField()
    long = serializers.CharField(required=False, allow_blank=True)
    lat = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Buyurtmada kamida bitta taom bo'lishi kerak")
        return items

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']