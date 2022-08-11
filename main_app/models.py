from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

SEX = (
  ('U', 'Unknown'),
  ('F', 'Female'),
  ('M', 'Male'),
  ('B', 'Blank')
)

class Animal(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  sex = models.CharField(
    max_length=1,
    choices=SEX,
    default=SEX[0][0]
  )
  species = models.CharField(max_length=100, blank=True)
  breed = models.CharField(max_length=100, blank=True)
  color = models.CharField(max_length=100, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('animals_detail', kwargs={'animal_id': self.id})
  
  def get_sex(self):
    return f"{self.get_sex_display()}"
  
  class Meta:
    ordering = ['species', 'name']

class Photo(models.Model):
  url = models.CharField(max_length=250)
  animal = models.OneToOneField(Animal, on_delete=models.CASCADE)

class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  description = models.CharField(max_length=100)
  animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.date}: {self.description}"
    
  def get_absolute_url(self):
    return reverse('animals_detail', kwargs={'animal_id': self.animal.id})    
  
  class Meta:
    ordering = ['-date']

class Weight(models.Model):
  date = models.DateField('Weigh Date')
  description = models.CharField(max_length=50)
  animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.date}: {self.description}"
    
  def get_absolute_url(self):
    return reverse('animals_detail', kwargs={'animal_id': self.animal.id})

  class Meta:
    ordering = ['-date']

class Care_Log(models.Model):
  date = models.DateField()
  description = models.CharField('Description of Care', max_length=100)
  animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.date}: {self.description}"
  
  def get_absolute_url(self):
    return reverse('animals_detail', kwargs={'animal_id': self.animal.id})
  
  class Meta:
    ordering = ['-date']

class Medication(models.Model):
  name = models.CharField(max_length=100)
  dosage = models.CharField(max_length=50)
  frequency = models.CharField(max_length=50)
  description = models.CharField(max_length=100)
  end_date = models.DateField('End Date', blank=True)
  animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('animals_detail', kwargs={'animal_id': self.animal.id})