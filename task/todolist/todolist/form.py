from django import forms

from todolist.models import ToDoList

class TodolistForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ("title", "description", "start_date", "end_date")

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ("title", "description", "start_date", "end_date", "is_complete")