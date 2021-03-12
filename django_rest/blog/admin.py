from django.contrib import admin
from .models import Blog,Category,Tag,Comment
# Register your models here.


admin.site.register([Blog,Category,Tag,Comment])