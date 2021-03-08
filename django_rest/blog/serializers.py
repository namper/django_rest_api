import email
from django.core.management.color import Style
from .models import Blog,Author
from rest_framework import serializers
from django.contrib.auth.models import User



class AuthorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']



class BlogSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Blog
        fields = ['id',  'name', 'author_name']

    def to_representation(self, instance):
        self.fields['author_name'] = AuthorSerializer()
        return super(BlogSerializer, self).to_representation(instance)

    

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