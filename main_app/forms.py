from django.forms import ModelForm
from .models import Medication, Feeding, Care_Log, Weight

class MedicationForm(ModelForm):
  class Meta:
    model = Medication
    fields = ['name', 'dosage', 'frequency', 'description', 'end_date']

class FeedingForm(ModelForm):
  class Meta:
    model = Feeding
    fields = ['date', 'description']

class Care_LogForm(ModelForm):
  class Meta:
    model = Care_Log
    fields = ['date', 'description']

class WeightForm(ModelForm):
  class Meta:
    model = Weight
    fields = ['date', 'description']