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

class CourseRegistration(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	subjects = models.ManyToManyField(Subject)

class StudentCourseRegistration(CourseRegistration,models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username
	
	
class TeacherSubjectRegistration(CourseRegistration,models.Model):
	students = models.ManyToManyField(StudentCourseRegistration,null=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


class Attendance(models.Model):
	STATUS_CHOICE = (
			('persent','persent'),
			('absent','absent'),
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
	leave_status = models.BooleanField(default=False)

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



	



