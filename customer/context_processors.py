from .models import Cart, CartItem, Wishlist


def counts(request):
    if request.path.startswith('/admin'):
        return {}

    # ----- cart -----
    cart_count = 0
    session_key = request.session.session_key
    if session_key:
        cart = Cart.objects.filter(cart_id=session_key).first()
        if cart:
            for item in CartItem.objects.filter(cart=cart, is_active=True):
                cart_count += item.quantity

    # ----- wishlist -----
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    else:
        wishlist_ids = request.session.get('wishlist', [])

    return {
        'cart_count': cart_count,
        'wishlist_count': len(wishlist_ids),
        'wishlist_ids': wishlist_ids,
    }