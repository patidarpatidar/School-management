from django.forms import ModelForm
from django.conf import settings
from django import forms
from .models import UserProfile , Course ,Subject,StudentCourseRegistration,TeacherSubjectRegistration

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ImageField
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password 

class UserProfileForm(forms.Form):
	GENDER = (
			('MALE','male'),
			('FEMALE','female'),
		)
	ROLE_CHOICE = (
			('STUDENT','student'),
			('TEACHER','teacher'),
			('ADMIN','admin'),
			
		)

	role = forms.ChoiceField(choices=ROLE_CHOICE)
	gender = forms.ChoiceField(choices=GENDER)
	phone = forms.CharField(max_length=20)
	street = forms.CharField(max_length=200)
	city = forms.CharField(max_length=200)
	state = forms.CharField(max_length=200)
	pincode = forms.IntegerField()
	image = forms.ImageField()

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if(len(phone)<10):
			raise ValidationError("phone number must be 10 digits!")
		return phone

	def clean_pincode(self):
		pincode = self.cleaned_data.get('pincode')
		if(len(str(pincode))<6):
			raise ValidationError("pin code must be 6 digits!")
		return pincode

class StudentCourseRegistrationForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all())
	subject = forms. ModelMultipleChoiceField(queryset=Subject.objects.all())


class TeacherSubjectRegistrationForm(forms.Form):
	subject = forms.ModelChoiceField(queryset=Subject.objects.all())

	def clean_subject(self):
		subject = self.cleaned_data.get('subject')
		if TeacherSubjectRegistration.objects.filter(subject = subject).exists():
			raise ValidationError("you can not take this subject subject is already taken!")
		return subject


from django.forms import TextInput , EmailInput	

class SignUpForm(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=200)
	username = forms.CharField(max_length=200)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget = forms.PasswordInput())
	confirm_password=forms.CharField(widget=forms.PasswordInput())

	

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')
		if(len(first_name)<=3):
			raise ValidationError("first_name must be more than 3 character!")
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name')
		if(len(last_name)<=3):
			raise ValidationError("last_name must be more than 3 character!")
		return last_name

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).exists():
			raise ValidationError("This email id already taken you can not use this email id!")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise ValidationError("Username must be unique! You can use difrent username!")
		return username

	def clean_confirm_password(self):
		clean_data = self.cleaned_data
		password = clean_data.get('password')
		confirm_password = clean_data.get('confirm_password')
		
		if(password!=confirm_password):
			raise ValidationError("password does not match")
		return confirm_password
	
	
class LoginForm(forms.Form):
	
	username = forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),max_length=200)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'30'}))


	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			return username
		raise ValidationError("Your username is wrong!")
	
	def clean_password(self):
		clean_data = self.cleaned_data
		username = clean_data.get('username')
		password = clean_data.get('password')
		if User.objects.filter(username=username).exists():
			user = User.objects.get(username=username)
			if check_password(password,user.password):
				return password	
			raise ValidationError("Your password is wrong!")
			
		
class AttendanceForm(forms.Form):
	STATUS_CHOICE = (
			('persent','Persent'),
			('absent','Absent'),
		)
	date = forms.DateField(initial=timezone.now())
	student = forms.ModelChoiceField(queryset=StudentCourseRegistration.objects.all())
	status = forms.ChoiceField(choices=STATUS_CHOICE)


class LeaveForm(forms.Form):
	leave_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
	leave_message = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20}))
	
class FeedbackForm(forms.Form):
	feedback_message = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20}))

	widgets = {
		 
		 'feedback_message' : forms.TextInput(attrs={'class':'form-control'}),
		 
		 }

class ResultForm(forms.Form):
	student = forms.ModelChoiceField(queryset=StudentCourseRegistration.objects.all())
	marks = forms.FloatField()



class UserUpdateForm(forms.Form):
	GENDER = (
			('MALE','male'),
			('FEMALE','female'),
		)
	ROLE_CHOICE = (
			('STUDENT','student'),
			('TEACHER','teacher'),
			('ADMIN','admin'),
			
		)
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	username = forms.CharField(max_length=200)
	email = forms.EmailField(required=True)
	role = forms.ChoiceField(choices=ROLE_CHOICE)
	gender = forms.ChoiceField(choices=GENDER)
	phone = forms.CharField(max_length=20)
	street = forms.CharField(max_length=200)
	city = forms.CharField(max_length=200)
	state = forms.CharField(max_length=200)
	pincode = forms.IntegerField()
	image = forms.ImageField()
