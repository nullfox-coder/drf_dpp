from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
            "description",
        )
    
    def validate_price(self,value):
        if(value<0):
            raise serializers.ValidationError("Price cannot be negative")
        return value
    

class OrderItemSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.name', read_only = True)
    product_price = serializers.DecimalField(source = 'product.price', read_only = True, max_digits=10, decimal_places=2)
    class Meta:
        model = OrderItem
        fields = (
            'product',
            # 'quantity,'
            # 'price_total',
            'product_name',
            'product_price'
        )


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(read_only = True, many = True)
    total_price = serializers.SerializerMethodField(method_name = 'total')

    def total(self, obj):
        return sum([item.price_total for item in obj.items.all()])
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
            'total_price'
        )

class ProductInfoSerializers(serializers.Serializer):
    products = ProductSerializers(many = True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
