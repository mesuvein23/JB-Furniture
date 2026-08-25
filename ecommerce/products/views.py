from django.db.models import Count
from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer
)
from .filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images')
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]