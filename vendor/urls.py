from django.urls import path
from . import views
from . views import *

urlpatterns = [
    path('vendor/',views.admindashboard,name="vendor"),
    # path('vendor/maindash/',views.maindash,name="maindash"),
    
    path('addcategory/',views.add_category,name="addcategory"),
    # path('listCategories/',views.listCategories,name="listcategories"),
    path('products/delete/<int:pk>/',ProductDeleteView.as_view(),name="products_delete"),

    path('category_list/',CategoryListView.as_view(),name="categories_list"),
    path('category/edit/<int:pk>/',CategoryUpdateView.as_view(),name="category_edit"),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name="category_delete"),

    path('addproduct/',views.add_products,name="addproduct"),
    # path('productShow/',ProductListView.as_view(),name="productShow"),
    
    
    path('addblog/',views.addblog,name="addblog"),
    path('productShow/',views.products_list,name="productShow"),

    path('vlogin/', Login.as_view(), name="vlogin"),
    path('accounts/login/', views.HandleLogin, name="login"),
    path('logout/',views.HandleLogout, name="logout"),
    
    path("signup/", SignUpView.as_view(), name="signup"),
    path('vregister/',views.HandleRegister, name="vregister"),


]