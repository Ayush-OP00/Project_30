from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Extra Fields
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

