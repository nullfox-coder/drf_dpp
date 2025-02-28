from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# status_choices = (
#     ("pending", "Pending"),
#     ("confirmed", "Confirmed"),
#     ("cancelled", "Cancelled"),
#     ("delivered", "Delivered")
# )

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products", null = True, blank = True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.name} - {self.price}"

class Order(models.Model):
    class choices(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        DELIVERED = "delivered", "Delivered"

    order_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=choices.choices, default=choices.PENDING)
    products = models.ManyToManyField(Product, through='OrderItem', related_name = 'orders')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price_total(self):
        return self.product.price * self.quantity
    