from django.db import models
from django.urls import reverse

# Create your models here.
from django.contrib.auth.models import User,  AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Course(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	fees = models.IntegerField()
	duration = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	course = models.ForeignKey(Course,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	GENDER = (
			('male','male'),
			('female','female'),
		)
	ROLE_CHOICE = (
			('student','student'),
			('teacher','teacher'),	
		)
	role = models.CharField(max_length=10, choices=ROLE_CHOICE,null=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	gender = models.CharField(max_length=10,choices=GENDER,null=True)
	phone = models.CharField(max_length=20,null=True)
	street = models.CharField(max_length=200,null=True)
	city = models.CharField(max_length=200,null=True)
	state = models.CharField(max_length=200,null=True)
	pin_code = models.IntegerField(null=True)
	image = models.ImageField(upload_to='uploads/student_images',null=True)

	def __str__(self):
		return self.user.username

class Registration(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	subjects = models.ManyToManyField(Subject)

	class Meta:
		abstract = True

class Student(Registration):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name

class Teacher(Registration):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	students = models.ManyToManyField(Student,through='TeacherStudent')
	
	def __str__(self):
		return self.user.first_name

class TeacherStudent(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

	
	def __str__(self):
		return '%s / %s'%(self.teacher,self.student)
	

class Attendance(models.Model):
	STATUS_CHOICE = (
			('persent','persent'),
			('absent','absent'),
		)
	teacher = models.ForeignKey(User,on_delete=models.CASCADE)
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	subjects = models.ForeignKey(Subject,on_delete=models.CASCADE)
	date = models.DateField()
	students = models.ForeignKey(Student,on_delete=models.CASCADE)
	status = models.CharField(max_length=10,choices=STATUS_CHOICE)

	def __str__(self):
		return self.teacher.username

class Result(models.Model):
	teacher = models.CharField(max_length=100)
	subjects = models.ForeignKey(Subject,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	students = models.ForeignKey(Student,on_delete=models.CASCADE)
	marks = models.FloatField(default=0)


class Leave(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	role = models.CharField(max_length=10)
	leave_date = models.DateField()
	leave_message = models.CharField(max_length=200)
	leave_status = models.BooleanField(default=False)

class Feedback(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	role = models.CharField(max_length=10)
	feedback_message= models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	feedback_reply=models.CharField(max_length=100)





	



