from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models.fields import URLField
from django.core.validators import URLValidator
from django.contrib.auth.hashers import make_password , check_password
from .models import UserProfile, Course, Subject, Leave, Feedback, Student ,Teacher, Attendance, Result
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail 
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='user-detail',read_only=True)
	#first_name = serializers.CharField(max_length=20 )
	#last_name = serializers.CharField(max_length=200 )
	#username = serializers.CharField(max_length=200 )
	#email = serializers.EmailField(required=True )
	password = serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'Password'})
	confirm_password=serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'ConfirmPassword'})
	
	class Meta:
		model = User
		fields = ['url','first_name','last_name','email' ,'username', 'password','confirm_password']
		
	def validate_email(self,email):
		user = User.objects.filter(email=email).first()
		if user:
			raise serializers.ValidationError("This email id already taken you can not use this email id!")
		return email

	def validate_username(self,username):
		user = User.objects.filter(username=username).first()
		if user:
			raise serializers.ValidationError("Username must be unique! You can use difrent username!")
		return username
	
	def validate(self,data):
		password = data.get('password')
		confirm_password = data.get('confirm_password')
		if(password!=confirm_password):
			raise serializers.ValidationError("password does not match")
		return data
	
	def create(self,validated_data):
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		email=validated_data['email']
		username=validated_data['username']
		password = validated_data['password']
		return User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
	
	def update(self,instance,validated_data):
		instance.first_name=validated_data.get('first_name',instance.first_name)
		instance.last_name=validated_data.get('last_name',instance.last_name)
		instance.username=validated_data.get('username',instance.username)
		instance.email=validated_data.get('email',instance.email)
		instance.set_password(validated_data.get('password',instance.password))
		instance.save()
		return instance

 

class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'Old Password'})
	new_password = serializers.CharField(write_only=True,style={'input_type':'password','placeholder':'New Password'})
	confirm_new_password = serializers.CharField(write_only=True,style={'input_type':'password','placeholder':'Confirm New Password'})		

	def validate_old_password(self,old_password):
		user = self.context.get('user')
		if not check_password(old_password,user.password):
			raise serializers.ValidationError("Old password is wrong!")
		return old_password

	def validate(self,data):
		new_password = data.get('new_password')
		confirm_new_password = data.get('confirm_new_password')
		if(new_password!=confirm_new_password):
			raise serializers.ValidationError("New password and confirm new password do not match!")
		return data


class UserProfileSerializer(serializers.ModelSerializer):
	ROLE_CHOICE = (
			('student','student'),
			('teacher','teacher'),	
		)
	GENDER = (
			('male','male'),
			('female','female'),
		)
	
	profile_url = serializers.HyperlinkedIdentityField(view_name='management:user-profile-detail',read_only=True)
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	#role = serializers.ChoiceField(choices=ROLE_CHOICE)
	#gender = serializers.ChoiceField(choices=GENDER)
	#phone = serializers.CharField(max_length=20)
	#street = serializers.CharField(max_length=20)
	#city = serializers.CharField(max_length=20)
	#state = serializers.CharField(max_length=200)
	#pin_code = serializers.IntegerField()
	#image = serializers.ImageField()

	class Meta:
		model = UserProfile
		fields = ['profile_url','user','role','gender','phone','street','city','state','pin_code','image']
	
	def validate_phone(self,phone):
		if ((len(phone)>12) & ('+91' in phone)):
			return phone
		raise serializers.ValidationError("please enter a valid phone number! +91xxxxxxxxxx")
	def validate_pin_code(self,pin_code):
		if(len(str(pin_code))!=6):
			raise serializers.ValidationError("pincode must be 6 digits! ")
		return pin_code

class CourseSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='management:course-detail')
	class Meta:
		model = Course
		fields = ['url','name','description','fees','duration']

class SubjectSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='management:subject-detail')
	course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
	class Meta:
		model = Subject
		fields = ['url','course','name','description']

class LeaveSerializer(serializers.ModelSerializer):
	ROLE_CHOICE = (
			('student','student'),
			('teacher','teacher'),	
		)
	url = serializers.HyperlinkedIdentityField(view_name='management:leave-detail')
	role = serializers.ChoiceField(choices=ROLE_CHOICE)
	class Meta:
		model = Leave
		fields = ['url','user','role','leave_date','leave_message','leave_status']
		read_only_fields = ['leave_status']

    
class FeedbackSerializer(serializers.Serializer):
	'''
	ROLE_CHOICE = (
			('student','student'),
			('teacher','teacher'),	
		)
	'''
	url = serializers.HyperlinkedIdentityField(view_name='management:feedback-detail')
	user = serializers.PrimaryKeyRelatedField(source='user.username',read_only=True)
	role = serializers.CharField(max_length=100,read_only=True)
	feedback_message = serializers.CharField(style={'base_template': 'textarea.html'})
	feedback_reply = serializers.CharField(max_length=200,read_only=True)
	
	'''
	class Meta:
		model = Feedback
		fields = ['url','user','role','feedback_message','feedback_reply']
		read_only_fields = ['feedback_reply','role',user]
	'''
	def create(self,validated_data):
		user = self.context.get('user')
		feedback_message = validated_data['feedback_message']
		role = user.userprofile.role
		return Feedback.objects.create(user=user,role=role,feedback_message=feedback_message)

	def update(self,instance,validated_data):
		instance.feedback_message = validated_data.get('feedback_message',instance.feedback_message)
		instance.save()
		return instance

class AttendanceSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='management:attendance-detail')
	students = serializers.PrimaryKeyRelatedField(source='students.user.first_name',queryset=Student.objects.all())
	subjects = serializers.PrimaryKeyRelatedField(source='subjects.name',queryset=Subject.objects.all())
	class Meta:
		model = Attendance
		fields = ['url','students','subjects','date','status']

class ResultSerializer(serializers.Serializer):
	url = serializers.HyperlinkedIdentityField(view_name='management:result-detail')
	students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
	subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
	marks = serializers.FloatField(default=0)
	
	
	def create(self,validated_data):
		user = self.context.get('user')
		subjects = validated_data['subjects']
		students = validated_data['students']
		marks = validated_data['marks']
		return Result.objects.create(teacher=user.first_name,subjects=subjects,students=students,marks=marks)

	def update(self,instance,validated_data):
		instance.subjects = validated_data.get('subjects',instance.subjects)
		instance.students = validated_data.get('students',instance.students)
		instance.marks = validated_data.get('marks',instance.marks)
		instance.save()
		return instance
		

class StudentSerializer(serializers.Serializer):
	#url = serializers.HyperlinkedIdentityField(view_name='management:student-detail')
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(userprofile__role='student'))
	course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
	subjects =serializers.PrimaryKeyRelatedField(style={'base_template':'checkbox_multiple.html'},many=True, queryset=Subject.objects.all())
	'''
	class Meta:
		model = Student
		fields = ['user','course','subjects']
	'''
	def validate_user(self,user):
		student = Student.objects.filter(user=user).first()
		if student:
			raise serializers.ValidationError("Student is already reagistered!")
		return user

	def create(self,validated_data):
		user = validated_data['user']
		course = validated_data['course']
		subjects = validated_data['subjects']
		student = Student.objects.create(user=user,course=course)
		student.subjects.set(subjects)
		student.save()
		return student

	def update(self,instance,validated_data):
		instance.user = validated_data.get('user',instance.user)
		instance.course = validated_data.get('course',instance.course)
		instance.subjects.set(validated_data.get('subjects',instance.subjects))
		instance.save()
		return instance
		
class TeacherSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='management:teacher-detail')
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(userprofile__role='teacher'),validators=[UniqueValidator(queryset=Teacher.objects.all(),message='Teacher is already reagistered')])
	class Meta:
		model = Teacher
		fields = ['url','user','course','subjects']


class ContactSerializer(serializers.Serializer):
	name = serializers.CharField()
	email = serializers.EmailField()
	message = serializers.CharField()

	def save(self):
		name = self.validated_data['name']
		email = self.validated_data['email']
		message = self.validated_data['message']
		email_from = settings.EMAIL_HOST_USER
		subject = "contact"
		send_mail(subject,message,email_from,[email])


from django_filters import FilterSet, AllValuesFilter

class AttendanceFilter(FilterSet):
	students = AllValuesFilter(field_name='students__user__first_name')
	subjects = AllValuesFilter(field_name='subjects__name')
	class Meta:
		model = Attendance
		fields=(
  		'students',
  		'subjects'
  		)