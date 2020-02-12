from rest_framework.generics import ListAPIView
from .serializers import PostSerializer
from django.shortcuts import render
from .models import Post
from .forms import CommentForm
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
import requests


# @login_required()
def home(request):
    # posts = Post.objects.all
    posts = requests.get('http://127.0.0.1:8000/api/posts/').json()
    for p in posts:
        x = p['date_posted'].split('T')
        p['date_posted'] = "{} > time: {}".format(
            x[0], (x[1].split('.'))[0])
        # print(p['date_posted'])
    context = {
        'posts': posts,
        'title': 'home',
    }
    return render(request, 'blog/home.html', context)


# class Home(generics.RetrieveAPIView):#apiHome
#     posts = Post.objects.all()
#     renderer_class = [TemplateHTMLRenderer]
#     serializer = PostSerializer(posts, many=True)

#     def get(self, request, *args, **kwargs):
#         self.objects = self.serializer.data
#         return Response({'posts': self.objects}, template_name='blog/home.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['- date_posted']


@api_view(['GET', 'POST', 'PUT'])
def post_list_api(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=204)


@api_view(['GET', 'POST', 'DELETE'])
def post_detail_api(request, pk):

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error, status=400)

    # elif request.method == 'UPDATE':
    #     data = JSONParser().parse(request)
    #     serializer = PostSerializer(post, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return JsonResponse(serializer.error, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def PostDetailView(request, pk):
    template_name = 'blog/post_detail.html'
    post = Post.objects.get(id=pk)
    comments = post.comments.all()

    #       .filter(active=True) # to make comments allowed by admin's permission only
    new_comment = None
    new_reply = None
    # Comment posted

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'object': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})  # {comments': comments,'new_comment': new_comment,'comment_form': comment_form} to be inluded in context dictionary


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})
