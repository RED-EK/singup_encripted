from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)

def validate_email(email):
    if email.split('@')[-1] not in ['proton.me', 'protonmail.com', 'gmail.com']:
        raise ValidationError('Only Protonmail, Proton.me, or Gmail emails are allowed')