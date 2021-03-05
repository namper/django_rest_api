from django.urls import path
from . import views
app_name="blog"


urlpatterns = [
    path('', views.BlogList.as_view(), name="blog-list"),
    path('<int:pk>/', views.BlogDetail.as_view(), name="blog-detail"),
    path('registration/', views.CreateUser.as_view(), name="registration"),
    path('login/', views.CustomAuthToken.as_view(), name="login"),
    path('users/', views.ListUser.as_view(), name="list"),
    # path('logout/', views.Logout.as_view(), name="logout")
]
