from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='home'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('category/', views.category_summary, name='category_summary'),

    path('search/', views.search, name='search'),


]
