from django.contrib import admin
from vendor.models import *
# Register your models here.


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class ProductImageInline(admin.TabularInline):     
    model = ProductImage
    extra = 3
    readonly_fields = ('uploaded_at',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available') 
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline]                


class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'slug', 'blog_images', 'blog_description') 
    prepopulated_fields = {'slug': ('blog_title',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Blog,BlogAdmin)
