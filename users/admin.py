from django.contrib import admin
from .models import Notes, Homework, Todo, Event, UploadedFile


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'title', 'description', 'due', 'is_finished')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_finished')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'location', 'event_link', 'image_url')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
