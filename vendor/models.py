from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

# Create your models here.

class Base(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+",db_column="created_by",null=True)
    created_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+",db_column="updated_by",null=True)
    updated_at = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug= models.SlugField(max_length=100,unique=True)
    description = HTMLField(max_length=255,blank=True)
    category_image = models.ImageField(upload_to='category_images/', null=True, default="")

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'category'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique= True)
    slug = models.SlugField(max_length=200, unique=True)
    description = HTMLField()
    specification = HTMLField(default='')
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_title(self):
        return self.product_name

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])
    
    def get_first_image(self):
        """Helper method to get the first image"""
        first_image = self.product_images.first()
        return first_image.image.url if first_image else None

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"

class Blog(models.Model):
    blog_title = models.CharField(max_length=200, unique= True)
    slug = models.SlugField(max_length=200, unique=True)
    blog_description = HTMLField()
    blog_images = models.ImageField(upload_to='media')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title


