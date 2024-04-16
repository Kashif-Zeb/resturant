from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    subject = 'Login Notification'
    message = f'Hello {user.Firstname},\n\nYou have successfully logged into your account.\n\nRegards,\nYour Website Team'
    sender_email = settings.EMAIL_HOST_USER  
    recipient_email = "kashifzk216@gmail.com"  #user.email
    send_mail(subject, message, sender_email, [recipient_email])