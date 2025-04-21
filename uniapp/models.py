from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

TASK_STAGES = [
    ('todo', 'To Do'),
    ('in_progress', 'In Progress'),
    ('review', 'Review'),
    ('completed', 'Completed'),
]

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='university_users',
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='university_user_permissions',
        blank=True,
        help_text='User-specific permissions.',
        verbose_name='user permissions',
    )

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_students = models.ManyToManyField(User, limit_choices_to={'role': 'student'})
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    attachments = models.FileField(upload_to='projects/', blank=True, null=True)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    deadline = models.DateField()
    stage = models.CharField(max_length=20, choices=TASK_STAGES, default='todo')
    comments = models.TextField(blank=True)
    attachments = models.FileField(upload_to='tasks/', blank=True, null=True)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)