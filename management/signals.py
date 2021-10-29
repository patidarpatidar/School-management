from django.dispatch import receiver

from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail 
from django.conf import settings
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@receiver(reset_password_token_created)
def send_password_reset_email(sender,instance,reset_password_token,*args,**kwargs):
  email = reset_password_token.user.email
  token = reset_password_token.key
  domain = settings.DOMAIN
  url = domain + reverse('password_reset:reset-password-confirm')
  subject = "Password reset link!"
  email_from = settings.EMAIL_HOST_USER
  message = 'Token id = ' + token + "\n" + url
  send_mail(subject,message,email_from,[email])

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def created_auth_token(sender,instance=None,created=False,**kwargs):
  if created:
    Token.objects.create(user=instance)






@receiver(post_save,sender=User)
def send_signup_email(sender,instance,created,**kwargs):
    # email sending for confirmation
  if created:
    email = instance.email
    subject = "Confirmation link"
    domain = settings.DOMAIN
    message = domain + reverse('management:login')
    email_from = settings.EMAIL_HOST_USER
    to_list = [email]
    #send_mail(subject,message,email_from,to_list,fail_silently=False)



