from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=10)
    session = models.CharField(max_length=10)
    description = models.TextField(max_length=1000)
    evaluation = models.IntegerField(default=1)
    signature = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
