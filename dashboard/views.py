from django.shortcuts import render, redirect
from .forms import *
from .rand_pict import *
from django.contrib import messages
from django.views import generic
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User 
from youtubesearchpython import VideosSearch
default_user = User.objects.get(username='dinaiym')
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

@login_required
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

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    form = HomeworkForm()  # Initialize the form here

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('is_finished')
                finished = True if finished == 'on' else False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST.get("subject"),
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                due=request.POST.get('due'),
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f"Homework added from {request.user.username}!!!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
      
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homework,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i["title"],
                'duration' : i['duration'],
                'thumbnail' : i["thumbnails"][0]["url"],
                'channel' : i["channel"]["name"],
                'link' : i["link"],
                'views' : i["viewCount"]["short"],
                'published' : i["publishedTime"]
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i["descriptionSnippet"]:
                    desc += j["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, "dashboard/youtube.html", context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)


def fetch_and_save_events():
    # Your web scraping code here to fetch event data
    url = "https://it-events.com/"
    response = requests.get(url)

    if response.status_code  == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        event_items = soup.find_all("div", class_="event-list-item")

        for item in event_items:
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

@login_required
def todo(request):
    form = TodoForm()
    if request.method == "POST":
       if form.is_valid():
        try:
            finished = form.cleaned_data.get("is_finished", False)
            if finished == "on":
                finished = True
            else:
                finished = False
        except:
            finished = False
        todos = Todo(
        user=request.user,
        title=form.cleaned_data["title"],
        is_finished=finished,
    )
        todos.save()
        messages.success(request, f"Todo added from {request.user.username}!!")
    # else:
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todos': todo,
        'done': todos_done
    }
    return render(request, "dashboard/todo.html", context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


# def books(request):
#     return render(request, "dashboard/books.html") #2:26:35


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect('login')
    else:
       form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, "dashboard/register.html", context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homes_done': homeworks_done,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/profile.html', context)