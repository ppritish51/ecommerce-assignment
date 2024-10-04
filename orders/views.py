from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from .models import Order, OrderItem, DiscountCode
from .serializers import OrderSerializer, DiscountCodeSerializer


class CheckoutAPI(APIView):
    def post(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = sum([item.product.price * item.quantity for item in cart.items.all()])

        # Get discount code from request (optional)
        discount_code = request.data.get('discount_code')
        discount = None
        discount_value = Decimal(0)

        if discount_code:
            try:
                discount = DiscountCode.objects.get(code=discount_code, is_used=False)
                discount_value = total_price * (discount.discount_percentage / 100)
                total_price -= discount_value
            except DiscountCode.DoesNotExist:
                return Response({'error': 'Invalid or used discount code'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=user, total_price=total_price, discount_value=discount_value)

        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Mark discount code as used
        if discount:
            discount.is_used = True
            discount.save()

        # Clear the cart
        cart.items.all().delete()

        return Response({'message': 'Order placed successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)


class OrderHistoryAPI(APIView):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidateDiscountAPI(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            discount = DiscountCode.objects.get(code=code, is_used=False)
            serializer = DiscountCodeSerializer(discount)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DiscountCode.DoesNotExist:
            return Response({'error': 'Invalid or used discount code'}, status=status.HTTP_400_BAD_REQUEST)
