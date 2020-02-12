from django.urls import path
from . import views
from users import views as user_view
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.home, name="blog-home"),
    # path('', views.Home.as_view(), name="blog-home"),
    path('register/', user_view.register, name="register"),
    path('post/<int:pk>/', views.PostDetailView, name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('about/', views.about, name="blog-about"),
]
