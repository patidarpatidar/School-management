from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_delete,post_save
from django.dispatch import Signal
from .models import Attendance , UserProfile,Teacher,Student,TeacherStudent
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.mail import send_mail 
from django.conf import settings


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



#post_save.connect(student_data,sender=Student,weak=False,dispatch_uid=None)


'''
@receiver(post_delete,sender=Attendance)
def my_callback(sender,**kwargs):
    print("Request finished!")
    print(sender)
    print(kwargs)

post_delete.connect(my_callback,sender=Attendance,weak=False,dispatch_uid=None)

post_delete.disconnect(receiver=None,sender=None,dispatch_uid=None)

custom_signal = Signal()

@receiver(custom_signal)
def show_data(sender,initial,**kwargs):
    print("attendance deleted")
    print(sender.username)
    print(sender.first_name)
    print(initial)
    print(kwargs)  
 
notification = Signal(providing_args=["request","user"])

@receiver(notification)
def show(sender,**kwargs):
    print(sender)
    print(kwargs)

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.userprofile.save()

post_save.connect(save_profile,sender=User)


@receiver(request_finished,sender=Attendance)
def finished(sender,**kwargs):
    print('attendance record view')
    print(sender)

request_finished.connect(finished,sender=Attendance,weak=False,dispatch_uid=None)

'''
