from django.db import models
from django.contrib.auth.models import User

class MajorTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='major_tasks')

    def __str__(self):
        return self.title

class MinorTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    major_task = models.ForeignKey(MajorTask, on_delete=models.CASCADE, related_name='minor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title