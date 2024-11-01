from api import views
from django.urls import path

urlpatterns = [
    path("", view=views.login, name="auth"),
    path("register/", view=views.register, name="register"),
    path("todo/", view=views.index, name="index"),
    path("home/", view=views.home, name="home"),
    path("logout/", view=views.logout, name="logout"),
    path("todos/create/", view=views.add_todos, name="create"),
]
