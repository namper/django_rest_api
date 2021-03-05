from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls", namespace="blog"))
]
