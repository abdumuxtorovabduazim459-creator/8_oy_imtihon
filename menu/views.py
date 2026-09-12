from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin
from .models import Food
from .serializers import (
    FoodSerializer, FoodUpdatePriceSerializer, FoodUpdateStatusSerializer
)
from .filters import FoodFilter

# Foydalanuvchi: Barcha taomlar (filter + pagination)
class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all().order_by('-id')
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = FoodFilter

# Admin: Taom qo'shish
class FoodCreateView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdmin]

# Admin: Taomni o'chirish
class FoodDeleteView(generics.DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdmin]

# Admin: Narxni o'zgartirish
class FoodUpdatePriceView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodUpdatePriceSerializer
    permission_classes = [IsAdmin]

# Admin: Statusni o'zgartirish
class FoodUpdateStatusView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodUpdateStatusSerializer
    permission_classes = [IsAdmin]