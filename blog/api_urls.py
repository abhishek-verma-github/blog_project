from django.urls import path, include
from .views import post_detail_api, post_list_api
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('', PostListViewApi)

urlpatterns = [

    path('posts/', post_list_api),
    path('posts/<int:pk>', post_detail_api),

]
