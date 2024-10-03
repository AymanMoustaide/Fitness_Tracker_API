from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    fitness_level = models.CharField(max_length=50, null=True, blank=True)

    # Override the groups and user_permissions fields to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Add a custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Add a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.FloatField(help_text='Duration in minutes')
    calories_burned = models.FloatField()

    def __str__(self):
        return self.name

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=100)
    target_value = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.goal_type

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_entries')
    progress_value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"Progress for {self.goal}"

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}"