from django.contrib import admin
from .models import Blog,Author
# Register your models here.


admin.site.register([Blog,Author])