import uuid

from django.contrib.auth.models import User
from django.db import models


class TodoList(models.Model):
    class Meta:
        verbose_name = "Todo List"
        verbose_name_plural = "Todo Lists"
        db_table = "todolist"
        ordering = ["-created_at"]  # Default ordering by created_at descending
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["completed"]),
            models.Index(fields=["title"]),
        ]

    todo_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, name="todo_id"
    )
    title = models.CharField(max_length=120, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Completed")
    created_by = models.ForeignKey(
        User,
        related_name="todolist",
        on_delete=models.CASCADE,
        name="created_by",
        verbose_name="Created By",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title
