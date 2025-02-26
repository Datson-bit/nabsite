from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('ICT', 'ICT Officer'),
        ('COUNCILOR', 'Councilor'),
        ('HOD', 'Head of Department'),
        ('CHAIRMAN', 'Chairman')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} - {self.role}"