from django.shortcuts import render,get_object_or_404 , HttpResponse , redirect , HttpResponseRedirect
from .models import Course , UserProfile,TeacherStudent,Student, Teacher , Attendance , Leave , Feedback , Result
from .forms import  SignUpForm , LoginForm ,ChangePasswordform,UserUpdateForm ,UserProfileForm ,CourseRegistrationForm ,ResultForm , AttendanceForm , LeaveForm , FeedbackForm
from django.contrib.auth import login,logout, authenticate
# Create your views here.
from django.views.generic.edit import UpdateView , DeleteView
from django.contrib.auth.hashers import check_password ,make_password

import datetime 
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

#-----------------------------User permission function (common)-----------------------------------
#------------------------------------------------------------------------------------->

def index_view(request):
	course = Course.objects.all()
	paginator = Paginator(course,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj':page_obj,
		'total':course.count()
	} 
	return render(request,'management/index.html',context)

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
		context = {
			'user':request.user,
		}
		return render(request,'management/user_profile.html',context)

@login_required(login_url='/management/login/')
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
		form = UserUpdateForm(initial=user_data)
	return render(request,'management/update_user_detail.html',{'form':form})

@login_required(login_url='/management/login/')
def user_profile_delete(request):
	user_profile = request.user.userprofile
	user_profile.delete()
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
		form = CourseRegistrationForm()
	return render(request,"management/course_registration.html",{'form':form})


@login_required(login_url='/management/login/')
def student_course_detail(request):
	student = request.user.student
	teacherstudent = TeacherStudent.objects.filter(student=student)
	context = {
		'course_detail':student,
		'teacherstudent':teacherstudent, 
	}
	return render(request,'management/course_registration_detail.html',context)

@login_required(login_url='/management/login/')
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
		course_data = {
		'course':student.course,
		'subjects':student.subjects.all,
		}
		form = CourseRegistrationForm(initial=course_data)
	return render(request,'management/update_course_registration.html',{'form':form})


@login_required(login_url='/management/login/')
def delete_student_course_registration(request):
	course = request.user.student
	course.delete()
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
		context = {
			'page_obj':page_obj,
			'persent':persent,
			'absent':absent,
		}
		return render(request,'management/attendance_view.html',context)
	else:
		messages.info(request,"You have not attend any class so you have not  any attendance record!")
		return redirect('/management/user-profile')

@login_required(login_url='/management/login/')
def result_view(request):
	student = request.user.student
	subjects = student.subjects.all()
	result = Result.objects.filter(students_id=student.id,subjects__in=subjects)
	return render(request,'management/view_result.html',{'results':result})

#-----------------------------Teacher permission function-----------------------------------
#------------------------------------------------------------------------------------->

@login_required(login_url='/management/login/')
def teacher_subject_registration(request):
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
		form = CourseRegistrationForm()
	return render(request,'management/course_registration.html',{'form':form})

@login_required(login_url='/management/login/')
def teacher_subject_detail(request):
	teacher = request.user.teacher
	total_student = teacher.students.count()	
	context = {
		'total_student':total_student,
		'subject_detail':teacher
	}
	return render(request,'management/teacher_subject_detail.html',context)

@login_required(login_url='/management/login/')
def update_subject_registration(request):
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
		subject_data = {
			'course':teacher.course,
			'subjects':teacher.subjects.all,
		}
		form = CourseRegistrationForm(initial = subject_data)
	return render(request,'management/update_course_registration.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_subject_registration(request):
	teacher = request.user.teacher
	teacher.delete()
	messages.success(request,"successfully deleted")
	return redirect('/management/user-profile')

@login_required(login_url='/management/login/')
def take_attendance(request):
	teacher = request.user.teacher
	if request.method=='POST':
		form = AttendanceForm(teacher,request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subjects']
			student = form.cleaned_data['students']
			date = form.cleaned_data['date']
			status = form.cleaned_data['status']
			Attendance.objects.create(teacher=request.user,date=date,students=student,course=teacher.course,subjects=subject, status=status)
			messages.success(request,"attendance add successfully!")
			return HttpResponseRedirect(reverse('management:take-attendance'))
	else:
		today = datetime.date.today()
		attendance = Attendance.objects.filter(teacher=request.user,date=today)
		form = AttendanceForm(teacher)
		paginator = Paginator(attendance,4)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context = {
			'today':today,
			'page_obj':page_obj,
			'form':form,
			}
		return render(request,'management/take_attendance.html',context)

@login_required(login_url='/management/login/')
def update_attendance(request,id):
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
			return HttpResponseRedirect(reverse('management:take-attendance'))
	else:
		attendance_data = {
			'subjects':attendance.subjects,
			'date':attendance.date,
			'students':attendance.students,
			'status':attendance.status,
		}
		form = AttendanceForm(teacher,initial=attendance_data )
		return render(request,'management/attendance_update.html',{'form':form})

@login_required(login_url='/management/login/')
def attendance_record(request):
	teacher_obj = request.user
	attendance = Attendance.objects.filter(teacher_id=teacher_obj.id)
	paginator = Paginator(attendance,4)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	if len(attendance) !=0:
		return render(request,'management/attendance_record.html',{'page_obj':page_obj})
	else:
		messages.info(request,"you have no any attendance record!")
	return redirect('management:take-attendance')


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
		attendance_data = {
			'subjects':attendance.subjects,
			'date':attendance.date,
			'students':attendance.students,
			'status':attendance.status,
		}
		form = AttendanceForm(teacher,initial=attendance_data )
		return render(request,'management/attendance_update.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_attendance_record(request,id):
	attendance = get_object_or_404(Attendance,pk=id)
	attendance.delete()
	messages.success(request,"attendance delete successfully")
	return redirect('/management/attendance-record')


@login_required(login_url='/management/login/')
def delete_attendance(request,id):
	attendance = get_object_or_404(Attendance,pk=id)
	attendance.delete()
	messages.success(request,"attendance delete successfully")
	return redirect('/management/take-attendance')

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
		form = ResultForm(teacher)
		results = Result.objects.filter(teacher=teacher)
		paginator = Paginator(results,5)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context = {
			'form':form,
			'page_obj':page_obj,
		}
		return render(request,'management/add_result.html',context)

@login_required(login_url='/management/login/')
def update_result(request,id):
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
			return HttpResponseRedirect(reverse('management:add-result'))
	else:
		result_data = {
			'subjects':result.subjects,
			'students':result.students,
			'marks' : result.marks,
		}
		form = ResultForm(teacher,initial=result_data)
		return render(request,'management/update_result.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_result(request,id):
	result = Result.objects.get(pk=id)
	result.delete()
	messages.success(request,"deleted successfully1")
	return redirect('/management/add-result')



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
				nxt = request.GET.get('next',None)
				if nxt is None:
					return redirect('management:user-profile')
				else:
					return redirect(nxt)
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
		context = {
			'page_obj':page_obj,
			'form':form
		}
	return render(request,'management/leave_information.html',context)

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
		leave_data = {
		'leave_date':leave.leave_date,
		'leave_message':leave.leave_message,
		}
		form = LeaveForm(initial=leave_data)
	return render(request,'management/update_leave.html',{'form':form})


@login_required(login_url='/management/login/')
def delete_leave(request,id):
	leave = Leave.objects.get(pk=id)
	leave.delete()
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
		context = {
			'form' : form,
			'feedback_list' : feedback_list,
			'page_obj':page_obj,
		}
	return render(request,'management/user_feedback.html',context)

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
		feedback_data = {
		'feedback_message':feedback.feedback_message
		}
		form = FeedbackForm(initial=feedback_data)
	return render(request,'management/update_feedback.html',{'form':form})

@login_required(login_url='/management/login/')
def delete_feedback(request,id):
	feedback = Feedback.objects.get(pk=id)
	feedback.delete()
	messages.success(request,"feedback deleted successfully!")
	return redirect('/management/feedback-information')
