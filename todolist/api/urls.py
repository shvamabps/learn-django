from api import views
from django.urls import path

urlpatterns = [
    path("", view=views.LoginView.as_view(), name="auth"),
    path("register/", view=views.RegisterView.as_view(), name="register"),
    path("todo/", view=views.IndexView.as_view(), name="index"),
    path("home/", view=views.HomeView.as_view(), name="home"),
    path("logout/", view=views.LogoutView.as_view(), name="logout"),
    path("todo/create/", view=views.AddTodosView.as_view(), name="create"),
    path(
        "todo/update/<str:todoId>/",
        view=views.UpdateTodosView.as_view(),
        name="update_todo",
    ),
    path(
        "todo/delete/<str:todoId>/",
        view=views.DeleteTodosView.as_view(),
        name="delete_todo",
    ),
]
