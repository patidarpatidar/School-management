from django.forms import ModelForm
from django.conf import settings
from django import forms
from .models import UserProfile ,Leave ,  Course ,Attendance,Subject,StudentCourseRegistration,TeacherSubjectRegistration

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
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

	role = forms.ChoiceField(choices=ROLE_CHOICE ,widget=forms.Select(attrs={'class':'form-control'}))
	gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=20 ,widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(max_length=200 , widget=forms.TextInput(attrs={'class':'form-control'}))
	city = forms.CharField(max_length=200 , widget=forms.TextInput(attrs={'class':'form-control'}))
	state = forms.CharField(max_length=200 , widget=forms.TextInput(attrs={'class':'form-control'}))
	pincode = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

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
	course = forms.ModelChoiceField(queryset=Course.objects.all(),empty_label=None,widget=forms.Select(attrs={'style': 'width:250px'}))
	subject = forms. ModelMultipleChoiceField(queryset=Subject.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'style':'width:15px'}))


class TeacherSubjectRegistrationForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all(),empty_label=None,widget=forms.Select(attrs={'style': 'width:250px'}))
	subject = forms.ModelChoiceField(queryset=Subject.objects.all(),empty_label=None,widget=forms.Select(attrs={'style': 'width:250px'}))

	def clean_subject(self):
		course = self.cleaned_data.get('course')
		subject = self.cleaned_data.get('subject')
		if TeacherSubjectRegistration.objects.filter(subject = subject,course=course).exists():
			raise ValidationError("inside this course subject teacher is already you can not register!")
		return subject


from django.forms import TextInput , EmailInput	

class SignUpForm(forms.Form):
	first_name = forms.CharField(max_length=20 , widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=200 , widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(max_length=200 , widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

	

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
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=200)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


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
	
	def __init__(self ,teacher, *args,**kwargs):
		self.teacher = kwargs.pop('teacher',None)
		super(AttendanceForm,self).__init__(*args,**kwargs)
		self.fields['student'].queryset=StudentCourseRegistration.objects.filter(subject=teacher.subject,course=teacher.course)
		
	STATUS_CHOICE = (
			('persent','Persent'),
			('absent','Absent'),
		)
	date = forms.DateField(initial=timezone.now() , widget=forms.DateInput(attrs={'style':'width:250px;'
        }))
	student = forms.ModelChoiceField(queryset=None,empty_label=None,widget=forms.Select(attrs={'style': 'width:250px'}))
	status = forms.ChoiceField(choices=STATUS_CHOICE,widget=forms.Select(attrs={'style': 'width:250px'}))


	'''
	def clean_student(self):
		student = self.cleaned_data.get('student')
		if Attendance.objects.filter(student=student,date=datetime.date.today()).exists():
			raise ValidationError("this student attendace already taken!")
		return student		
	'''
	
class LeaveForm(forms.Form):
	leave_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
	leave_message = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20}))
	
	
class FeedbackForm(forms.Form):
	feedback_message = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':20}))

	widgets = {
		 
		 'feedback_message' : forms.TextInput(attrs={'class':'form-control'}),
		 
		 }

class ResultForm(forms.Form):
	def __init__(self ,teacher, *args,**kwargs):
		self.teacher = kwargs.pop('teacher',None)
		super(ResultForm,self).__init__(*args,**kwargs)
		print(teacher.subject)
		self.fields['student'].queryset=StudentCourseRegistration.objects.filter(subject=teacher.subject,course=teacher.course)
	student = forms.ModelChoiceField(queryset=None,empty_label=None,widget=forms.Select(attrs={'style': 'width:250px'}))
	marks = forms.FloatField(widget=forms.TextInput(attrs={'style':'width:250px;'}))



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

class ChangePasswordform(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	