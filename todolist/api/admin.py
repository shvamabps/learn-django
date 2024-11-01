from django.contrib import admin

from .models import TodoList


class TodoListAdmin(admin.ModelAdmin):
    model = TodoList

    list_display = (
        "todo_id",
        "title",
        "description",
        "completed",
        "created_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("completed", "created_at")
    search_fields = ("title", "description")
    ordering = ("created_at",)


admin.site.register(TodoList, TodoListAdmin)
