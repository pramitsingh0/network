
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:username>", views.view_profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following_posts/", views.following_posts, name="following_posts")
]
