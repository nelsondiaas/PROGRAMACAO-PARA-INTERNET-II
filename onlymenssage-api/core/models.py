from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    status = models.CharField(max_length=120)
    

