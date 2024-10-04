from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Product, Category
from cart.models import Cart, CartItem
from .models import Order, DiscountCode


class OrderTests(APITestCase):

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

        # Create a cart for the user and add an item
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Create a valid discount code for testing
        self.discount_code = DiscountCode.objects.create(code="DISCOUNT10", discount_percentage=10.00)

    def test_checkout_without_discount(self):
        # Test placing an order without a discount
        url = reverse('checkout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_price, 1000.00)  # 2 items at $500 each

        # Check if the cart was cleared
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout_with_valid_discount(self):
        # Test placing an order with a valid discount
        url = reverse('checkout')
        response = self.client.post(url, {'discount_code': 'DISCOUNT10'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the order was created with the correct discount applied
        order = Order.objects.first()
        self.assertEqual(order.total_price, 900.00)  # 10% off from $1000.00
        self.assertEqual(order.discount_value, 100.00)

        # Check if the discount code was marked as used
        discount = DiscountCode.objects.get(code="DISCOUNT10")
        self.assertTrue(discount.is_used)

    def test_checkout_with_invalid_discount(self):
        # Test placing an order with an invalid discount code
        url = reverse('checkout')
        response = self.client.post(url, {'discount_code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid or used discount code')

    def test_discount_code_already_used(self):
        # Use the discount code once
        self.client.post(reverse('checkout'), {'discount_code': 'DISCOUNT10'})

        # Try to use the same discount code again
        url = reverse('checkout')
        response = self.client.post(url, {'discount_code': 'DISCOUNT10'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid or used discount code')

    def test_order_history(self):
        # Place an order
        self.client.post(reverse('checkout'))

        # Test retrieving order history
        url = reverse('order-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the order details
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total_price'], '1000.00')
        self.assertEqual(len(response.data[0]['items']), 1)
        self.assertEqual(response.data[0]['items'][0]['product'], 'Smartphone')

    def test_validate_discount_code(self):
        # Test validating a valid discount code
        url = reverse('validate-discount')
        response = self.client.post(url, {'code': 'DISCOUNT10'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'DISCOUNT10')
        self.assertEqual(response.data['discount_percentage'], '10.00')

    def test_validate_invalid_discount_code(self):
        # Test validating an invalid discount code
        url = reverse('validate-discount')
        response = self.client.post(url, {'code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid or used discount code')
