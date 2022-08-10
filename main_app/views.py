from typing import List
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Animal, Photo, Feeding, Weight, Care_Log, Medication # This was pointing to main_app.models
from .forms import MedicationForm
import uuid
import boto3

# Add these "constant" variables below the imports
S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'wheremydinner'

@login_required
def animals_index(request):
  # Only get animals that belong to the user
  animals = Animal.objects.filter(user=request.user)
  # You could also retrieve the logged in user's animals like this
  # animals = request.user.animal_set.all()
  return render(request, 'animals/index.html', {'animals': animals})

@login_required
def animals_detail(request, animal_id):
  animal = Animal.objects.get(id=animal_id)
  # Using the manager’s `exclude` method to grab all toys that don’t need the condition passed to it.
  # The Django Query API enables **[Field Lookups](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups)** for every field in the model. `id__in` is one such field lookup that checks if the model’s `id` is in a list and that list is being created with this code.
  # toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  # feeding_form = FeedingForm()
  feedings = Feeding.objects.filter(animal_id=animal_id) # [:5] Only get 5 max
  weights = Weight.objects.filter(animal_id=animal_id)
  medications = Medication.objects.filter(animal_id=animal_id)
  medication_form = MedicationForm()
  care_log = Care_Log.objects.filter(animal_id=animal_id)
  return render(request, 'animals/detail.html', {
    'animal': animal, 'feedings': feedings, 'weights': weights, 'care_log': care_log, 'medications': medications, 'medication_form': medication_form
  })

@login_required
def add_photo(request, animal_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, animal_id=animal_id)
      # Remove old photo if it exists
      cat_photo = Photo.objects.filter(animal_id=animal_id)
      if cat_photo.first():
        cat_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('animals_detail', animal_id=animal_id)

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('animals_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

@login_required
def add_medication(request, animal_id):
  form = MedicationForm(request.POST)
  if form.is_valid():
    new_medication = form.save(commit=False)
    new_medication.animal_id = animal_id
    new_medication.save()
  return redirect('animals_detail', animal_id=animal_id)

class Home(LoginView):
  template_name = 'home.html'

class AnimalCreate(LoginRequiredMixin, CreateView):
  model = Animal
  fields = ['name', 'age', 'sex', 'species', 'breed', 'color']
  success_url = '/animals/'

  # This inherited method is called when a valid cat form is being submitted
  def form_valid(self, form):
    form.instance.user = self.request.user  # form.instance is the Animal
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class AnimalUpdate(LoginRequiredMixin, UpdateView):
  model = Animal
  fields = ['name', 'age', 'sex', 'species', 'breed', 'color']

class AnimalDelete(LoginRequiredMixin, DeleteView):
  model = Animal
  success_url = '/animals/'

class MedicationUpdate(LoginRequiredMixin, UpdateView):
  model = Medication
  fields  = ['name', 'dosage', 'frequency', 'description', 'end_date']

class MedicationDelete(LoginRequiredMixin, DeleteView):
  model = Medication
  
  def get_success_url(self):
    return reverse_lazy('animals_detail', kwargs={'animal_id': self.object.animal.id})


from .models import Animal, Photo, Feeding, Weight, Care_Log, Medication # This was pointing to main_app.models


class FeedingCreate(LoginRequiredMixin, CreateView):
  model = Feeding
  fields  = ['date','description']
  def form_valid(self, form):
    form.instance.animal = Animal.objects.get(pk=self.kwargs.get('pk'))
    print(f'form.instance.animal: {form.instance.animal}')
    # if form.instance.animal.user != self.request.user:
    #   raise form.ValidationError("You are not authorized to change to this animal.")

    return super().form_valid(form)

class FeedingUpdate(LoginRequiredMixin, UpdateView):
  model = Feeding
  fields  = ['date','description']

class FeedingDelete(LoginRequiredMixin, DeleteView):
  model = Feeding
  def get_success_url(self):
    return reverse_lazy('animals_detail', kwargs={'animal_id': self.object.animal.id})