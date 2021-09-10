from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from .views import *
app_name = 'management'
urlpatterns = [
    path('',index_view,name='index'),
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    path('user-profile-create',user_profile_create,name='user-profile-create'),
    path('user-profile',user_profile_view,name='user-profile'),
    path('user-update',update_user_detail,name='user-update'),
    path('delete-user',user_delete,name='delete-user'),

    
    path('course-registration-detail',student_course_registration_view,name='course-registration-detail'),
    path('update-course-registration',update_student_course_registration,name='update-course-registration'),
    path('delete-course-registration/',delete_student_course_registration,name='delete-course-registration'),

    path('teacher-subject',teacher_subject_registration_view,name='teacher-subject'),
    path('update-subject-registration',update_subject_registration,name='update-subject-registration'),
    path('delete-subject-registration',delete_subject_registration,name='delete-subject-registration'),

    
    path('take-attendance',take_attendance,name='take-attendance'),
    path('attendance-record',attendance_record,name='attendance-record'),
    path('attendance-view',attendance_view,name='attendance-view'),
    path('update-attendance-record/<int:id>',update_attendance_record,name='update-attendance-record'),
    path('delete-attendance-record/<int:id>',delete_attendance_record,name='delete-attendance-record'),
    path('update-attendance/<int:id>',update_attendance,name='update-attendance'),
    path('delete-attendance/<int:id>',delete_attendance,name='delete-attendance'),

    path('leave-information',apply_leave_view,name='leave-information'),
    path('update-leave/<int:id>',update_leave,name='update-leave'),
    path('delete-leave/<int:id>',delete_leave,name='delete-leave'),
    
    path('feedback-information',feedback_send_view,name='feedback-information'),
    path('delete-feedback/<int:id>',delete_feedback,name='delete-feedback'),
    path('update-feedback/<int:id>',update_feedback,name='update-feedback'),
    
    path('add-result',result_add,name='add-result'),
    path('view-result',result_view,name='view-result'),
    path('update-result/<int:id>',update_result,name='update-result'),
    path('delete-result/<int:id>',delete_result,name='delete-result'),






]
if settings.DEBUG:
        urlpatterns + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
