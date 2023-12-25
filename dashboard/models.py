from django.db import models
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField()

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"
        
    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    event_link = models.URLField()
    image_url = models.URLField()
