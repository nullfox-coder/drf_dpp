from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    )
from rest_framework.response import Response
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(price__gte=5)
    serializer_class = ProductSerializers

class ProductDetailed(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    lookup_url_kwarg = 'pk' # default is 'pk'

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
    
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'description', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        # if self.request.method == 'POST':
        #     self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ProductInfo(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializers(
            {
                'product': products,
                'count': len(products),
                'max_price': products.aggregate(max_price=Max('price'))['max_price']
            }
        )
        return Response(serializer.data)


class OrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializers

class UserOrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        obj = super().queryset.filter(user=user)
        return obj
    

