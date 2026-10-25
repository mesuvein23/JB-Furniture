from django.contrib import admin
from .models import *

admin.site.site_header = "JB Furniture Admin"
admin.site.site_title = "JB Furniture Admin"
admin.site.index_title = "Store Management"


# ================= ORDERS =================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'product_price', 'quantity')
    readonly_fields = ('product', 'product_price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_no', 'fname', 'lname', 'phone', 'city', 'total_price',
                    'payment_mode', 'status', 'user', 'created_at')
    list_display_links = ('tracking_no', 'fname')
    list_editable = ('status',)
    list_filter = ('status', 'payment_mode', 'created_at')
    search_fields = ('tracking_no', 'fname', 'lname', 'email', 'phone')
    readonly_fields = ('user', 'tracking_no', 'total_price', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order', {'fields': ('tracking_no', 'status', 'total_price', 'payment_mode', 'payment_id',
                              'created_at', 'updated_at')}),
        ('Customer', {'fields': ('user', 'fname', 'lname', 'email', 'phone')}),
        ('Delivery address', {'fields': ('address', 'city', 'state', 'country', 'zipcode')}),
        ('Notes', {'fields': ('message',)}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'product_price', 'quantity', 'created_at')
    search_fields = ('order__tracking_no', 'product__product_name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'payment_method')


# ================= CART & WISHLIST =================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    list_filter = ('is_active',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added')
    search_fields = ('user__username', 'product__product_name')


# ================= CUSTOMERS & CONTENT =================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'created')
    list_filter = ('city',)
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    readonly_fields = ('created',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('name', 'product__product_name', 'comment')


@admin.register(HelpCard)
class HelpCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'link_url')
    list_editable = ('order',)