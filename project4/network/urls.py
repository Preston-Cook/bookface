
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('following', views.following, name="following"),
    path('account/<str:username>', views.account, name="account"),

    # API Routes
    path('edit/<int:post_id>', views.edit, name="edit"),
    path('info/<int:post_id>', views.info, name='info'),
    path('delete/<int:post_id>', views.delete, name="delete"),
    path('like/<int:post_id>', views.like, name="like"),
    path('follow/<str:username>', views.follow, name="follow")
]