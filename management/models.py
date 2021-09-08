from django.db import models
from django.urls import reverse

# Create your models here.
from django.contrib.auth.models import User,  AbstractUser

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
			('MALE','male'),
			('FEMALE','female'),
		)
	ROLE_CHOICE = (
			('STUDENT','student'),
			('TEACHER','teacher'),
			('ADMIN','admin')
			
		)
	role = models.CharField(max_length=10, choices=ROLE_CHOICE)
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	gender = models.CharField(max_length=10,choices=GENDER)
	phone = models.CharField(max_length=20)
	street = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	pin_code = models.IntegerField()
	image = models.ImageField(upload_to='uploads/student_images')

	def __str__(self):
		return self.user.username

class StudentCourseRegistration(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	subject = models.ManyToManyField(Subject)

	def __str__(self):
		return self.user.username
		
class TeacherSubjectRegistration(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	subject = models.OneToOneField(Subject,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username

class Attendance(models.Model):
	STATUS_CHOICE = (
			('persent','Persent'),
			('absent','Absent'),
		)
	teacher = models.ForeignKey(User,on_delete=models.CASCADE)
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
	date = models.DateField()
	student = models.ForeignKey(StudentCourseRegistration,on_delete=models.CASCADE)
	status = models.CharField(max_length=10,choices=STATUS_CHOICE)

	def __str__(self):
		return self.teacher.username

class Leave(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	role = models.CharField(max_length=10)
	leave_date = models.DateField()
	leave_message = models.CharField(max_length=200)
	leave_status = models.IntegerField(default=0)

class Feedback(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	role = models.CharField(max_length=10)
	feedback_message= models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	feedback_reply=models.CharField(max_length=100)

class Result(models.Model):
	teacher = models.CharField(max_length=100)
	subject = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	student = models.ForeignKey(StudentCourseRegistration,on_delete=models.CASCADE)
	marks = models.FloatField(default=0)



	



