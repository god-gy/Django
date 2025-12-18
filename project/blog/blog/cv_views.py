from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from blog.models import Blog

class BlogListView(ListView):
    queryset = Blog.objects.all().order_by('-created_at')
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

class BlogCreateView(LoginRequiredMixin ,CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ['title', 'content']
    # success_url = reverse_lazy('cv_blog_list')

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.author = self.request.user
        # self.object.save()

        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        self.object = blog

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cv_blog_detail', kwargs={'pk': self.object.pk})
