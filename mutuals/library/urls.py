from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('', views.home, name="home"),
    path('t/<str:pk>/', views.topic, name="topic"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-post/', views.createPost, name="create-post"),
    path('update-post/<str:pk>', views.updatePost, name="update-post"),
    path('delete-post/<str:pk>', views.deletePost, name="delete-post"),
    path('delete-comment/<str:pk>', views.deleteComment, name="delete-comment"),
]
