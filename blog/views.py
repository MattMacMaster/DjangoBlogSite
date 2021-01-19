from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post

from django.contrib.auth import get_user_model

User = get_user_model()

# Currently Replaced by PostListView but kept in as example as method view


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

# Login mixin param, redirects you to login page if instance isnt found


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # Checking if the user is signed in as the post author to create then passes to form valid method

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Login mixin param, redirects you to login page if instance isnt found, and passes test requirement from second mixin


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # Checking if the user is signed in as the post author to edit then passes to form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # This is a check if the user is the author and proceeds if the test passes

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#Legacy and removed


def about(request):
    return render(
        request, 'blog/about.html',
        {'title': 'About'}
    )
