from django.urls import path
from . import views


urlpatterns=[
 path('register',views.registerUser),
 path('login',views.login),
 path('basket',views.TodoBasket.as_view()),
 path('basket/<int:pk>',views.TodoBasketDetail.as_view()),
 path('basket/<int:basket>/todo',views.Todo.as_view()),
 path('basket/<int:basket>/todo/<int:todo>',views.TodoDetail.as_view()),
 path('',views.sendReact)
]