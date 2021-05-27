from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
import json

from home.models import Item
from .models import Cart, Wishlist, Contact
from home.views import BaseView


# Create your views here.

@login_required(login_url='home:login')
def addToCart(request):
    data = json.loads(request.body)
    slug = data['productSlug']

    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).discounted_price

    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price

    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        quantity += 1
        total = original_price * quantity
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity, total=total)
        if Wishlist.objects.filter(username=username, slug=slug).exists():
            Wishlist.objects.filter(username=username, slug=slug).delete()

        return JsonResponse("Item was added", safe=False)

    else:
        quantity = 1

    total = original_price * quantity

    data = Cart.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug)[0],
        slug=slug,
        quantity=quantity,
        total=total,
    )

    if Wishlist.objects.filter(username=username, slug=slug).exists():
        Wishlist.objects.filter(username=username, slug=slug).delete()
    messages.success(request, f'{data.items.name}  added in cart!!')

    return JsonResponse("Item was added", safe=False)

class CartView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views['my_cart'] = Cart.objects.filter(username=username, checkout=False)
        cart_items = self.views['my_cart']
        grand_total = 0
        for item in cart_items:
            grand_total = grand_total + item.total
        self.views['grand_total'] = grand_total

        return render(request, 'cart.html', self.views)

@login_required(login_url='home:login')
def add_to_wishlist(request, slug):
    username = request.user.username
    item = Item.objects.get(slug=slug)
    if Cart.objects.filter(username=username, items=item.id).exists() or Wishlist.objects.filter(username=username,
                                                                                                 items=item.id).exists():
        messages.success(request, f'{item} already added in cart!!')
        return HttpResponseRedirect(reverse('cart:my_cart'))
    else:
        Wishlist.objects.create(username=username, items=item, slug=slug)
        return HttpResponseRedirect(reverse('cart:my_wishlist'))


class WishlistView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views['wishlist'] = Wishlist.objects.filter(username=username)
        return render(request, 'wishlist.html', self.views)


def delete_wishlist(request, slug):
    username = request.user.username
    item = Wishlist.objects.filter(username=username, slug=slug)
    item.delete()
    return HttpResponseRedirect(reverse('cart:my_wishlist'))


def delete_cart(request, slug):
    username = request.user.username
    item = Cart.objects.filter(username=username, slug=slug, checkout=False)
    item.delete()
    return HttpResponseRedirect(reverse('cart:my_cart'))


def increase_quantity(request, slug):
    username = request.user.username
    item = Cart.objects.get(username=username, slug=slug, checkout=False)
    item.quantity = item.quantity + 1
    item.total = Item.objects.get(slug=slug).price * item.quantity
    item.save()

    return HttpResponseRedirect(reverse('cart:my_cart'))


def decrease_quantity(request, slug):
    username = request.user.username
    item = Cart.objects.get(username=username, slug=slug, checkout=False)
    item.quantity = item.quantity - 1
    item.total = Item.objects.get(slug=slug).price * item.quantity
    item.save()

    return HttpResponseRedirect(reverse('cart:my_cart'))

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email_address = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact.objects.create(
            name=name,
            email=email_address,
            subject=subject,
            message=message,
        )
        contact.save()
        email = EmailMessage(
            'Hello',
            f'name: {name}\nemail: {email_address}\nsubject: {subject}\n{message}',
            'readitbyaryan@gmail.com',
            [email_address]
        )
        email.send()
        messages.success(request,"Your email has been sent!!")

    return render(request, 'contact.html')
