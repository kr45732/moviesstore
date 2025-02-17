from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item

def index(request):
    """
    Display the shopping cart page.
    """
    # Get the cart from the session
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    
    # Fetch movies in the cart
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    
    # Calculate the cart total
    cart_total = calculate_cart_total(cart, movies_in_cart)
    
    # Prepare template data
    template_data = {
        'cart_total': cart_total,
        'movies_in_cart': [
            {'title': movie.title, 'price': movie.price}
            for movie in movies_in_cart
        ],
    }
    return render(request, 'cart/index.html', {'template_data': template_data})

@login_required
def purchase(request):
    """
    Handle the purchase process.
    """
    # Get the cart from the session
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    
    # Redirect if the cart is empty
    if not movie_ids:
        return redirect('cart.index')
    
    # Fetch movies in the cart
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    
    # Calculate the cart total
    cart_total = calculate_cart_total(cart, movies_in_cart)
    
    # Create an order
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    
    # Create items for the order
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    
    # Clear the cart
    request.session['cart'] = {}
    
    # Prepare template data for the purchase confirmation page
    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
    }
    return render(request, 'cart/purchase.html', {'template_data': template_data})

def clear(request):
    """
    Clear the shopping cart.
    """
    # Clear the cart from the session
    request.session['cart'] = {}
    return redirect('cart.index')

def add(request, id):
    """
    Add a movie to the shopping cart.
    """
    # Get the cart from the session
    cart = request.session.get('cart', {})
    
    # Add the movie to the cart or increment its quantity
    cart[str(id)] = cart.get(str(id), 0) + 1
    
    # Save the updated cart in the session
    request.session['cart'] = cart
    
    return redirect('cart.index')