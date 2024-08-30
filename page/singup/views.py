from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google.views import oauth2_login
from allauth.account.views import SignupView
import smtplib
from email.message import EmailMessage
import uuid

def send_verification_email(user):
    token = uuid.uuid4().hex
    user.verification_token = token
    user.save()
    msg = EmailMessage()
    msg.set_content('Please click on the link to verify your email: http://example.com/verify_email/' + token)
    msg['Subject'] = 'Verify your email'
    msg['From'] = 'your_email@example.com'
    msg['To'] = user.email
    server = smtplib.SMTP_SSL('smtp.example.com', 465)
    server.login('your_email@example.com', 'your_password')
    server.send_message(msg)
    server.quit()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            send_verification_email(user)
            return redirect('email_verification_sent')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

class GoogleSignupView(SignupView):
    adapter_class = GoogleOAuth2Adapter

    def get(self, request, *args, **kwargs):
        return oauth2_login(request, *args, **kwargs)

def email_verification_sent(request):
    return render(request, 'email_verification_sent.html')

def verify_email(request, token):
    user = CustomUser.objects.get(verification_token=token)
    if user:
        user.is_email_verified = True
        user.verification_token = None
        user.save()
        return redirect('home')
    else:
        return redirect('email_verification_failed')