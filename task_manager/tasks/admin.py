from django.contrib import admin

# Register your models here.
from .models import Task, Photo

admin.site.register(Photo)
admin.site.register(Task)
