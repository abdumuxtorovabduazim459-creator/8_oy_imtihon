from django.utils import timezone
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin
from menu.models import Food
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, CreateOrderSerializer, OrderStatusUpdateSerializer
)

class CreateOrderView(generics.GenericAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            with transaction.atomic():
                jami_summa = 0
                order_items_data = []

                for item in data['items']:
                    try:
                        food = Food.objects.get(id=item['ovqat_id'])
                    except Food.DoesNotExist:
                        return Response(
                            {"error": f"Taom ID {item['ovqat_id']} topilmadi"},
                            status=status.HTTP_404_NOT_FOUND
                        )
                    if food.status == 'yoq':
                        return Response(
                            {"error": f"{food.nomi} hozircha mavjud emas"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    item_total = food.narxi * item['soni']
                    jami_summa += item_total
                    order_items_data.append({
                        'ovqat': food,
                        'soni': item['soni'],
                        'narxi': food.narxi
                    })

                order = Order.objects.create(
                    user=request.user,
                    jami_summa=jami_summa,
                    manzil=data['manzil'],
                    description=data.get('description', ''),
                    tel=data['tel'],
                    long=data.get('long', ''),
                    lat=data.get('lat', ''),
                    status=Order.Status.YARATILDI
                )

                for oi in order_items_data:
                    OrderItem.objects.create(buyurtma=order, **oi)

            return Response({
                "message": "Buyurtma qabul qilindi",
                "order_id": order.id,
                "jami_summa": jami_summa
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchi: O'z buyurtmalari tarixi
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__ovqat')

# Admin: Barcha buyurtmalar
class AllOrdersView(generics.ListAPIView):
    queryset = Order.objects.all().prefetch_related('items__ovqat').order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]

# Admin: Statusni o'zgartirish
class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == Order.Status.YETKAZILDI and not instance.delivered_at:
            instance.delivered_at = timezone.now()
            instance.save()