from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from cart.models import Wishlist, Cart

class BaseView(View):
    views = {}

class HomeView(BaseView):
    def get(self, request):
        self.views['category'] = Category.objects.filter(status='active')
        self.views['slider'] = Slider.objects.filter(status='active')
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.filter(status='active')
        self.views['hots'] = Item.objects.filter(status='active', label='hot')
        self.views['new'] = Item.objects.filter(status='active', label='new')
        self.views['my_wishlist_items'] = Wishlist.objects.filter(username=request.user.username).count()
        self.views['my_cart_items'] = Cart.objects.filter(username=request.user.username, checkout=False).count()

        return render(request, 'index.html', self.views)

class ProductsView(BaseView):
    def get(self, request):
        self.views['all_products'] = Item.objects.all()

        return render(request, 'product-list.html', self.views)

class CategoryItemView(BaseView):
    def get(self, request, slug):
        category_id = Category.objects.get(slug=slug).id
        self.views['cat_items'] = Item.objects.filter(category=category_id)
        return render(request, 'category.html', self.views)

class BrandItemView(BaseView):
    def get(self, request, slug):
        brand = Brand.objects.get(name=slug)
        self.views['brand_items'] = brand.item_set.all()
        return render(request, 'brand.html', self.views)

class ItemSearchView(BaseView):
    def get(self, request):
        search = request.GET.get('search', None)
        print("Form submitted")
        print(request.GET)
        if search is None:
            return redirect('/')
        else:
            self.views['search_item'] = Item.objects.filter(name__icontains = search)
            print(self.views['search_item'])
            return render(request, 'search.html', self.views)

class ItemDetailView(BaseView):
    def get(self, request, slug):
        self.views['items_detail'] = Item.objects.filter(slug = slug)
        category = self.views['items_detail'][0].category
        self.views['related_items'] = Item.objects.filter(category=category)
        return render(request, 'product-detail.html', self.views)

def signup(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        if request.method == 'POST':
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            cpassword = request.POST['cpassword']

            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is already taken! ')
                    return redirect('home:signup')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already taken')
                    return redirect('home:signup')
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=f_name,
                        last_name=l_name
                    )
                    user.save()
                    messages.error(request, 'Account Created!!')
                    return redirect('home:signup')
            else:
                messages.error(request, 'The passwords doesnot match!! ')
                return redirect('home:signup')
    return render(request, 'login.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid Credentials ')
                return redirect('home:login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home:login')


