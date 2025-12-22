from django import forms

from todolist.models import ToDoList, Comment


class TodolistForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ("title", "description", "start_date", "end_date")

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ("title", "description", "start_date", "end_date", "is_complete")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("massage", )
        widgets = {
            'massage': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control', 'placeholder': '댓글을 입력하세요'}),
        }
        labels = {
            'massage' : '내용'
        }
