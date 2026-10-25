from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView,UpdateView,DetailView,CreateView,DeleteView
from . models import *
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate,login,logout
import json
from vendor.models import *
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from tinymce.models import HTMLField
import re
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def admindashboard(request):
    """View to display all products"""
    products = Product.objects.all().prefetch_related('product_images')
    return render(request, 'vendor/admindashboard.html', {'object_list': products})

def maindash(request):
    return render(request, 'vendor/dashboard/main-dashboard.html')


# class home(TemplateView):
#     template_name = 'vendor/admindashboard.html'

class vendor(TemplateView):
    template_name = 'vendor/admin/index.html'

# def vendor(request):
#     return render(request, 'vendor/admin/index.html') 

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def is_valid_password(password):
            # Password criteria: Minimum length 8, at least one uppercase, one lowercase, one digit
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
            return True
        else:
            return False

def HandleRegister(request):
    if request.method == "POST":
        # firstname = request.POST['fname']
        # lastname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 =request.POST['password2']


        user= User.objects.create_user(username, email, pass1)
        return redirect('home')
            
           

    return render(request, 'vendor/vendorregister.html')

class Login(TemplateView):
    template_name = 'vendor/auth/login.html'

def HandleLogin(request):
    if request.method == "POST":
        login_user =request.POST['loginuser']
        login_password = request.POST['login_password']

        user =authenticate(request,username=login_user,password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")   
            return redirect('vendor')
        else:
            messages.error(request, "Invalid Username or Password")   
            
    
   
def HandleLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('vlogin')


def add_category(request):
    if request.method == 'POST':
        # Access form fields
        try:
            name = request.POST['category_name']
            slug = request.POST['slug']
            description = request.POST['category-description']
            category_image = request.FILES.get('category_image', None)  # Use request.FILES for file uploads

            # Basic validation (optional but recommended)
            if not all([name, slug, description]):
                return HttpResponse("Please fill in all required fields.")
            
            # Print statements for debugging
            print(name, slug, description, category_image)
        # Create the Category instance
        
            category = Category.objects.create(
                category_name=name,
                slug=slug,
                description=description,
                category_image=category_image
            )
            # Optionally redirect to a success page or back to the form
            return HttpResponse("Category added successfully!")
        
        except Exception as e:
            # Handle any unexpected errors
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'vendor/category/addcategory.html')

class CategoryListView(ListView):
    model = Category
    template_name = 'vendor/category/show_categories.html'

class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name= "vendor/category/categories_edit.html"    
    success_url = reverse_lazy ('categories_list')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories_list')  # Redirect after successful deletion
    template_name = 'vendor/delete.html'  # Template for confirmation

def add_products(request):
    if request.method == 'POST':
        try:
            # get form data
            p_name = request.POST['product_name']
            p_slug = request.POST['productslug']
            p_description = request.POST['product-description']
            p_specification = request.POST['product-specification']
            p_price = request.POST['price']
            p_stock = request.POST['stock']
            p_available = request.POST['is_available'] == '1'
            p_category_id = request.POST['category']

            # Validation
            if not all([p_name, p_slug, p_description, p_price, p_stock, p_category_id]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'vendor/products/addproduct.html', {
                    'categories': Category.objects.all()
                })
            
            # Get category
            p_category = get_object_or_404(Category, id=p_category_id)
            

            # create product
            product = Product.objects.create(
                product_name = p_name,
                slug=p_slug,
                description=p_description,
                specification=p_specification,
                price=p_price,
                stock=p_stock,
                is_available=p_available,
                category=p_category,
            )

            image_files = request.FILES.getlist('images')
            for image in image_files:
                ProductImage.objects.create(product=product, image=image)

            # Optionally redirect to a success page or back to the form
            return HttpResponse("Product added successfully!")
        
        except Exception as e:
            # Handle any unexpected errors
            return HttpResponse(f"An error occurred: {e}")

    categories = Category.objects.all()   
    return render(request, 'vendor/products/addproduct.html', {'categories': categories})

def products_list(request):
    """View to display all products"""
    products = Product.objects.all().prefetch_related('product_images')
    return render(request, 'vendor/products/show_product.html', {'object_list': products})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('productShow')  # Redirect after successful deletion
    template_name = 'vendor/delete.html'  # Template for confirmation


def addblog(request):
    if request.method == 'POST':
        title = request.POST['blog_title']
        slug = request.POST['blog_slug']
        description = request.POST['blog_description']
        images = request.FILES.get('blog_images')


        try:
            allinterior = Blog.objects.create(
                blog_title = title,
                slug=slug,
                blog_description=description,
                blog_images=images,
            )

            # Optionally redirect to a success page or back to the form
            return HttpResponse("Interior 3D added successfully!")
            
        except Exception as e:
            # Handle any unexpected errors
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'vendor/blogs/addblogs.html')

    
    


