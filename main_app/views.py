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

from .models import Animal # This was pointing to main_app.models

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