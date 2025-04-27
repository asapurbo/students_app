from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# signup info
class SignUp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signup')
    created_at = models.DateTimeField(auto_now_add=True)
    isValid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
