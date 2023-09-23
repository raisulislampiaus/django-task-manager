from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    photos = models.ManyToManyField('Photo', blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='task_photos/')

    def __str__(self):
        return str(self.image)

