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
        cart = Cart.objects.get(user=user)

        # Calculate total price from cart items
        total_price = sum([item.product.price * item.quantity for item in cart.items.all()])

        # Check if the user qualifies for a discount based on their order count
        order_count = Order.objects.filter(user=user).count() + 1  # Increment to include this current order
        discount_value = Decimal(0)

        if order_count % 2 == 0:  # Assuming nth order is every 2nd order
            # Apply 10% discount
            discount_value = total_price * Decimal(0.1)
            total_price -= discount_value

            # Generate a unique discount code by appending a timestamp or random value
            discount_code = f"DISCOUNT{order_count}_{user.id}"

            # Ensure the discount code is unique, else handle IntegrityError
            try:
                DiscountCode.objects.create(
                    code=discount_code,
                    discount_percentage=10.00,
                    is_used=True  # Mark it used since it's automatically applied
                )
            except IntegrityError:
                return Response({'error': 'Discount code creation failed due to uniqueness violation.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create the order
        order = Order.objects.create(user=user, total_price=total_price, discount_value=discount_value)

        # Add order items from the cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Include the price here
            )

        # Clear the cart after the order is placed
        cart.items.all().delete()

        # Return the response with order details
        return Response({
            'message': 'Order placed successfully',
            'order_id': order.id,
            'total_price': total_price,
            'discount_applied': discount_value
        }, status=status.HTTP_201_CREATED)


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
