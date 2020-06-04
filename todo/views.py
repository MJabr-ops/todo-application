from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
# Create your views here.
from .models import Karbar,todo as TodoModel,TodoBasket as BasketModel
from rest_framework.renderers import JSONRenderer
from .serializers import KarbarSerializer,TodoBasketSerializer,TodoSerializer
from rest_framework import status
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['POST'])
def registerUser(request):
    userData=request.data
    user=KarbarSerializer(data=userData)
    if user.is_valid():
        print("is valid")
        refresh = RefreshToken.for_user(user)
        user.save()

        return Response({"success":True,"data":user.data,"refresh_token":str(refresh),"access_token":str(refresh.access_token)})

    return Response("is not valid {}".format(user.errors))



class TodoBasket(APIView):

    def get(self,request,format=None):

        basket=BasketModel.objects.filter(user=3)
        print(basket)
        json_basket=TodoBasketSerializer(basket,many=True)

        return Response(json_basket.data)
    def post(self,request,format=None):
        data=request.data
        basket=TodoBasketSerializer(data=data)
        print("data is ",data)


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
def login(request):
    try:
        if(request.data['email'] and request.data['password']):
            email=request.data['email']
            password=request.data['password']
            user=get_object_or_404(Karbar,email=email)

            if(check_password(password,user.password)):
                serialUser = KarbarSerializer(user)

                return Response(serialUser.data)

            else:
                return Response({'success':False,'errors':"invalid password"})



    except :
        return Response({'success':False,'errors':"should contain valid email and password"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def sendReact(request):
    return Response({'name':'mohammad','lastname':'jabbari'})



#todo jwt auth


#todo custom permission,and user permission on modifying objects

#todo redis cache
#todo save users password with hashing




#todo must be ordered by number










