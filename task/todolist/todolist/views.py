from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from todolist.form import TodolistForm
from todolist.models import ToDoList

@login_required()
def todo_list(request):
    todos = ToDoList.objects.filter(user=request.user).order_by('-modified_at')
    request.session['count'] = request.session.get('count', 0) + 1

    q = request.GET.get('q')
    if q:
        todos = todos.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(todos, 10)
    page= request.GET.get('page')
    page_object= paginator.get_page(page)

    context = {
        'todos': todos,
        'count': request.session['count'],
        'page_object': page_object,
    }
    return render(request, 'todolist.html', context)

def todo_info(request, pk):
    todo = get_object_or_404(ToDoList, pk=pk)
    context = {'todo': todo}
    return render(request, 'todoinfo.html', context)

@login_required()
def todo_create(request):
    form = TodolistForm(request.POST or None)
    print(form)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todoinfo', kwargs={'pk': todo.pk}))

    context = {'form': form}
    return render(request, 'todocreate.html', context)

@login_required()
def todo_update(request, pk):
    todo = get_object_or_404(ToDoList, pk=pk, user=request.user)

    form = TodolistForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo = form.save()
        return redirect(reverse('todoinfo', kwargs={'pk': todo.pk}))

    context = {
        'form': form,
    }
    return render(request, 'todoupdate.html', context)

@login_required()
@require_http_methods(['POST'])
def todo_delete(request, pk):
    todo = get_object_or_404(ToDoList, pk=pk, user=request.user)
    todo.delete()
    return redirect(reverse('todolist'))
