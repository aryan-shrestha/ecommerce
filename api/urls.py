from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('item/', views.ItemList.as_view()),
    path('item/<int:pk>/', views.ItemDetail.as_view()),
    path('brand/', views.BrandList.as_view()),
    path('brand/<int:pk>/', views.BrandDetail.as_view()),
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)