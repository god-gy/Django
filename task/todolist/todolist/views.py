from django.shortcuts import render, get_object_or_404

from .models import ToDoList


def todo_list(request):
    todos = ToDoList.objects.all()
    context = {'todos': todos}
    return render(request, 'todolist.html', context)

def todo_info(request, pk):
    todo = get_object_or_404(ToDoList, pk=pk)
    context = {'todo': todo}
    return render(request, 'todoinfo.html', context)
