from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("product/", ProductList.as_view()),
    path("product/<int:pk>", ProductDetailed.as_view()),
    path("order/", OrderList.as_view())
]