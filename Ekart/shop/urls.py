from django.urls import path
from . import views

urlpatterns = [
  path('',views.index,name = 'index'),
  path(r'index/', views.index,name = 'index'),
  path(r'about/',views.about,name='about'),
  path(r'contact/',views.contact,name='contact'),
  path(r'products/<int:myid>/',views.products,name='products'),
  path(r'search/',views.search,name='search'),
  path(r'checkout/',views.checkout,name='checkout'),
  path(r'tracker/',views.tracker,name='tracker'),
 
]
