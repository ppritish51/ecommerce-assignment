from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product, Category


class ProductTests(APITestCase):

    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='pritish', password='12345678')
        self.client.login(username='pritish', password='12345678')

        # Create a category and product for testing
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone with advanced features",
            price=500.00,
            stock=10,
            category=self.category
        )

    def test_list_products(self):
        # Test the product list API
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        # Test the product detail API
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Smartphone')
