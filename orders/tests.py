from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Product, Category
from cart.models import Cart, CartItem
from .models import Order, DiscountCode

class OrderTests(APITestCase):
    NTH_ORDER = 2  # Should match the NTH_ORDER in the CheckoutAPI

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
            stock=50,  # Increased stock to handle multiple orders
            category=self.category
        )

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

    def test_checkout_without_discount(self):
        # Add items to cart
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Test placing an order when it's not the nth order
        url = reverse('checkout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(float(order.total_price), 1000.00)  # 2 items at $500 each
        self.assertEqual(float(order.discount_value), 0.00)  # No discount applied

        # Check if the cart was cleared
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout_with_automatic_discount(self):
        # First order (no discount)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.client.post(reverse('checkout'))

        # Second order (should get discount because we count +1)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # There should be two orders now
        self.assertEqual(Order.objects.count(), 2)
        order = Order.objects.last()
        self.assertEqual(float(order.total_price), 900.00)  # 10% discount applied on $1000
        self.assertEqual(float(order.discount_value), 100.00)  # Discount value is $100

    def test_order_history(self):
        # Place multiple orders
        for _ in range(3):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
            self.client.post(reverse('checkout'))

        # Test retrieving order history
        url = reverse('order-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the number of orders
        self.assertEqual(len(response.data), 3)

        # Verify discount application on every nth order
        for i, order_data in enumerate(response.data):
            expected_total = 900.00 if (i + 1) % self.NTH_ORDER == 0 else 1000.00
            expected_discount = 100.00 if (i + 1) % self.NTH_ORDER == 0 else 0.00
            self.assertEqual(float(order_data['total_price']), expected_total)
            self.assertEqual(float(order_data['discount_value']), expected_discount)

    def test_multiple_orders_discount_applied_correctly(self):
        # Place orders up to NTH_ORDER * 2 to check discounts at each nth order
        total_orders = self.NTH_ORDER * 2
        for i in range(total_orders):
            # Add items to cart
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
            response = self.client.post(reverse('checkout'))
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            order = Order.objects.last()
            if (i + 1) % self.NTH_ORDER == 0:
                # Discount should be applied
                self.assertEqual(float(order.total_price), 900.00)
                self.assertEqual(float(order.discount_value), 100.00)
            else:
                # No discount
                self.assertEqual(float(order.total_price), 1000.00)
                self.assertEqual(float(order.discount_value), 0.00)

    def test_order_items_recorded_correctly(self):
        # Add items to cart
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Place an order
        self.client.post(reverse('checkout'))

        # Check that OrderItems are recorded correctly
        order = Order.objects.first()
        order_items = order.items.all()
        self.assertEqual(order_items.count(), 1)
        order_item = order_items.first()
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(float(order_item.price), 500.00)
