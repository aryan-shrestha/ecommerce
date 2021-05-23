from django.urls import path
from . import views

urlpatterns = [
    path('item/', views.item_list),
    path('item/<int:pk>/', views.item_detail),
    path('brand/', views.brand_list),
    path('brand/<int:pk>/', views.brand_detail),
    path('category/', views.category_list),
    path('category/<int:pk>/', views.category_detail),

]