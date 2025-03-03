from django.test import TestCase
from .models import User, Order
from django.urls import reverse
from rest_framework import status

class UserOrderTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        Order.objects.create(user=self.user1, status='pending')
        Order.objects.create(user=self.user2, status='confirmed')
        Order.objects.create(user=self.user1, status='cancelled')
        Order.objects.create(user=self.user2, status='delivered')

    def test_user_order_endpoint_retrieves_only_authenticated_users(self):
        user = User.objects.get(username='testuser1',password='testpassword1')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == 200
        data = response.json()
        self.assertTrue(all([order['user'] == user.id for order in data]))

    def test_user_order_unauthenticated_users(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
