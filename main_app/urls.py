from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('accounts/signup/', views.signup, name='signup'),
  path('animals/', views.animals_index, name='animals_index'),
  path('animals/<int:animal_id>/', views.animals_detail, name='animals_detail'),
  path('animals/create/', views.AnimalCreate.as_view(), name='animals_create'),
  path('animals/<int:pk>/update/', views.AnimalUpdate.as_view(), name='animals_update'),
  path('animals/<int:pk>/delete/', views.AnimalDelete.as_view(), name='animals_delete'),
]