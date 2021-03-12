from django import http
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import views
from rest_framework.serializers import Serializer
from rest_framework.settings import import_from_string
from .models import  Blog,Category,Tag,Comment
from django.http import HttpResponse, Http404, response
from .serializers import BlogSerializer,RegisterSerializer,CategorySerializer,TagSerializer,CommentSerializer
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from  django_filters.rest_framework import  DjangoFilterBackend


class TagList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class BlogList(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id','name',]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)





class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer


    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({'detail': 'სხვაგან მოხვდი!'}, 
                            status=status.HTTP_404_NOT_FOUND)

        return super(BlogDetail, self).handle_exception(exc)

    def delete(self, request, pk):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]




class CreateUser(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=RegisterSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            "user": serializer.data, 
            "token": token.key
        })
    
    

class ListUser(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class CustomAuthToken(generics.CreateAPIView):
    serializer_class=AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)