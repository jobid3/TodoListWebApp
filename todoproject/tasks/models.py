from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MajorTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_task_id = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'user_task_id')

    def save(self, *args, **kwargs):
        if self.user_task_id == 0:
            last = MajorTask.objects.filter(user=self.user).order_by('-user_task_id').first()
            self.user_task_id = (last.user_task_id + 1) if last else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    major_task = models.ForeignKey(MajorTask, on_delete=models.CASCADE, related_name='subtasks')
    task_subtask_id = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('major_task', 'task_subtask_id')

    def save(self, *args, **kwargs):
        if self.task_subtask_id == 0:
            last = SubTask.objects.filter(major_task=self.major_task).order_by('-task_subtask_id').first()
            self.task_subtask_id = (last.task_subtask_id + 1) if last else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title