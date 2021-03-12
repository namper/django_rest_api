from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return  self.title

class Category(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-id',)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    author_name=models.ForeignKey(User, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)


    def __str__(self):
        return self.name

class Comment(models.Model):
    comment=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.name
