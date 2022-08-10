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
  path('animals/<int:animal_id>/add_photo/', views.add_photo, name='add_photo'),
  path('animals/<int:animal_id>/add_medication/', views.add_medication, name='add_medication'),
  path('medication/<int:pk>/update/', views.MedicationUpdate.as_view(), name='medications_update'),
  path('medication/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medications_delete'),
  path('feeding/create/', views.FeedingCreate.as_view(), name='feedings_create'),
  path('feeding/<int:pk>/update/', views.FeedingUpdate.as_view(), name='feedings_update'),
  path('feeding/<int:pk>/delete/', views.FeedingDelete.as_view(), name='feedings_delete'),
]