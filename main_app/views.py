from typing import List
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Animal, Photo, Feeding, Weight, Care_Log, Medication # This was pointing to main_app.models
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
  return render(request, 'animals/detail.html', {
    'animal': animal, 
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