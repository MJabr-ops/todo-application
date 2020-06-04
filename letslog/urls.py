from rest_framework_simplejwt import views as simp_jwt
from django.urls import path
from . import views
urlpatterns=[
    path('api/token',simp_jwt.TokenObtainPairView.as_view()),
    path('api/token/refresh',simp_jwt.TokenRefreshView.as_view()),
    path('app',views.HelloView.as_view())

]