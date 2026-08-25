from django.db import transaction
from rest_framework import status, viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Address
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, CheckoutSerializer


class CartViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request):
        """GET /api/cart/"""
        serializer = self.get_serializer(self.get_cart())
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='items')
    def add_item(self, request):
        """POST /api/cart/items/  {product_id, quantity}"""
        cart = self.get_cart()
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'quantity': quantity}
        )
        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock:
                return Response(
                    {'quantity': f'Only {product.stock} left in stock.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.quantity = new_qty
            item.save()

        return Response(
            CartSerializer(cart).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['patch', 'delete'], url_path='items/(?P<item_id>[^/.]+)')
    def modify_item(self, request, item_id=None):
        """PATCH or DELETE /api/cart/items/<id>/"""
        cart = self.get_cart()
        try:
            item = cart.items.get(pk=item_id)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            item.delete()
            return Response(CartSerializer(cart).data)

        quantity = request.data.get('quantity')
        if quantity is None or int(quantity) < 1:
            return Response(
                {'quantity': 'Must be at least 1.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if int(quantity) > item.product.stock:
            return Response(
                {'quantity': f'Only {item.product.stock} left in stock.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        item.quantity = int(quantity)
        item.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """DELETE /api/cart/clear/"""
        self.get_cart().items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items')
        )

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """POST /api/orders/checkout/  {address_id}"""
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response(
                {'detail': 'Your cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = Address.objects.get(
            pk=serializer.validated_data['address_id'], user=request.user
        )

        with transaction.atomic():
            items = cart.items.select_related('product').select_for_update()

            for item in items:
                if item.quantity > item.product.stock:
                    return Response(
                        {'detail': f'{item.product.name} is out of stock.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            order = Order.objects.create(
                user=request.user,
                status=Order.Status.CONFIRMED,
                total_amount=cart.total,
                shipping_address={
                    'full_name': address.full_name,
                    'line1': address.line1,
                    'line2': address.line2,
                    'city': address.city,
                    'state': address.state,
                    'postal_code': address.postal_code,
                    'country': address.country,
                },
            )

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                for item in items
            ])

            for item in items:
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])

            cart.items.all().delete()

        return Response(
            OrderSerializer(order).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """POST /api/orders/<id>/cancel/"""
        order = self.get_object()
        if order.status not in [
            Order.Status.PENDING,
            Order.Status.CONFIRMED,
            Order.Status.PAID,
        ]:
            return Response(
                {'detail': 'This order can no longer be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            for item in order.items.select_related('product'):
                item.product.stock += item.quantity
                item.product.save(update_fields=['stock'])
            order.status = Order.Status.CANCELLED
            order.save(update_fields=['status'])

        return Response(OrderSerializer(order).data)