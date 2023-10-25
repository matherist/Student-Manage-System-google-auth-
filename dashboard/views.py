from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic

from .rand_pict import *
import requests
from bs4 import BeautifulSoup

from django.contrib.auth.models import User 
default_user = User.objects.get(username='dinaiym')

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST["title"], description=request.POST["description"])
            notes.save()
        messages.success(request, f"Notes added from {request.user.username} successfully!")
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes


def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST["subject"],
                title = request.POST["title"],
                due = request.POST['due'],


            )
    form = HomeworkForm()    
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homework, 
        'homework_done': homework_done, 
        'form': form}
    return render(request, 'dashboard/homework.html', context)

def fetch_and_save_events():
    url = "https://it-events.com/"
    response = requests.get(url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        event_items = soup.find_all("div", class_="event-list-item")

        for item in enumerate(event_items):

            event = Event(
                user=default_user, 
                title=item.find("a", class_="event-list-item__title").text,
                date=item.find("div", class_="event-list-item__info").text,
                event_link="https://it-events.com" + item.find("a", class_="event-list-item__title")["href"],
               
            )
            location_element = item.find("div", class_="event-list-item__info_location")
            event.location = location_element.text if location_element else "Location not available"
            event.save()

def events(request):
    fetch_and_save_events()
    events = Event.objects.all()[:18]
    return render(request, 'header/events.html', {'events': events, 'images': data_links})