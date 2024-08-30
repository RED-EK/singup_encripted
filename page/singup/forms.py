from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@proton.me') and not email.endswith('@protonmail.com') and not email.endswith('@gmail.com'):
            raise ValidationError('Only Protonmail, Proton.me, or Gmail emails are allowed')
        return email