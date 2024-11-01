from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .form import LoginForm, RegisterForm, TodoListForm
from .models import TodoList


# Create your views here.
def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return redirect("auth")


def login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                form = LoginForm()
                auth_login(request, user)
                messages.success(request, "Login successful.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
                form = LoginForm()
                return render(request, "todo/auth.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "todo/auth.html", {"form": form})


def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("auth")  # Redirect to the login page
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = RegisterForm()

    return render(request, "todo/register.html", {"form": form})


@login_required
def logout(request: HttpRequest):
    if request.user.is_authenticated:
        request.session.delete()
        messages.success(request, "Logout successful.")
    return redirect("auth")


@login_required(login_url="auth")
def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("auth")

    todos = TodoList.objects.filter(created_by_id=request.user.id).select_related(
        "created_by"
    )

    return render(request, "todo/home.html", {"todos": todos})


@login_required(login_url="auth")
def add_todos(request: HttpRequest):
    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            TodoList.objects.create(
                title=title, description=description, created_by_id=request.user.id
            )
            messages.success(request, "Todo added successfully.")
            return redirect("create")  # Redirect after a successful POST
        else:
            messages.error(request, "Failed to add todo item.")
            # Render the same template with the form containing errors
    else:
        form = TodoListForm()

    return render(request, "todo/create_todo.html", {"form": form})


def update_todos(request: HttpRequest): ...


def delete_todos(request: HttpRequest): ...
