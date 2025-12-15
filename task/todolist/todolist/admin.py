from django.contrib import admin

from .models import ToDoList

@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'is_complete')
    list_display_links = ('id', 'title')
    list_filter = ('is_complete',)