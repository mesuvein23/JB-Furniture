from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Category, Product, ProductImage, Blog


# =========================================================
#  Access control: only staff (admin) accounts may use the
#  vendor dashboard. Everyone else is sent to the admin login.
# =========================================================

class StaffRequiredMixin(UserPassesTestMixin):
    """For class-based views: allow staff only."""
    login_url = reverse_lazy('admin:login')

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff


# ================= DASHBOARD =================

@staff_member_required
def admindashboard(request):
    """Vendor dashboard home: all products."""
    products = Product.objects.all().prefetch_related('product_images')
    return render(request, 'vendor/admindashboard.html', {'object_list': products})


# ================= LOGIN / LOGOUT =================

def vendor_login(request):
    """Staff log in through the secure Django admin login, then return to the dashboard."""
    return redirect(f"{reverse('admin:login')}?next={reverse('vendor')}")


def HandleLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('vlogin')


# ================= CATEGORIES =================

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        try:
            name = request.POST['category_name']
            slug = request.POST['slug']
            description = request.POST['category-description']
            category_image = request.FILES.get('category_image', None)

            if not all([name, slug, description]):
                return HttpResponse("Please fill in all required fields.")

            Category.objects.create(
                category_name=name,
                slug=slug,
                description=description,
                category_image=category_image,
            )
            return HttpResponse("Category added successfully!")

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'vendor/category/addcategory.html')


class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'vendor/category/show_categories.html'


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'vendor/category/categories_edit.html'
    success_url = reverse_lazy('categories_list')


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('categories_list')
    template_name = 'vendor/delete.html'


# ================= PRODUCTS =================

@staff_member_required
def add_products(request):
    if request.method == 'POST':
        try:
            p_name = request.POST['product_name']
            p_slug = request.POST['productslug']
            p_description = request.POST['product-description']
            p_specification = request.POST['product-specification']
            p_price = request.POST['price']
            p_stock = request.POST['stock']
            p_available = request.POST['is_available'] == '1'
            p_category_id = request.POST['category']

            if not all([p_name, p_slug, p_description, p_price, p_stock, p_category_id]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'vendor/products/addproduct.html', {
                    'categories': Category.objects.all()
                })

            p_category = get_object_or_404(Category, id=p_category_id)

            product = Product.objects.create(
                product_name=p_name,
                slug=p_slug,
                description=p_description,
                specification=p_specification,
                price=p_price,
                stock=p_stock,
                is_available=p_available,
                category=p_category,
            )

            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)

            return HttpResponse("Product added successfully!")

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'vendor/products/addproduct.html', {'categories': Category.objects.all()})


@staff_member_required
def products_list(request):
    products = Product.objects.all().prefetch_related('product_images')
    return render(request, 'vendor/products/show_product.html', {'object_list': products})


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('productShow')
    template_name = 'vendor/delete.html'


# ================= BLOGS =================

@staff_member_required
def addblog(request):
    if request.method == 'POST':
        title = request.POST['blog_title']
        slug = request.POST['blog_slug']
        description = request.POST['blog_description']
        images = request.FILES.get('blog_images')

        try:
            Blog.objects.create(
                blog_title=title,
                slug=slug,
                blog_description=description,
                blog_images=images,
            )
            return HttpResponse("Blog post added successfully!")

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'vendor/blogs/addblogs.html')