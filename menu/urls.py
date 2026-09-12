from django.urls import path
from .views import (
    FoodListView, FoodCreateView, FoodDeleteView,
    FoodUpdatePriceView, FoodUpdateStatusView
)

urlpatterns = [
    path('', FoodListView.as_view(), name='food-list'),
    path('create/', FoodCreateView.as_view(), name='food-create'),
    path('<int:pk>/delete/', FoodDeleteView.as_view(), name='food-delete'),
    path('<int:pk>/price/', FoodUpdatePriceView.as_view(), name='food-price'),
    path('<int:pk>/status/', FoodUpdateStatusView.as_view(), name='food-status'),
]