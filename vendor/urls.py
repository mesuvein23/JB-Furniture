from django.urls import path
from . import views

urlpatterns = [
    # ---------- dashboard (staff only) ----------
    path('vendor/', views.admindashboard, name="vendor"),

    # ---------- categories ----------
    path('addcategory/', views.add_category, name="addcategory"),
    path('category_list/', views.CategoryListView.as_view(), name="categories_list"),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name="category_edit"),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name="category_delete"),

    # ---------- products ----------
    path('addproduct/', views.add_products, name="addproduct"),
    path('productShow/', views.products_list, name="productShow"),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name="products_delete"),

    # ---------- blogs ----------
    path('addblog/', views.addblog, name="addblog"),

    # ---------- staff login / logout ----------
    path('vlogin/', views.vendor_login, name="vlogin"),
    path('logout/', views.HandleLogout, name="logout"),
]