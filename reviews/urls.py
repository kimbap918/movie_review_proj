from django.urls import path 
from . import views

app_name = 'reviews'

urlpatterns = [
  path('', views.index, name='index'),
  path('create/', views.create, name='create'),
  path('community/', views.community, name='community'),
  path('detail/<int:pk>', views.detail, name='detail'),
]