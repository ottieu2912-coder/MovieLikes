from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<str:title>', views.like, name='like'),
    path('dislike/<str:title>', views.dislike, name='dislike'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    #unlike and undislike undo the actions of liking and disliking a movie
    path('unlike/<str:title>', views.unlike, name="unlike"),
    path('undislike/<str:title>', views.undislike, name="undislike"),
    path('signup/', views.signUp, name='signup')

]