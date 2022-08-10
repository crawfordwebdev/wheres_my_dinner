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
  path('animals/<int:animal_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('animals/<int:animal_id>/add_weight/', views.add_weight, name='add_weight'),
  path('animals/<int:animal_id>/add_care_log/', views.add_care_log, name='add_care_log'),
  path('medication/<int:pk>/update/', views.MedicationUpdate.as_view(), name='medications_update'),
  path('medication/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medications_delete'),
  path('feeding/<int:pk>/update/', views.FeedingUpdate.as_view(), name='feedings_update'),
  path('feeding/<int:pk>/delete/', views.FeedingDelete.as_view(), name='feedings_delete'),
  path('weight/<int:pk>/update/', views.WeightUpdate.as_view(), name='weight_update'),
  path('weight/<int:pk>/delete/', views.WeightDelete.as_view(), name='weight_delete'),
  path('care-log/<int:pk>/update/', views.Care_LogUpdate.as_view(), name='care_log_update'),
  path('care-log/<int:pk>/delete/', views.Care_LogDelete.as_view(), name='care_log_delete'),
]