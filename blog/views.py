from re import search
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView,
    )
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def post(self, request, *arg, **kwargs):
        search_title = request.POST['search-title']
        search_tag = request.POST['search-tag']
        tag_results = Post.objects.all()

        if request.POST['search-tag'] == "funny":
            tag_results = Post.objects.filter(tags=1)

        if request.POST['search-tag'] == "exciting":
            tag_results = Post.objects.filter(tags=2)

        if request.POST['search-tag'] == "scary":
            tag_results = Post.objects.filter(tags=3)

        if request.POST['search-tag'] == "delicious":
            tag_results = Post.objects.filter(tags=4)

        if request.POST['search-tag'] == "sad":
            tag_results = Post.objects.filter(tags=5)


        if request.POST['search-title']:
            search_results = tag_results.filter(title__contains=search_title)
        else:
            search_results = tag_results

        context = {
            "title": search_title,
            "tag": search_tag,
            "posts": search_results
        }

        return render(request, self.template_name, context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        post_data = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if post_data.likes.filter(id=self.request.user.id).exists():
            liked = True

        total_likes = post_data.total_likes()
        tag_list = []
        
        for tag in post_data.tags.all():
            tag_list.append(tag)
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['tag_list'] = tag_list
        context['title'] = post_data.title  
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked= False
        post.likes.remove(request.user.id)
    else:
        liked = True
        post.likes.add(request.user.id)

    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))