from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class MajorTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_task_id = models.PositiveIntegerField(editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'user_task_id')

    def save(self, *args, **kwargs):
        if not self.user_task_id:
            # Get the max user_task_id for this user and increment
            last_task = MajorTask.objects.filter(user=self.user).order_by('-user_task_id').first()
            self.user_task_id = (last_task.user_task_id + 1) if last_task else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    major_task = models.ForeignKey(MajorTask, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} (of {self.major_task})'