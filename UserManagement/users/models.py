from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]
    ACCOUNT_STATE_CHOICES = [
        ('UNVERIFIED', 'Unverified'),
        ('PENDING_VERIFICATION', 'Pending_verification'),
        ('VERIFIED', 'Verified'),

    ]
    

    # photo = models.ImageField(upload_to='user_photos')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=100)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=ACCOUNT_STATE_CHOICES,default='UNVERIFIED')
    NID_or_passport_number = models.CharField(max_length=100, blank=True)
    document_image = models.ImageField(upload_to='documents/', blank=True)
    # Add any additional fields or methods as needed

    def __str__(self):
        return self.username
