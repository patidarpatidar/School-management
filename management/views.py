from django.shortcuts import render,get_object_or_404 , HttpResponse , redirect , HttpResponseRedirect
from .models import Course , UserProfile,StudentCourseRegistration, TeacherSubjectRegistration , Attendance , Leave , Feedback , Result
from .forms import  SignUpForm , LoginForm ,UserUpdateForm ,UserProfileForm ,StudentCourseRegistrationForm ,ResultForm, TeacherSubjectRegistrationForm , AttendanceForm , LeaveForm , FeedbackForm
from django.contrib.auth import login,logout, authenticate
# Create your views here.
from django.views.generic.edit import UpdateView , DeleteView

import datetime 
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth.models import User
from django.urls import reverse_lazy



#-----------------------------User permission function (common)-----------------------------------
#------------------------------------------------------------------------------------->
def index_view(request):
	course = Course.objects.all()
	context = {
		'course_list' : course
	} 
	return render(request,'management/index.html',context)

def user_profile_create(request):
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
			pincode = clean_data['pincode']
			image = clean_data['image']
			profile = UserProfile.objects.create(role=role,
									gender=gender,
									user=request.user,
									phone=phone,
									street=street,
									city=city,
									state=state,
									pin_code=pincode,
									image=image,
	
								)
			
			messages.success(request,"Your profile is complete!")
			return HttpResponseRedirect(reverse('management:user-profile'))
	else:
		form = UserProfileForm()
		return render(request,'management/user_profile_create.html',{'form':form})


def user_profile_view(request):
	user_obj = request.user
	if User.objects.filter(pk=user_obj.id,userprofile=None):
		messages.info(request,"first for fill your profile!")
		return HttpResponseRedirect(reverse('management:user-profile-create'))	
	else:
		context = {
			'user':user_obj,
			'profile':user_obj.userprofile,
		}
		return render(request,'management/user_profile.html',context)

def update_user_detail(request):
	user = request.user
	if request.method=="POST":
		form = UserUpdateForm(request.POST,request.FILES)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			
			user.first_name=cleaned_data['first_name']
			user.last_name = cleaned_data['last_name']
			user.email = cleaned_data['email']
			user.username = cleaned_data['username']
			user.userprofile.role = cleaned_data['role']
			user.userprofile.gender = cleaned_data['gender']
			user.userprofile.phone = cleaned_data['phone']
			user.userprofile.street = cleaned_data['street']
			user.userprofile.city = cleaned_data['city']
			user.userprofile.state = cleaned_data['state']
			user.userprofile.pin_code = cleaned_data['pincode']
			user.userprofile.image=cleaned_data['image']
			user.save()
			user.userprofile.save()
			messages.success(request,"profile update successfully")
			return HttpResponseRedirect(reverse('management:user-profile'))
	else:
		user_data = {
		'first_name':user.first_name,
		'last_name':user.last_name,
		'username':user.username,
		'email':user.email,
		'role':user.userprofile.role,
		'gender':user.userprofile.gender,
		'phone':user.userprofile.phone,
		'street':user.userprofile.street,
		'city':user.userprofile.city,
		'state':user.userprofile.state,
		'pincode':user.userprofile.pin_code,
		'image':user.userprofile.image.url,
		}
		print(user_data['image'])
		form = UserUpdateForm(user_data)
	return render(request,'management/update_user_detail.html',{'form':form})


def user_delete(request):
	user = request.user
	user.delete()
	messages.success(request,"successfully deleted!")
	return redirect('/management')

def apply_leave_view(request):
	if request.method=='POST':
		form = LeaveForm(request.POST)
		if form.is_valid():
			date = form.cleaned_data['leave_date']
			message = form.cleaned_data['leave_message']
			Leave.objects.create(user=request.user,role=request.user.userprofile.role,leave_date=date,leave_message=message,leave_status=0)
			messages.success(request,"your leave information send successfully . wait for confirm your leave!")
			return HttpResponseRedirect(reverse('management:leave-information'))
	else:
		form = LeaveForm()
		leave_detail = Leave.objects.filter(user_id=request.user.id)
		context = {
			'leave_detail':leave_detail,
			'form':form
		}
	return render(request,'management/leave_information.html',context)

def update_leave(request,id):
	leave = Leave.objects.get(pk=id)
	
	if request.method=="POST":
		form = LeaveForm(request.POST)
		if form.is_valid():
			leave.leave_date =form.cleaned_data['leave_date']
			leave.leave_message =form.cleaned_data['leave_message']
			leave.save()
			messages.success(request,"leave information update successfully!")
			return redirect('/management/leave-information')
	else:
		leave_data = {
		'leave_date':leave.leave_date,
		'leave_message':leave.leave_message,
		}
		form = LeaveForm(leave_data)
	return render(request,'management/update_leave.html',{'form':form})



def delete_leave(request,id):
	leave = Leave.objects.get(pk=id)
	leave.delete()
	messages.success(request,"leave deleted successfully!")
	return 	redirect('/management/leave-information')

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
		context = {
			'form' : form,
			'feedback_list' : feedback_list,
		}
	return render(request,'management/user_feedback.html',context)

def update_feedback(request,id):
	feedback = get_object_or_404(Feedback,pk=id)
	if request.method=="POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			feedback.feedback_message=form.cleaned_data.get('feedback_message')
			feedback.save()
			messages.success(request,"feedback messages update successfully!")
			return redirect('/management/feedback-information')
	else:
		feedback_data = {
		'feedback_message':feedback.feedback_message
		}
		form = FeedbackForm(feedback_data)
	return render(request,'management/update_feedback.html',{'form':form})

def delete_feedback(request,id):
	feedback = Feedback.objects.get(pk=id)
	feedback.delete()
	messages.success(request,"feedback deleted successfully!")
	return redirect('/management/feedback-information')



#-----------------------------Student permission function-----------------------------------
#------------------------------------------------------------------------------------->
	
def student_course_registration_view(request):
	student_obj = request.user
	if User.objects.filter(pk=student_obj.id,studentcourseregistration=None):
		messages.info(request,"You have not registration any course so first for need course registration!")
		if request.method=='POST':
			form = StudentCourseRegistrationForm(request.POST)
			if form.is_valid():
				course = form.cleaned_data['course']
				subject = form.cleaned_data['subject']
				course_registration = StudentCourseRegistration.objects.create(user=student_obj,course=course)
				course_registration.subject.set(subject)
			
				messages.success(request,"Your course registration is successfully!")
				return HttpResponseRedirect(reverse('management:course-registration-detail'))
		else:
			form = StudentCourseRegistrationForm()
		return render(request,"management/course_registration.html",{'form':form})
	else:
		context = {
			'course_detail' : student_obj.studentcourseregistration
		}

		return render(request,'management/course_registration_detail.html',context)

def update_student_course_registration(request):
	student = request.user.studentcourseregistration
	
	if request.method=="POST":
		form = StudentCourseRegistrationForm(request.POST)
		if form.is_valid():
			student.course=form.cleaned_data['course']
			student.subject.set(form.cleaned_data['subject'])
			student.save()
			messages.success(request,"registration detail update successfully")
			return HttpResponseRedirect(reverse('management:course-registration-detail'))
	else:
		course_data = {
		'course':student.course,
		'subject':student.subject,

		}
		form = StudentCourseRegistrationForm(course_data)
	return render(request,'management/update_course_registration.html',{'form':form})

def delete_student_course_registration(request):
	course = request.user.studentcourseregistration
	course.delete()
	messages.success(request,"successfully deleted!")
	return redirect('/management/user-profile')

def attendance_view(request):
	student_obj = request.user
	attendance = Attendance.objects.filter(student__user__id=student_obj.id)
	if len(attendance)!=0:
		persent = 0
		absent = 0
		for i in attendance:
			if i.status=='P':
				persent+=1
			else:
				absent+=1
		context = {
			'attendance':attendance,
			'persent':persent,
			'absent':absent,
		}
	
		return render(request,'management/attendance_view.html',context)
	else:
		messages.info(request,"You have not attend any class so you have not  any attendance record!")
		return redirect('/management/user-profile')



#-----------------------------Teacher permission function-----------------------------------
#------------------------------------------------------------------------------------->

def teacher_subject_registration_view(request):
	teacher_obj = request.user
	if User.objects.filter(pk=teacher_obj.id,teachersubjectregistration=None):
		messages.info(request,"You have not register for any subjects so need for register!")
		if request.method=='POST':
			form = TeacherSubjectRegistrationForm(request.POST)
			if form.is_valid():
				subject = form.cleaned_data['subject']
				teachersubject = TeacherSubjectRegistration.objects.create(subject=subject,user=teacher_obj)
				
				messages.success(request,"Your have successfully register!")
				return HttpResponseRedirect(reverse('management:teacher-subject'))
		else: 
			form = TeacherSubjectRegistrationForm()
		return render(request,'management/teacher_subject.html',{'form':form})
	else:
		context = {
			'subject_detail':teacher_obj.teachersubjectregistration
		}
		return render(request,'management/teacher_subject_detail.html',context)

def update_subject_registration(request):
	teacher = request.user.teachersubjectregistration
	if request.method=="POST":
		form = TeacherSubjectRegistrationForm(request.POST)
		if form.is_valid():
			teacher.subject = form.cleaned_data['subject']
			teacher.save()
			messages.success(request,"udate your subject registration!")
			return HttpResponseRedirect(reverse('management:teacher-subject'))
	else:
		subject_data = {
			'subject':teacher.subject,
		}
		form = TeacherSubjectRegistrationForm(subject_data)
	return render(request,'management/update_subject_registration.html',{'form':form})

def delete_subject_registration(request):
	teacher = request.user.teachersubjectregistration
	teacher.delete()
	messages.success(request,"successfully deleted")
	return redirect('/management/teacher-subject')

def take_attendance(request):
	teacher_obj = request.user
	if request.method=='POST':
		form = AttendanceForm(request.POST)
		if form.is_valid():
			student = form.cleaned_data['student']
			date = form.cleaned_data['date']
			status = form.cleaned_data['status']
			Attendance.objects.create(teacher=teacher_obj,date=date,student=student,course=student.course,subject=teacher_obj.teachersubjectregistration.subject, status=status)
			messages.success(request,"attendance add successfully!")
			return HttpResponseRedirect(reverse('management:take-attendance'))
	else:
		today = datetime.date.today()
		attendance = Attendance.objects.filter(teacher_id=teacher_obj.id,date=today)
		form = AttendanceForm()
		context = {
			'today':today,
			'attendance':attendance,
			'form':form,
		}
	return render(request,'management/take_attendance.html',context)

def attendance_record(request):
	teacher_obj = request.user
	attendance = Attendance.objects.filter(teacher_id=teacher_obj.id,subject=teacher_obj.teachersubjectregistration.subject)
	if len(attendance) !=0:
		return render(request,'management/attendance_record.html',{'attendance':attendance})
	else:
		messages.info(request,"you have no any attendance record!")
		return redirect('management:take-attendance')

def update_attendance(request,id):
	attendance = Attendance.objects.get(pk=id)
	if request.method=="POST":
		form = AttendanceForm(request.POST)
		if form.is_valid():
			attendance.date = form.cleaned_data['date']
			attendance.student = form.cleaned_data['student']
			attendance.status = form.cleaned_data['status']
			attendance.save()
			messages.success(request,"attendance update successfully!")
			return HttpResponseRedirect(reverse('management:attendance-record'))
	else:
		attendance_data = {
			'date':attendance.date,
			'student':attendance.student,
			'status':attendance.status,
		}
		form = AttendanceForm(attendance_data)
		return render(request,'management/attendance_update.html',{'form':form})

def delete_attendance(request,id):
	attendance = get_object_or_404(Attendance,pk=id)
	attendance.delete()
	messages.success(request,"attendance delete successfully")
	return redirect('/management/attendance-record')

def result_add(request):
	if request.method=='POST':
		form = ResultForm(request.POST)
		if form.is_valid():
			student = form.cleaned_data['student']
			marks = form.cleaned_data['marks']
			subject = request.user.teachersubjectregistration.subject
			Result.objects.create(teacher=request.user,student=student,marks=marks,subject=subject)
			messages.success(request,"result add successfully!")
			return HttpResponseRedirect(reverse('management:add-result'))
	else:
		form = ResultForm()
		results = Result.objects.filter(teacher=request.user)
		context = {
			'form':form,
			'results':results,
		}
	return render(request,'management/add_result.html',context)

def update_result(request,id):
	result = Result.objects.get(pk=id)
	if request.method=="POST":
		form = ResultForm(request.POST)
		if form.is_valid():
			result.student = form.cleaned_data['student']
			result.marks = form.cleaned_data['marks']
			result.save()
			messages.success(request,"result update successfully!")
			return HttpResponseRedirect(reverse('management:add-result'))
	else:
		result_data = {
			'student':result.student,
			'marks' : result.marks,
		}
		form = ResultForm(result_data)
		return render(request,'management/update_result.html',{'form':form})

def delete_result(request,id):
	result = Result.objects.get(pk=id)
	result.delete()
	messages.success(request,"deleted successfully1")
	return redirect('/management/add-result')

def result_view(request):
	result = Result.objects.filter(student=request.user)
	return render(request,'management/view_result.html',{'results':result})

#------------------------------signup Login logout function----------------------------------
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
			messages.success(request,"You have successfully signup , you can login using username and password")
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

				return redirect('management:index')
	else:
		form = LoginForm()
	return render(request,'management/login.html',{'form':form})
	

def logout_view(request):
	logout(request)
	messages.success(request,"you have successfully logged out")
	return redirect('management:index')
