from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics

class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(price__gte=5)
    serializer_class = ProductSerializers

class ProductDetailed(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    lookup_url_kwarg = 'pk' # default is 'pk'

class OrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializers

