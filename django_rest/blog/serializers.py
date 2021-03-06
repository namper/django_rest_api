import email
from django.core.management.color import Style
from .models import Blog,Category,Tag,Comment
from rest_framework import serializers
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','comment', 'created', 'blog']

    def to_representation(self, instance):
        rep = super(CommentSerializer, self).to_representation(instance)
        rep['blog'] = instance.blog.name
        return rep

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['id','title']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title']



class BlogSerializer(serializers.ModelSerializer):
    # tag=TagSerializer(many=True,read_only=True)
    active_blog=serializers.SerializerMethodField()

    def get_active_blog(self,obj):
        return Blog.objects.filter(is_active=True).count()

    class Meta:
        model = Blog
        fields = ['id',  'name', 'is_active', 'author_name','category','tag','active_blog']


    def to_representation(self, instance):
        rep = super(BlogSerializer, self).to_representation(instance)
        rep['author_name'] = instance.author_name.username
        rep['category']=instance.category.title

        return rep



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True,)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "პაროლები არ ემთხვევა"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user