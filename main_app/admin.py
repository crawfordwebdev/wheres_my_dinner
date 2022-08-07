from django.contrib import admin
from .models import Animal, Photo, Feeding, Weight, Care_Log, Medication

admin.site.register(Animal)
admin.site.register(Photo)
admin.site.register(Feeding)
admin.site.register(Weight)
admin.site.register(Care_Log)
admin.site.register(Medication)