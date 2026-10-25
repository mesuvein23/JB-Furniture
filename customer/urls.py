from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ---------- pages ----------
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('review/', views.reviews, name="reviews"),
    path('blogs/', views.blogs, name="blogs"),
    path('blog/<slug:slug>/', views.blogs_detail, name='blog_detail'),
    path('search/', views.HandleSearchData, name="search"),

    # ---------- products & categories ----------
    path('products/', views.products, name="products"),
    path('products/<slug:category_slug>/', views.products, name="products_by_category"),
    path('products/<slug:category_slug>/<slug:product_slug>', views.products_detail, name="products_detail"),
    path('sale/', views.sale_products, name="sale"),
    path('categories/', views.categories, name="categories"),
    path('categories/<slug:category_slug>/', views.show_categories_item, name="category_item"),

    # ---------- cart ----------
    path('cart/', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name="add_cart"),
    path('remove_cart/<int:product_id>/', views.remove_cart, name="remove_cart"),
    path('remove_cart_items/<int:product_id>/', views.remove_cart_items, name="remove_cart_items"),

    # ---------- wishlist ----------
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # ---------- checkout ----------
    path('checkout/', views.checkout, name="checkout"),
    path('placeorder/', views.placeorder, name="placeorder"),
    path('buynow/', views.buynow, name="buynow"),

    # ---------- accounts ----------
    path('account/signup/', views.signup_view, name='account_signup'),
    path('account/login/', views.login_view, name='account_login'),
    path('account/logout/', views.logout_view, name='account_logout'),
    path('account/orders/', views.my_orders, name='my_orders'),

	    # ---------- password: change (logged in) ----------
    path('account/password/change/', auth_views.PasswordChangeView.as_view(
        template_name='customer/account/password_change.html'), name='password_change'),
    path('account/password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='customer/account/password_change_done.html'), name='password_change_done'),

    # ---------- password: forgot / reset ----------
    path('account/password/reset/', auth_views.PasswordResetView.as_view(
        template_name='customer/account/password_reset.html',
        email_template_name='customer/account/password_reset_email.txt',
        subject_template_name='customer/account/password_reset_subject.txt'), name='password_reset'),
    path('account/password/reset/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='customer/account/password_reset_done.html'), name='password_reset_done'),
    path('account/password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='customer/account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('account/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='customer/account/password_reset_complete.html'), name='password_reset_complete'),
]