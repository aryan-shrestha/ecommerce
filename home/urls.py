from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('all_products/', ProductsView.as_view(), name='all_products'),
    path('category/<str:slug>', CategoryItemView.as_view(), name='category'),
    path('brand/<str:slug>', BrandItemView.as_view(), name='brand'),
    path('search', ItemSearchView.as_view(), name='search'),
    path('item_detail/<str:slug>', ItemDetailView.as_view(), name='item_detail'),

    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
