import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Q, Min, Max, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from .models import *
from .forms import SignUpForm, EmailLoginForm


# ================= PAGES =================

def home(request):
    sale_products = Product.objects.filter(is_available=True)
    all_interio = Blog.objects.all()
    return render(request, 'customer/main/home.html', {'sale_products': sale_products, 'all_interio': all_interio})


def aboutus(request):
    return render(request, 'customer/main/aboutus.html')


def reviews(request):
    return render(request, 'customer/products/review_page.html')


def blogs(request):
    all_interio = Blog.objects.all()
    return render(request, 'customer/main/blogs/all_blogs.html', {'all_interio': all_interio})


def blogs_detail(request, slug):
    all_blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'customer/main/blogs/blog.html', {'all_blog': all_blog})


def help_section_view(request):
    cards = HelpCard.objects.all()
    return render(request, 'help_section/help_section.html', {'cards': cards})


# ================= CONTACT =================

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '')
        subject = request.POST.get('subject', '').strip()

        errors = {}
        if not first_name:
            errors['firstname'] = "Please enter your first name."
        if not email:
            errors['email'] = "Please enter your email."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Please enter a valid email address."
        if city not in dict(Contact.CITY_CHOICES):
            errors['city'] = "Please select a city."
        if not subject:
            errors['subject'] = "Please write your message."

        if not errors:
            Contact.objects.create(
                first_name=first_name, last_name=last_name,
                email=email, city=city, subject=subject,
            )
            messages.success(request, "Thank you! Your message has been sent. We'll get back to you soon.")
            return redirect('contact')

        return render(request, 'customer/main/contact.html', {'errors': errors, 'data': request.POST})

    data = {}
    if request.GET.get('quote'):
        data['subject'] = "Hi, I'd like a quote for: "
    return render(request, 'customer/main/contact.html', {'data': data})


# ================= SEARCH =================

def HandleSearchData(request):
    query = request.GET.get('query', '').strip()

    if not query:
        messages.warning(request, "Please enter something to search for.")
        search_data = Product.objects.none()
    elif len(query) > 72:
        messages.warning(request, "Your search is too long. Please try a shorter one.")
        search_data = Product.objects.none()
    else:
        search_data = Product.objects.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query),
            is_available=True,
        ).distinct()

    return render(request, 'customer/main/search.html', {'search': search_data, 'query': query})


# ================= PRODUCT LISTINGS =================

def _product_listing(request, products):
    """Shared filtering, sorting and pagination for product listing pages."""

    # ----- price range -----
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    try:
        if min_price:
            products = products.filter(price__gte=float(min_price))
    except ValueError:
        min_price = ''
    try:
        if max_price:
            products = products.filter(price__lte=float(max_price))
    except ValueError:
        max_price = ''

    # ----- sorting -----
    sort = request.GET.get('sort', 'newest')
    sort_options = {
        'newest': '-id',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'product_name',
    }
    products = products.order_by(sort_options.get(sort, '-id'))

    # ----- pagination -----
    product_count = products.count()
    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)

    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()          # for pagination links
    params.pop('category', None)
    querystring_no_cat = params.urlencode()   # for category links on the Sale page

    return {
        'products': page_obj,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_pages': paginator.num_pages,
        'product_count': product_count,
        'categories': Category.objects.all(),
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'querystring': querystring,
        'querystring_no_cat': querystring_no_cat,
        'price_limits': Product.objects.filter(is_available=True).aggregate(low=Min('price'), high=Max('price')),
        'filters_active': bool(min_price or max_price or sort != 'newest'),
    }


def products(request, category_slug=None):
    category = None
    qs = Product.objects.filter(is_available=True).prefetch_related('product_images')

    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        qs = qs.filter(category=category) if category else Product.objects.none()

    context = _product_listing(request, qs)
    context.update({'category': category, 'category_slug': category_slug})
    return render(request, 'customer/products/product.html', context)


def sale_products(request):
    category = None
    qs = Product.objects.filter(is_available=True).prefetch_related('product_images')

    cat_slug = request.GET.get('category')
    if cat_slug:
        category = Category.objects.filter(slug=cat_slug).first()
        if category:
            qs = qs.filter(category=category)

    context = _product_listing(request, qs)
    context['category'] = category
    if category:
        context['filters_active'] = True
    return render(request, 'customer/products/allsale_products.html', context)


# ================= CATEGORIES =================

def categories(request):
    categories = Category.objects.all()
    return render(request, 'customer/categories/categories.html', {'categories': categories})


def categories_display(request):
    categories = Category.objects.all()
    return render(request, 'customer/main/home.html', {'categories': categories})


def show_categories_item(request, category_slug):
    categories = Category.objects.filter(slug=category_slug)
    return render(request, 'customer/categories/show_categories_item.html', {'categories': categories})


# ================= PRODUCT DETAIL =================

def products_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product.objects.prefetch_related('product_images').select_related('category'),
        category__slug=category_slug, slug=product_slug,
    )

    cart_item = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=single_product, is_active=True
    ).first()

    reviews = single_product.reviews.order_by('-created_at')
    review_count = reviews.count()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    related_products = (Product.objects
                        .filter(category=single_product.category, is_available=True)
                        .exclude(id=single_product.id)
                        .prefetch_related('product_images')[:4])

    return render(request, 'customer/products/product_detail.html', {
        'single_product': single_product,
        'in_cart': cart_item is not None,
        'cart_item_quantity': cart_item.quantity if cart_item else 0,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'related_products': related_products,
    })


# ================= WISHLIST (logged-in users) =================

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product').order_by('-added')
    return render(request, 'customer/wishlist/wishlist.html', {'items': items})


def toggle_wishlist(request, product_id):
    back = request.META.get('HTTP_REFERER') or '/'

    # guests: ask them to log in, then bring them back to the product
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to save items to your wishlist.")
        return redirect_to_login(back)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        existing = Wishlist.objects.filter(user=request.user, product=product)
        if existing.exists():
            existing.delete()
            messages.info(request, f"{product.product_name} removed from your wishlist.")
        else:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, f"{product.product_name} added to your wishlist.")
    return redirect(back)


# ================= CART (works for guests) =================

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


def _get_cart_items(request):
    """Return (cart_items, total, quantity) for the current visitor."""
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    if not cart:
        return CartItem.objects.none(), 0, 0
    cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    return cart_items, total, quantity


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    cart_item = CartItem.objects.filter(product=product, cart=cart).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    messages.success(request, 'Product added to cart.')
    return redirect('cart')


def cart(request):
    cart_items, total, quantity = _get_cart_items(request)
    return render(request, 'customer/cart/cart.html', {
        'total': total, 'quantity': quantity, 'cart_items': cart_items,
    })


def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    cart_item = CartItem.objects.filter(product_id=product_id, cart=cart).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


def remove_cart_items(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    CartItem.objects.filter(product_id=product_id, cart=cart).delete()
    messages.warning(request, 'Product removed from cart.')
    return redirect('cart')


# ================= CHECKOUT (login required) =================

@login_required
def checkout(request):
    cart_items, total, quantity = _get_cart_items(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
    return render(request, 'customer/cart/checkout.html', {
        'total': total, 'quantity': quantity, 'cart_items': cart_items,
    })


@login_required
def buynow(request):
    return render(request, 'customer/order/buynow.html')


@login_required
def placeorder(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart_items, total, quantity = _get_cart_items(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # save the order
    neworder = Order(
        user=request.user,
        fname=request.POST.get('fname'),
        lname=request.POST.get('lname'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        country=request.POST.get('country'),
        zipcode=request.POST.get('zipcode'),
        payment_mode=request.POST.get('payment_mode'),
        total_price=total,
    )
    neworder.save()

    # tracking number: YYYYMMDD + order id
    neworder.tracking_no = datetime.date.today().strftime("%Y%m%d") + str(neworder.id)
    neworder.save()

    # order items
    for item in cart_items:
        OrderItem.objects.create(
            order=neworder,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
        )

    # email to the shop (won't break checkout if email isn't set up)
    product_list = ", ".join(item.product.product_name for item in cart_items)
    send_mail(
        subject='JB Furniture - New Order Received',
        message=f'New order {neworder.tracking_no} containing: {product_list}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['jayabarahifurniture@gmail.com'],
        fail_silently=True,
    )

    cart_items.delete()

    messages.success(request, f"Order placed! Your tracking number is {neworder.tracking_no}. You can follow it in My Orders.")
    return redirect('my_orders')


# ================= ACCOUNTS =================

def _keep_cart(request, old_key):
    """Logging in gives a new session key; move the guest cart to it."""
    new_key = request.session.session_key
    if old_key and new_key and old_key != new_key:
        Cart.objects.filter(cart_id=old_key).update(cart_id=new_key)


def _next_url(request, default='home'):
    nxt = request.POST.get('next') or request.GET.get('next')
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return nxt
    return default


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            old_key = request.session.session_key
            login(request, user)
            _keep_cart(request, old_key)
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect(_next_url(request))
    else:
        form = SignUpForm()
    return render(request, 'customer/account/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            old_key = request.session.session_key
            login(request, form.get_user())
            _keep_cart(request, old_key)
            return redirect(_next_url(request))
    else:
        form = EmailLoginForm(request)
    return render(request, 'customer/account/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def my_orders(request):
    orders = (Order.objects.filter(user=request.user)
              .prefetch_related('orderitem_set__product')
              .order_by('-created_at'))
    return render(request, 'customer/account/my_orders.html', {'orders': orders})