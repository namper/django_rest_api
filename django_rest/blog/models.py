from django.db import models

# Create your models here.


class Blog(models.Model):
    name=models.CharField(max_length=100)
    author_name=models.CharField(max_length=50)

    def __str__(self):
        return self.name