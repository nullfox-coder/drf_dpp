from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("user/", UserListCreate.as_view()),
    path("products/", ProductListCreate.as_view()),
    # path("product/create/", ProductCreate.as_view()),
    path("product/info/", ProductInfo.as_view()),
    path("product/<int:pk>", ProductDetailed.as_view()),
    # path("order/", OrderList.as_view()),
    # path("user-orders/", UserOrderList.as_view(), name="user-orders"),
]

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)

urlpatterns+=router.urls