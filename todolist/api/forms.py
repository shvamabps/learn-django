from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    password_validators_help_texts,
    validate_password,
)
from django.core.exceptions import ValidationError

from .models import TodoList


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["title", "description", "completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "completed": forms.CheckboxInput(
                attrs={
                    "class": "w-4 h-4 text-blue-500 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            }
        )
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e)
        return password

    def password_validators_help_texts(self):
        return password_validators_help_texts()
