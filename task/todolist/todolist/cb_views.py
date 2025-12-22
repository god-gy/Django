from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todolist.form import CommentForm
from todolist.models import ToDoList, Comment


class TodoListView(LoginRequiredMixin, ListView):
    queryset = ToDoList.objects.all()
    template_name = 'todolist.html'
    paginate_by = 10
    ordering = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset

class TodoDetailView(ListView):
    model = ToDoList
    template_name = 'todoinfo.html'
    context_object_name = 'todo'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(ToDoList, pk=kwargs.get('todo_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:      # 이방법 추천
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by('-created_at')
        paginator = Paginator(comments, 5)
        context = {
            'todo' : self.object.__dict__,
            'comment_form': CommentForm(),
            'page_obj': paginator.get_page(self.request.GET.get('page'))
        }
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = ToDoList
    template_name = 'todocreate.html'
    fields = ['title', 'description', 'start_date', 'end_date']

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()
        self.object = todo
        return HttpResponseRedirect(self.get_success_url())

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoList
    template_name = 'todoupdate.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'is_complete']

    def get_object(self, queryset = None):
        object = self.model.objects.get(pk=self.kwargs['todo_pk'])
        return object

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:      # 이방법 추천
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('cbv:list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('cbv:detail', kwargs={'todo_pk': self.object.pk}))

    def get_todo(self):
        pk = self.kwargs['todo_pk']
        todo = get_object_or_404(ToDoList, pk=pk)
        return todo

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset = None):
        object = self.model.objects.get(pk=self.kwargs['todo_pk'])
        if not self.request.user.is_superuser:
            object = get_object_or_404(ToDoList, pk=object.pk)
        return object

    def get_success_url(self):
        return reverse_lazy('cbv:detail', kwargs={'todo_pk': self.object.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset = None):
        object = self.model.objects.get(pk=self.kwargs['todo_pk'])
        if not self.request.user.is_superuser:
            object = get_object_or_404(ToDoList, pk=object.pk)
        return object

    def get_success_url(self):
        return reverse_lazy('cbv:list')