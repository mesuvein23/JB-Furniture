from rest_framework import serializers
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'product_count']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight — used for grid/listing pages."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'stock',
            'in_stock', 'category_name', 'primary_image',
        ]

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if not image:
            return None
        request = self.context.get('request')
        url = image.image.url
        return request.build_absolute_uri(url) if request else url


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full payload — used for the single product page."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'stock',
            'in_stock', 'is_active', 'category', 'category_id',
            'images', 'created_at',
        ]
        read_only_fields = ['slug', 'created_at']