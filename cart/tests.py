from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Cart, CartItem
from products.models import Product, Category


class CartTests(APITestCase):

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

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

    def test_add_item_to_cart(self):
        # Test adding an item to the cart
        url = reverse('add-to-cart')
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_item_from_cart(self):
        # Add an item to the cart first
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Test removing the item from the cart
        url = reverse('remove-from-cart')
        data = {
            'product_id': self.product.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CartItem.objects.filter(cart=self.cart, product=self.product).exists())

    def test_get_cart(self):
        # Add an item to the cart first
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Test retrieving the cart
        url = reverse('get-cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product']['name'], 'Smartphone')
