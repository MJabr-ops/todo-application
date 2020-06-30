from django.urls import path
from . import views

from TodoApplication import settings
from django.views.decorators.cache import cache_page
urlpatterns=[
 path('register',views.registerUser),
 path('login',views.login),
 path('refresh_token',views.refresh_token_view),
 path('basket',cache_page(settings.CACHE_TTL)(views.TodoBasket.as_view())),
 path('basket/<int:pk>',cache_page(settings.CACHE_TTL)(views.TodoBasketDetail.as_view())),
 path('basket/<int:basket>/todo',cache_page(settings.CACHE_TTL)(views.Todo.as_view())),
 path('basket/<int:basket>/todo/<int:todo>',cache_page(settings.CACHE_TTL)(views.TodoDetail.as_view())),

]