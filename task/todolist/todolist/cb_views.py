from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todolist.models import ToDoList


class TodoListView(ListView):
    queryset = ToDoList.objects.all()
    template_name = 'todolist.html'
    paginate_by = 10
    ordering = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = ToDoList
    template_name = 'todoinfo.html'
    context_object_name = 'todo'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:      # 이방법 추천
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TodoDetailView, self).get_context_data(**kwargs)
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
        object = self.model.objects.get(pk=self.kwargs['pk'])
        return object

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:      # 이방법 추천
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('cbv:list')