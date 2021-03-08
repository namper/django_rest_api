from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    
class Blog(models.Model):
    name = models.CharField(max_length=100)
    author_name=models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
