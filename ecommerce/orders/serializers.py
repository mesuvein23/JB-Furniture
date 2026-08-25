from rest_framework import serializers
from products.models import Product
from products.serializers import ProductListSerializer
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source='product', write_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal']

    def validate(self, attrs):
        product = attrs.get('product') or self.instance.product
        quantity = attrs.get('quantity', 1)
        if quantity > product.stock:
            raise serializers.ValidationError(
                {'quantity': f'Only {product.stock} left in stock.'}
            )
        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'item_count']

    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'status_display', 'total_amount',
            'shipping_address', 'items', 'created_at',
        ]
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    """Input only — takes an address id, produces an Order."""
    address_id = serializers.IntegerField()

    def validate_address_id(self, value):
        user = self.context['request'].user
        if not user.addresses.filter(pk=value).exists():
            raise serializers.ValidationError('Address not found.')
        return value