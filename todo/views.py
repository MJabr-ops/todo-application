from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
# Create your views here.
from .models import Karbar,todo as TodoModel,TodoBasket as BasketModel
from rest_framework.renderers import JSONRenderer
from .serializers import KarbarSerializer,TodoBasketSerializer,TodoSerializer
from rest_framework import status
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from rest_framework import exceptions
from .utils import generate_access_token,generate_refresh_token
import jwt
from django.contrib.auth import get_user_model
from .authenticate import SafeJWTAuthentication

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@permission_classes([AllowAny])
@api_view(['POST'])
def registerUser(request):
    userData=request.data
    user=KarbarSerializer(data=userData)
    if user.is_valid():
        print("is valid")

        user.save()

        return Response({"success":True,"data":user.data})

    return Response("is not valid {}".format(user.errors))



class TodoBasket(APIView):

    def get(self,request,format=None):

        user=SafeJWTAuthentication().authenticate(request)


        if user is not None:


            basket=BasketModel.objects.filter(user=user[0].id)


            json_basket=TodoBasketSerializer(basket,many=True)

            return Response(json_basket.data)
        else:
            return Response({'success':False,'error':'user not found'})
    def post(self,request,format=None):
        data=request.data

        user = SafeJWTAuthentication().authenticate(request)
        basket=TodoBasketSerializer(data={'title':data['title'],'user':user[0].id})



        if basket.is_valid():

            basket.save()
            return Response({'success':True,'data':basket.data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'errors':basket.errors})

class TodoBasketDetail(APIView):
    def get_object(self,pk):
        try:

            return BasketModel.objects.get(pk=pk)

        except BasketModel.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        obj=self.get_object(pk)
        serialObj=TodoBasketSerializer(obj)
        return Response({'success':True,'data':serialObj.data},status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):

        data=request.data
        basket=self.get_object(pk)
        serialBasket=TodoBasketSerializer(instance=basket,data=data)

        if(serialBasket.is_valid()):
            serialBasket.save()
            return Response({'success':True,'data':serialBasket.data},status=status.HTTP_200_OK)
        return Response({'success':False,'errors':serialBasket.errors})
    def delete(self,request,pk,format=None):
        obj=self.get_object(pk)
        obj.delete()
        return Response({'success':True},status=status.HTTP_204_NO_CONTENT)



class Todo(APIView):
    #@cache_page(CACHE_TTL)
    def get(self,request,basket):
        todos=TodoModel.objects.filter(todoBasket=basket).order_by('-dateCreated')
        if(todos.count()==0):
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_todos=TodoSerializer(todos,many=True)
            return Response(serialized_todos.data)
    def post(self,request,basket):
        data=request.data
        full_data=data.copy()
        full_data['todoBasket']=basket

        todo=TodoSerializer(data=full_data)
        if(todo.is_valid()):
            todo.save()
            return Response({'success':True,'data':todo.data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'errors':todo.errors},status=status.HTTP_400_BAD_REQUEST)

class TodoDetail(APIView):
    def get(self,request,basket,todo):

            object=get_object_or_404(TodoModel,pk=todo,todoBasket=basket)

            serialobject=TodoSerializer(object)
            return Response(serialobject.data,status=status.HTTP_200_OK)


    def put(self,request,basket,todo):
        object=get_object_or_404(TodoModel,pk=todo,todoBasket=basket)
        serialobject=TodoSerializer(instance=object,data=request.data)
        if serialobject.is_valid():
            serialobject.save()
            return Response({'success': True, 'data': serialobject.data})
        else:
            return Response({'seccess':False,'errors':serialobject.errors})

    def delete(self):
        pass




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # try:
        response=Response()
        if(request.data['email'] and request.data['password']):
            email=request.data['email']
            password=request.data['password']
            if (email is None) or (password is None):
                raise exceptions.AuthenticationFailed(
                    'email and password required')

            user = Karbar.objects.filter(email=email).first()
            if (user is None):
                raise exceptions.AuthenticationFailed('user not found')
            if (not user.check_password(password)):
                raise exceptions.AuthenticationFailed('wrong password')

            serialized_user = KarbarSerializer(user).data

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = {
                'access_token': access_token,
                'user': serialized_user,
            }
            return response

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')


    access_token = generate_access_token(user)
    return Response({'access_token': access_token})






