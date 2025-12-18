from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        self.object = blog

        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse_lazy('cv_blog_detail', kwargs={'pk': self.object.pk})
    # models에 정의

class BlogUpdateView(LoginRequiredMixin ,UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ['title', 'content']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    # def get_object(self, queryset = None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404()
    #     return self.object

    # def get_success_url(self):
    #     return reverse_lazy('cv_blog_detail', kwargs={'pk': self.object.pk})
    # models에 정의
