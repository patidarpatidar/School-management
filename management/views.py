from django.shortcuts import render,get_object_or_404 , HttpResponse , redirect , HttpResponseRedirect
from .models import Course,Subject ,UserProfile,TeacherStudent,Student, Teacher , Attendance , Leave , Feedback , Result
from .forms import  SignUpForm ,SendEmailForm,ForgotPasswordForm,AttendanceFilter, LoginForm ,ChangePasswordform,UserUpdateForm ,UserProfileForm ,CourseRegistrationForm ,ResultForm , AttendanceForm , LeaveForm , FeedbackForm
from django.contrib.auth import login,logout, authenticate
# Create your views here.

from django.contrib.auth.hashers import check_password ,make_password
from django.db.models import Q
from .decorator import teacher_required,student_required,role_required
import datetime 
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail 
from django.conf import settings
from django.template.loader import render_to_string

from .signals import send_signup_email
from django.db.models.signals import post_save
#-----------------------------User permission function (common)-----------------------------------
#------------------------------------------------------------------------------------->


from .serializers import *
from django.http import JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser,FileUploadParser
from rest_framework.decorators import api_view , permission_classes,action
from rest_framework import permissions , status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import mixins , generics,filters
from .permissions import IsSuperUser ,IsTeacher
from  rest_framework import authentication
#import django_filters.rest_framework


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filterset_fields = ['username','first_name']
	#parser_classes = [JSONParser,FormParser]
	
	@action(methods=['put'],detail=True,url_path='change-password',url_name='change-password',serializer_class=ChangePasswordSerializer,permission_classes=[permissions.IsAuthenticated])
	def change_password(self,request,pk=None):
		user = User.objects.get(pk=pk)
		if request.user.pk==user.pk :
			serializer = ChangePasswordSerializer(data=request.data,context = {'user':user})
			if serializer.is_valid():
				new_password = serializer.validated_data['new_password']
				user.set_password(new_password)
				user.save()
				return Response({'msg':'password change successfully!'},status=status.HTTP_200_OK)
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		return Response({'msg':'you can not change this password!'},status=status.HTTP_400_BAD_REQUEST)


class UserProfileList(generics.ListCreateAPIView):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = UserProfile
	serializer_class = UserProfileSerializer

class CourseList(generics.ListCreateAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAdminUser]

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Course
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAdminUser]

class SubjectList(generics.ListCreateAPIView):
	queryset =Subject.objects.all()
	serializer_class = SubjectSerializer
	permission_classes = [permissions.IsAdminUser]

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset =Subject
	serializer_class = SubjectSerializer
	permission_classes = [permissions.IsAdminUser]

class LeaveList(generics.ListCreateAPIView):
	queryset = Leave.objects.all()
	serializer_class = LeaveSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LeaveDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Leave
	serializer_class = LeaveSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FeedbackList(generics.ListCreateAPIView):
	queryset = Feedback.objects.all().order_by('-id')
	serializer_class = FeedbackSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def post(self,request):
		serializer = FeedbackSerializer(data=request.data,context={'user':request.user})
		if serializer.is_valid():
			serializer.save()
			return Response({'msg':'feedback send'},status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Feedback
	serializer_class = FeedbackSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AttendanceList(generics.ListAPIView):
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer
	permission_classes = [permissions.IsAuthenticated]
	filterset_fields = ['students','subjects','date']
	#filter_backends = [filters.OrderingFilter]
	#ordering_fields = ['students','subjects','date']

class AttendanceDetail(generics.RetrieveDestroyAPIView):
	queryset = Attendance
	permission_classes = [IsTeacher]
	serializer_class = AttendanceSerializer

class ResultList(generics.ListCreateAPIView):
	queryset = Result.objects.all()
	serializer_class = ResultSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def post(self,request):
		serializer = ResultSerializer(data=request.data,context={'user':request.user})
		
		if serializer.is_valid():
			serializer.save()
			return Response({'msg':'Result add succsefully!'},status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Result
	serializer_class = ResultSerializer
	permission_classes = [IsTeacher]

class StudentList(generics.ListCreateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Student
	serializer_class = StudentSerializer

class TeacherList(generics.ListCreateAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Teacher
	serializer_class = TeacherSerializer









def delete_selected_attendance(request):
	if request.method=="POST":
		attendance_ids = request.POST.getlist('attendance')
		for id in attendance_ids:
			Attendance.objects.get(pk=id).delete()
		msg = messages.success(request,"successfully")
		return redirect('management:attendance-record')


def fetch_subject(request,id):
	subjects = Subject.objects.filter(course_id=id)
	return render(request,'management/fetch_subject.html',{'subjects':subjects})


def send_forgot_password_email(request):
	if request.method=="POST":
		form = SendEmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = User.objects.filter(email=email)
			if user.exists():
				# Email sending for password reset .
				user = user.first()
				template_name = "management/password_reset_email.txt"
				domain = settings.DOMAIN
				subject = "Password reset instructions link."	
				#import pdb; pdb.set_trace();			
				message = domain + reverse('management:forgot-password')
				email_from = settings.EMAIL_HOST_USER
				send_mail(subject,message,email_from,[email],fail_silently=False)
				messages.success(request,"Password reset instructions have been sent successfully via email.")
				return HttpResponseRedirect(reverse('management:password-reset-email-done'))		
	else:	
		form = SendEmailForm()
	return render(request,'management/send_forgot_password_email.html',{'form':form})

def password_reset_email_done(request):
	return render(request,"management/password_reset_email_done.html")

def forgot_password(request):
	if request.method=='POST':
		form = ForgotPasswordForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']  
			password = form.cleaned_data['new_password']
			confirm_password = form.cleaned_data['confirm_new_password']
			user = User.objects.get(username=username)
			if user.exists():
				user.set_password(password)
				user.save()
				messages.success(request,"your password reset successfully!")
				return HttpResponseRedirect(reverse('management:password-reset-done'))	
	else:	
		form = ForgotPasswordForm()
	return render(request,'management/forgot_password.html',{'form':form})

def password_reset_done(request):
	return render(request,"management/password_reset_done.html")


def fetch_student(request,id):
	subject = Subject.objects.filter(id=id)
	students = Student.objects.filter(subjects__in=subject)
	return render(request,'management/fetch_student.html',{'students':students})


def fetch_student_result(request,id):
	teacher = request.user.teacher
	results = Result.objects.filter(subjects_id=id).order_by('-id')
	paginator = Paginator(results,4)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'management/fetch_student_result.html',{'page_obj':page_obj})

def fetch_student_attendance(request,id):
	teacher = request.user.teacher
	today = datetime.date.today()
	student =Student.objects.filter(subjects__id=id).order_by('-id')
	subject = Subject.objects.get(pk=id)
	attendance = Attendance.objects.filter(date=today,teacher=teacher.user,subjects=subject)
	take_attendance = []
	for i in attendance:
		take_attendance.append(i.students)
	paginator = Paginator(student,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'management/fetch_student_attendance.html',{'today':today,'page_obj':page_obj,'subject':subject,'take_attendance':take_attendance,'teacher':teacher})


def index_view(request):
	course = Course.objects.all().order_by('-id')
	paginator = Paginator(course,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'management/index.html',{'page_obj':page_obj,'total':course.count()})

@login_required(login_url='/management/login/')
def user_profile_create(request):
	user = request.user
	if request.method == 'POST':
		form = UserProfileForm(request.POST,request.FILES)
		if form.is_valid():
			clean_data = form.cleaned_data
			role = clean_data['role']
			gender = clean_data['gender']
			phone = clean_data['phone']
			street = clean_data['street']
			city = clean_data['city']
			state = clean_data['state']
			pin_code = clean_data['pincode']
			image = clean_data['image']
			user_profile = UserProfile(user=user,role=role,gender=gender,phone=phone,street=street,city=city,state=state,pin_code=pin_code,image=image)
			user_profile.save()
			messages.success(request,"Your profile is complete!")
			return HttpResponseRedirect(reverse('management:user-profile'))
	else:
		form = UserProfileForm()
	return render(request,'management/user_profile_create.html',{'form':form})

@login_required(login_url='/management/login/')
def user_profile_view(request):
	if User.objects.filter(pk=request.user.id,userprofile=None):
		return HttpResponseRedirect(reverse('management:user-profile-create'))	
	else:
		return render(request,'management/user_profile.html',{'user':request.user
		,'userprofile':request.user.userprofile})

@login_required(login_url='/management/login/')
#@role_required
def update_user_detail(request):
	user = request.user
	if request.method=="POST":
		form = UserUpdateForm(request.POST,request.FILES)
		if form.is_valid():
			clean_data = form.cleaned_data
			if len(request.FILES)!=0:
				image=clean_data['image']
			user.first_name=clean_data['first_name']
			user.last_name = clean_data['last_name']
			user.email = clean_data['email']
			user.username = clean_data['username']
			user.userprofile.role = clean_data['role']
			user.userprofile.gender = clean_data['gender']
			user.userprofile.phone = clean_data['phone']
			user.userprofile.street = clean_data['street']	
			user.userprofile.city = clean_data['city']
			user.userprofile.state = clean_data['state']
			user.userprofile.pin_code = clean_data['pincode']
			user.save()
			user.userprofile.save()
			messages.success(request,"profile update successfully")
			return HttpResponseRedirect(reverse('management:user-profile'))

	else:
		user_data = {'first_name':user.first_name,'last_name':user.last_name,'username':user.username,'email':user.email,'role':user.userprofile.role,'gender':user.userprofile.gender,'phone':user.userprofile.phone,'street':user.userprofile.street,'city':user.userprofile.city,'state':user.userprofile.state,'pincode':user.userprofile.pin_code}
		form = UserUpdateForm(initial=user_data)
	return render(request,'management/update_user_detail.html',{'form':form})

@login_required(login_url='/management/login/')
def user_profile_delete(request):
	request.user.userprofile.delete()
	messages.success(request,"successfully deleted!")
	return redirect('management:user-profile')



#-----------------------------Student permission function-----------------------------------
#------------------------------------------------------------------------------------->
	
@login_required(login_url='/management/login/')
def student_course_registration(request):
	if request.method=='POST':
		form = CourseRegistrationForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data['course']
			subjects = form.cleaned_data['subjects']
			teachers = Teacher.objects.filter(course=course,subjects__in=subjects)
			student = Student.objects.create(user=request.user,course=course)
			student.subjects.set(subjects)
			for teacher in teachers:
				if not TeacherStudent.objects.filter(student=student,teacher=teacher):
					TeacherStudent.objects.create(teacher=teacher,student=student)
			messages.success(request,"Your course registration is successfully!")
			return HttpResponseRedirect(reverse('management:course-detail'))
	else:
		courses = Course.objects.all()
		form = CourseRegistrationForm()
	return render(request,"management/course_registration.html",{'form' : form,'courses' :courses})



@login_required(login_url='/management/login/')
def student_course_detail(request):
	student = request.user.student
	teacherstudent = TeacherStudent.objects.filter(student=student)
	return render(request,'management/course_registration_detail.html',{'student':student,'subjects':student.subjects.all,'teacherstudent':teacherstudent})

@login_required(login_url='/management/login/')
@student_required
def update_student_course_registration(request):
	student = request.user.student
	if request.method=="POST":
		form = CourseRegistrationForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data['course']
			subjects = form.cleaned_data['subjects']
			teachers = Teacher.objects.filter(course=course,subjects__in=subjects)
			student.course= course
			student.subjects.set(subjects)
			TeacherStudent.objects.filter(student=student).delete()
			for teacher in teachers:
				if not TeacherStudent.objects.filter(student=student,teacher=teacher):
					TeacherStudent.objects.create(teacher=teacher,student=student)
			student.save()
			messages.success(request,"registration detail update successfully")
			return HttpResponseRedirect(reverse('management:course-detail'))
	else:
		form = CourseRegistrationForm(initial={'course':student.course,'subjects':student.subjects.all})
		courses = Course.objects.all()
		subjects = Subject.objects.filter(course=student.course)
	return render(request,'management/update_course_registration.html',{'form':form,'courses':courses,'subjects':subjects})


@login_required(login_url='/management/login/')
def delete_student_course_registration(request):
	request.user.student.delete()
	messages.success(request,"successfully deleted!")
	return redirect('/management/user-profile')


@login_required(login_url='/management/login/')
def attendance_view(request):
	student = request.user.student
	subjects = student.subjects.all()
	attendance = Attendance.objects.filter(students_id=student.id,subjects__in=subjects)
	paginator = Paginator(attendance,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	if len(attendance)!=0:
		persent = 0
		absent = 0
		for i in attendance:
			if i.status=='persent':
				persent+=1
			else:
				absent+=1
		return render(request,'management/attendance_view.html',{'page_obj':page_obj,'persent':persent,'absent':absent,'student':student})
	else:
		messages.info(request,"You have not attend any class so you have not  any attendance record!")
		return redirect('/management/user-profile')

@login_required(login_url='/management/login/')
def result_view(request):
	student = request.user.student
	subjects = student.subjects.all()
	result = Result.objects.filter(students_id=student.id,subjects__in=subjects)
	return render(request,'management/view_result.html',{'results':result,'student':student,'subjects':student.subjects.all})

#-----------------------------Teacher permission function-----------------------------------
#------------------------------------------------------------------------------------->

@login_required(login_url='/management/login/')
def teacher_course_registration(request):
	if request.method=='POST':
		form = CourseRegistrationForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data['course']
			subjects = form.cleaned_data['subjects']
			students = Student.objects.filter(course=course,subjects__in=subjects)		
			teacher_obj = Teacher.objects.create(course=course,user=request.user)
			teacher_obj.subjects.set(subjects)

			for student in students:
				if not TeacherStudent.objects.filter(student=student,teacher=teacher_obj):
					TeacherStudent.objects.create(teacher=teacher_obj,student=student)
			messages.success(request,"Your have successfully register!")
			return HttpResponseRedirect(reverse('management:teacher-subject-detail'))
	else: 
		return render(request,'management/course_registration.html',{'form' : CourseRegistrationForm(),'courses' :Course.objects.all(),
		})

@login_required(login_url='/management/login/')
def teacher_course_detail(request):
	teacher = request.user.teacher
	total_student = teacher.students.count()	
	return render(request,'management/teacher_subject_detail.html',{'total_student':total_student,'teacher':teacher,'subjects':teacher.subjects.all
	})

@login_required(login_url='/management/login/')
@teacher_required
def update_teacher_course_registration(request):
	teacher = request.user.teacher
	if request.method=="POST":
		form = CourseRegistrationForm(request.POST)
		if form.is_valid():
			subjects = form.cleaned_data['subjects']
			course = form.cleaned_data['course']
			students = Student.objects.filter(course=course,subjects__in=subjects)
			TeacherStudent.objects.filter(teacher=teacher).delete()
			teacher.course = course
			teacher.subjects.set(subjects)
			for student in students:
				if not TeacherStudent.objects.filter(student=student,teacher=teacher):
					TeacherStudent.objects.create(teacher=teacher,student=student)	
			teacher.save()
			messages.success(request,"udate your subject registration!")
			return HttpResponseRedirect(reverse('management:teacher-subject-detail'))
	else:
		form = CourseRegistrationForm(initial = {'course':teacher.course,'subjects':teacher.subjects.all,
		})
	return render(request,'management/update_course_registration.html',{'form' : form,'courses':Course.objects.all(),'subjects':Subject.objects.filter(course=teacher.course)})

@login_required(login_url='/management/login/')
def delete_course_registration(request):
	request.user.teacher.delete()
	messages.success(request,"successfully deleted")
	return redirect('/management/user-profile')

@login_required(login_url='/management/login/')
@teacher_required
def take_attendance(request):
	teacher = request.user.teacher
	form = AttendanceForm(teacher)
	return render(request,'management/take_attendance.html',{'form':form,'teacher':teacher,'subjects':teacher.subjects.all})


@login_required(login_url='/management/login/')
def attendance_persent(request,id,subject):
	teacher = request.user.teacher
	subject = Subject.objects.get(name=subject)
	teacher = request.user.teacher
	student = Student.objects.get(pk=id)
	today = datetime.date.today()
	Attendance.objects.create(teacher=teacher.user,students=student,date=today,status='persent',course=teacher.course,subjects=subject)

	form = AttendanceForm(teacher)
	messages.success(request,"attendance add successfully!")
	return render(request,'management/take_attendance.html',{'form':form,'teacher':teacher,'subjects':teacher.subjects.all,'subject_value':subject})


@login_required(login_url='/management/login/')
def attendance_absent(request,id,subject):
	subject = Subject.objects.get(name=subject)
	teacher = request.user.teacher
	student = Student.objects.get(pk=id)
	today = datetime.date.today()
	Attendance.objects.create(teacher=teacher.user,students=student,date=today,status='absent',course=teacher.course,subjects=subject)
	messages.success(request,"attendance add successfully!")
	return HttpResponseRedirect(reverse('management:take-attendance'))

def filter_attendance(request,student_id,subject_id,date,short):
	if date:
		date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	else:
		date=None
	if subject_id and student_id and date:
		return Attendance.objects.filter(Q(students__id=student_id) & Q(subjects__id=subject_id) & Q(date=date) & Q(teacher=request.user)).order_by('-id')
	elif subject_id and date :
		return Attendance.objects.filter(Q(subjects__id=subject_id) & Q(date=date) & Q(teacher_id=request.user.id)).order_by('-id')
	elif (student_id  and (subject_id or date)):
		return Attendance.objects.filter(Q(students__id=student_id) & (Q(subjects__id=subject_id) | Q(date=date)) & Q(teacher_id=request.user.id)).order_by('-id')
	elif student_id or subject_id or date:
		return Attendance.objects.filter((Q(subjects__id=subject_id) | Q(date=date) | Q(students__id=student_id)) & Q(teacher_id=request.user.id)).order_by('id')
	elif short=='today':
		return Attendance.objects.filter(teacher_id=request.user.id,date=datetime.date.today()).order_by('-id')
	else:
		return Attendance.objects.filter(teacher_id=request.user.id).order_by('-date')


@login_required(login_url='/management/login/')
def attendance_record(request):
	teacher = request.user.teacher
	date = request.GET.get('date')
	subject_id = request.GET.get('subjects')
	student_id = request.GET.get('students')
	if student_id=='':student_id=None;
	if subject_id=='':subject_id=None;
	short = request.GET.get('short', None)
	form = AttendanceFilter(teacher,initial={'students':student_id,'subjects':subject_id,'date':date,'short':short})
	attendance = filter_attendance(request,student_id,subject_id,date,short)
	paginator = Paginator(attendance,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'management/attendance_record.html',{'form':form,'page_obj':page_obj,'teacher':teacher,'subjects':teacher.subjects.all,'students':teacher.students.all,
	})


@login_required(login_url='/management/login/')
def update_attendance_record(request,id):
	attendance = Attendance.objects.get(pk=id)
	teacher = request.user.teacher
	if request.method=="POST":
		form = AttendanceForm(teacher,request.POST)
		if form.is_valid():
			attendance.subjects = form.cleaned_data['subjects']
			attendance.date = form.cleaned_data['date']
			attendance.students = form.cleaned_data['students']
			attendance.status = form.cleaned_data['status']
			attendance.save()
			messages.success(request,"attendance update successfully!")
			return HttpResponseRedirect(reverse('management:attendance-record'))
	else:
		form = AttendanceForm(teacher,initial={
			'subjects':attendance.subjects,'date':attendance.date,'students':attendance.students,'status':attendance.status,
		} )
		return render(request,'management/attendance_update.html',{'attendance':attendance,'form':form,'teacher':teacher,'subjects':teacher.subjects.all,'students':teacher.students.all
		})



@login_required(login_url='/management/login/')
def delete_attendance_record(request,id):
	Attendance.objects.get(pk=id).delete()
	
	
	custom_signal.send(sender=request.user,initial=id,kwargs={'name':'rajmal'})
	notification.send(sender=request.user,request=request,user={'rajmal'})
	
	messages.success(request,"attendance delete successfully")
	return redirect('/management/attendance-record')

def delete_all_attendance(request):
	Attendance.objects.filter(teacher_id=request.user.id).delete()
	messages.success(request,"deleted successfully!")
	return redirect('management:attendance-record')

@login_required(login_url='/management/login/')
def result_add(request):
	teacher = request.user.teacher
	if request.method=='POST':
		form = ResultForm(teacher,request.POST)
		if form.is_valid():
			subjects = form.cleaned_data['subjects']
			students = form.cleaned_data['students']
			marks = form.cleaned_data['marks']
			Result.objects.create(teacher=teacher,students=students,marks=marks,subjects=subjects)
			messages.success(request,"result add successfully!")
			return HttpResponseRedirect(reverse('management:add-result'))
		else:
			messages.info(request,"this student result already added!")
			return HttpResponseRedirect(reverse('management:add-result'))
	else:
		return render(request,'management/add_result.html',{'form':ResultForm(teacher),'teacher':teacher,'students':teacher.students.all,'subjects':teacher.subjects.all,
		})

@login_required(login_url='/management/login/')
def update_result(request,id):
	result = Result.objects.get(pk=id)
	teacher = request.user.teacher
	if request.method=="POST":
		form = ResultForm(teacher,request.POST)
		if not form.is_valid():
			result.subjects = form.cleaned_data['subjects']
			result.students = form.cleaned_data['students']
			result.marks = form.cleaned_data['marks']
			result.save()
			messages.success(request,"result update successfully!")
			return HttpResponseRedirect(reverse('management:add-result'))
	else:
		form = ResultForm(teacher,initial={'subjects':result.subjects,'students':result.students,'marks' : result.marks})
		return render(request,'management/update_result.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_result(request,id):
	Result.objects.get(pk=id).delete()
	messages.success(request,"deleted successfully1")
	return redirect('/management/add-result')

def filter_result_information(request,student_id,subject_id,date,short):
	if date:
		date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
	else:
		date=None
	if subject_id and student_id and date:
		return Result.objects.filter(Q(students__id=student_id) & Q(subjects__id=subject_id) & Q(created_at__date=date) & Q(teacher=request.user.first_name)).order_by('-id')
	elif subject_id and date :
		return Result.objects.filter(Q(subjects__id=subject_id) & Q(created_at__date=date) & Q(teacher=request.user.first_name)).order_by('-id')
	elif (student_id  and (subject_id or date)):
		return Result.objects.filter(Q(students__id=student_id) & (Q(subjects__id=subject_id) | Q(created_at__date=date)) & Q(teacher=request.user.first_name)).order_by('-id')
	elif student_id or subject_id or date:
		return Result.objects.filter((Q(subjects__id=subject_id) | Q(created_at__date=date) | Q(students__id=student_id)) & Q(teacher=request.user.first_name)).order_by('id')
	else:
		return Result.objects.filter(teacher=request.user.first_name).order_by('-created_at')

def result_information(request):
	teacher = request.user.teacher
	date = request.GET.get('date')
	subject_id = request.GET.get('subject',None)
	subject = Subject.objects.filter(id=subject_id)
	student_id = request.GET.get('student',None)
	student = Student.objects.filter(id=student_id)
	short = request.GET.get('short',None)
	results = filter_result_information(request,student_id,subject_id,date,short)
	paginator = Paginator(results,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'management/result_information.html',{'page_obj':page_obj,'teacher':teacher,'students':teacher.students.all,'subjects':teacher.subjects.all,'subject_value':subject.first(),'student_value':student.first(),'date':date})

@login_required(login_url='/management/login/')
def delete_result_information(request,id):
	Result.objects.get(pk=id).delete()
	messages.success(request,"deleted successfully!")
	return redirect('/management/result-information')

def update_result_information(request,id):
	result = Result.objects.get(pk=id)
	teacher = request.user.teacher
	if request.method=="POST":
		form = ResultForm(teacher,request.POST)
		if form.is_valid():
			result.subjects = form.cleaned_data['subjects']
			result.students = form.cleaned_data['students']
			result.marks = form.cleaned_data['marks']
			result.save()
			messages.success(request,"result update successfully!")
			return HttpResponseRedirect(reverse('management:result-information'))
	else:
		form = ResultForm(teacher,initial={'subjects':result.subjects,'students':result.students,'marks' : result.marks})
	return render(request,'management/update_result.html',{'form':form})


#------------------------------signup Login logout function---------------------- 
#---------------------------------------------------------------------------------------->


def signup_view(request):
	if request.method=='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			clean_data=form.cleaned_data
			first_name=clean_data['first_name']
			last_name = clean_data['last_name']
			username = clean_data['username']
			email = clean_data['email']
			password = clean_data['password']
			user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
			post_save.connect(send_signup_email)
			messages.success(request,"Thanks for registeration. Please check your email.")
			return HttpResponseRedirect(reverse('management:login'))
	else:
		form = SignUpForm()
	return render(request,'management/signup.html',{'form':form})

   
def login_view(request):
	if request.method=="POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request,username = username , password=password)
			if user is not None:
				login(request,user)
				messages.success(request,f"You have successfully login! Welcome: {user.first_name}")
				nxt = request.GET.get('next',None)
				if nxt is None:
					return redirect('management:user-profile')
				else:
					return redirect(nxt)
				request.session['user']=user

	else:
		form = LoginForm()
	return render(request,'management/login.html',{'form':form})
	

def logout_view(request):
	logout(request)
	messages.success(request,"you have successfully logged out")
	return redirect('management:login')


@login_required(login_url='/management/login/')
def change_password(request):
	user = request.user
	if request.method=="POST":
		form = ChangePasswordform(request.POST)
		if form.is_valid():
			old_password = form.cleaned_data['old_password']
			if check_password(old_password,user.password):
				user.set_password(form.cleaned_data['new_password'])
				user.save()
				messages.success(request,"your password change successfully!")
				return redirect('/management/')
			else:
				messages.info(request,"your old password is wrong!")
				return redirect('management:change-password')
	else:
		form = ChangePasswordform()
	return render(request,'management/change_password.html',{'form':form})

@login_required(login_url='/management/login/')
def apply_leave_view(request):
	if request.method=='POST':
		form = LeaveForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			date = clean_data['leave_date']
			message = clean_data['leave_message']
			Leave.objects.create(user=request.user,role=request.user.userprofile.role,leave_date=date,leave_message=message)
			messages.success(request,"your leave information send successfully . wait for confirm your leave!")
			return HttpResponseRedirect(reverse('management:leave-information'))
	else:
		form = LeaveForm()
		leave_detail = Leave.objects.filter(user_id=request.user.id)
		paginator = Paginator(leave_detail,2)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
	return render(request,'management/leave_information.html',{'page_obj':page_obj,'form':form})

@login_required(login_url='/management/login/')
def update_leave(request,id):
	leave = Leave.objects.get(pk=id)
	if request.method=="POST":
		form = LeaveForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			leave.leave_date =clean_data['leave_date']
			leave.leave_message =clean_data['leave_message']
			leave.save()
			messages.success(request,"leave information update successfully!")
			return redirect('/management/leave-information')
	else:
		form = LeaveForm(initial={'leave_date':leave.leave_date,'leave_message':leave.leave_message})
	return render(request,'management/update_leave.html',{'form':form})


@login_required(login_url='/management/login/')
def delete_leave(request,id):
	Leave.objects.get(pk=id).delete()
	messages.success(request,"leave deleted successfully!")
	return 	redirect('/management/leave-information')

@login_required(login_url='/management/login/')
def feedback_send_view(request):
	user_obj = request.user
	if request.method=="POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data['feedback_message']
			Feedback.objects.create(user=user_obj,role=user_obj.userprofile.role,feedback_message=message,feedback_reply="")
			messages.success(request,"your feedback is send successfully!")
			return HttpResponseRedirect(reverse('management:feedback-information'))
	else:
		form = FeedbackForm()
		feedback_list = Feedback.objects.filter(user_id=user_obj.id)
		paginator = Paginator(feedback_list,3)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
	return render(request,'management/user_feedback.html',{'form':form,'feedback_list':feedback_list,'page_obj':page_obj})

@login_required(login_url='/management/login/')
def update_feedback(request,id):
	feedback = get_object_or_404(Feedback,pk=id)
	if request.method=="POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			feedback.feedback_message=form.cleaned_data['feedback_message']
			feedback.save()
			messages.success(request,"feedback messages update successfully!")
			return redirect('/management/feedback-information')
	else:
		form = FeedbackForm(initial={'feedback_message':feedback.feedback_message})
	return render(request,'management/update_feedback.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_feedback(request,id):
	Feedback.objects.get(pk=id).delete()
	messages.success(request,"feedback deleted successfully!")
	return redirect('/management/feedback-information')

