from django.contrib import admin
from .models import Course , Subject ,TeacherStudent, UserProfile , Student ,Result, Teacher , Attendance , Leave , Feedback
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
	list_display = ['name','description','fees','duration']
	list_filter = ['name']
admin.site.register(Course,CourseAdmin)
admin.site.register(TeacherStudent)
admin.site.register(Subject)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user','role','gender','phone','street','city','state','pin_code']
	list_filter=['user']
	search_fields = ('role',)
admin.site.register(UserProfile,UserProfileAdmin)

class StudentAdmin(admin.ModelAdmin):
	list_display = ['user','course','get_subjects']
	list_filter = ['course']
admin.site.register(Student,StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
	list_display = ['user','course','get_subjects']
	list_filter = ['course']
admin.site.register(Teacher,TeacherAdmin)

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ['teacher','students','date','course','subjects','status']
	list_filter = ['date']
	search_fields = ("date",)

admin.site.register(Attendance,AttendanceAdmin)

class LeaveAdmin(admin.ModelAdmin):
	list_display = ['user','role','leave_date','leave_message','leave_status']
	list_filter = ['leave_date']
	list_editable = ['leave_status']
admin.site.register(Leave,LeaveAdmin)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ['user','role','created_at','feedback_message','feedback_reply']
	list_editable = ['feedback_reply']

admin.site.register(Feedback,FeedbackAdmin)

class ResultAdmin(admin.ModelAdmin):
	list_display = ['students','subjects','marks','teacher']
admin.site.register(Result,ResultAdmin)

admin.site.site_header = "Student Management"
admin.site.index_title = "student management admin"