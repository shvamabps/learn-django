from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import LoginForm, RegisterForm, TodoListForm
from .models import TodoList


class IndexView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("home")
        return redirect("auth")


class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, "todo/auth.html", {"form": form})

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful.")
                return redirect("home")
            messages.error(request, "Invalid username or password.")
        return render(request, "todo/auth.html", {"form": form})


class RegisterView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("home")
        form = RegisterForm()
        return render(request, "todo/register.html", {"form": form})

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("auth")
        messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, "todo/register.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request: HttpRequest):
        auth_logout(request)
        messages.success(request, "Logout successful.")
        return redirect("auth")


@method_decorator(login_required(login_url="auth"), name="dispatch")
class HomeView(View):
    def get(self, request: HttpRequest):
        todos = TodoList.objects.filter(created_by_id=request.user.id).select_related(
            "created_by"
        )
        return render(request, "todo/home.html", {"todos": todos})


@method_decorator(login_required(login_url="auth"), name="dispatch")
class AddTodosView(View):
    def get(self, request: HttpRequest):
        form = TodoListForm()
        return render(request, "todo/create_todo.html", {"form": form})

    def post(self, request: HttpRequest):
        form = TodoListForm(request.POST)
        if form.is_valid():
            TodoList.objects.create(
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                created_by_id=request.user.id,
                completed=form.cleaned_data.get("completed"),
            )
            messages.success(request, "Todo added successfully.")
            return redirect("create")
        messages.error(request, "Failed to add todo item.")
        return render(request, "todo/create_todo.html", {"form": form})


@method_decorator(login_required(login_url="auth"), name="dispatch")
class UpdateTodosView(View):
    def get(self, request: HttpRequest, todoId: str):
        todo = get_object_or_404(
            TodoList, todo_id=todoId, created_by_id=request.user.id
        )
        form = TodoListForm(instance=todo)
        return render(request, "todo/update_todo.html", {"form": form, "todo": todo})

    def post(self, request: HttpRequest, todoId: str):
        todo = get_object_or_404(
            TodoList, todo_id=todoId, created_by_id=request.user.id
        )
        form = TodoListForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully.")
            return redirect("home")
        messages.error(request, "Failed to update todo item.")
        return render(request, "todo/update_todo.html", {"form": form, "todo": todo})


@method_decorator(login_required(login_url="auth"), name="dispatch")
class DeleteTodosView(View):
    def get(self, request: HttpRequest, todoId: str):
        todo = get_object_or_404(
            TodoList, todo_id=todoId, created_by_id=request.user.id
        )
        print(todo)
        todo.delete()
        messages.success(request, "Todo deleted successfully.")
        return redirect("home")
