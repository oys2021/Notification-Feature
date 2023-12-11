from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

@receiver(post_delete)
def delete_notification(sender, instance, **kwargs):
    if sender.__name__ == 'Task':
        Task = apps.get_model('testing', 'Task')
        Notification.objects.filter(user=instance.user, message=f"New task assigned: {instance.task_content}").delete()

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=20)
    task_content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super(Task, self).save(*args, **kwargs)

        # Automatically create a notification when a task is created
        Notification.objects.create(
            user=self.user,
            message=f"New task assigned: {self.task_content}",
        )

    def __str__(self):
        return self.task_name