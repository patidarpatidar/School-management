from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'management'
urlpatterns = [
    
    
    #path('users/',UserList.as_view(),name='user-list'),
    #path('users/<int:pk>',UserDetail.as_view(),name='user-detail'),
    path('userprofile/',UserProfileList.as_view(),name='user-profile'),
    path('userprofile/<int:pk>/',UserProfileDetail.as_view(),name='user-profile-detail'),
    path('course/',CourseList.as_view(),name='course-list'),
    path('course/<int:pk>/',CourseDetail.as_view(),name='course-detail'),
    path('subject/',SubjectList.as_view(),name='subject-list'),
    path('subject/<int:pk>/',SubjectDetail.as_view(),name='subject-detail'),
    path('leave/',LeaveList.as_view(),name='leave-list'),
    path('leave/<int:pk>/',LeaveDetail.as_view(),name='leave-detail'),
    path('feedback/',FeedbackList.as_view(),name='feedback-list'),
    path('feedback/<int:pk>/',FeedbackDetail.as_view(),name='feedback-detail'),
    path('attendance/',AttendanceList.as_view(),name='attendance-list'),
    path('attendance/<int:pk>/',AttendanceDetail.as_view(),name='attendance-detail'),
    path('result/',ResultList.as_view(),name='result-list'),
    path('result/<int:pk>',ResultDetail.as_view(),name='result-detail'),
    path('student/',StudentList.as_view(),name='student-list'),
    path('student/<int:pk>',StudentDetail.as_view(),name='student-detail'),
    #path('student/<int:pk>',StudentDetail.as_view(),name='student-delete'),

    path('teacher/',TeacherList.as_view(),name='teacher-list'),
    path('teacher/<int:pk>',TeacherDetail.as_view(),name='teacher-detail'),
    path('contact/',ContactView.as_view(),name='contact-view'),
    path('userview/',UserView.as_view(),name='user-view'),
    path('throttle/',ThrottleView.as_view(),name='throttle-view'),

    path('',index_view,name='index'),
    path('signup',signup_view,name='signup'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    
    path('user-profile-create',user_profile_create,name='user-profile-create'),
    path('user-profile',user_profile_view,name='user-profile'),
    path('user-update',update_user_detail,name='user-update'),
    path('delete-user',user_profile_delete,name='delete-user'),

    path('course-registration',student_course_registration,name='course-registration'),
    path('course-detail',student_course_detail,name='course-detail'),
    path('update-course-registration',update_student_course_registration,name='update-course-registration'),
    path('delete-course-registration/',delete_student_course_registration,name='delete-course-registration'),

    path('teacher-subject-registration',teacher_course_registration,name='teacher-subject-registration'),
    path('teacher-subject-detail',teacher_course_detail,name='teacher-subject-detail'),
    path('update-subject-registration',update_teacher_course_registration,name='update-subject-registration'),
    path('delete-subject-registration',delete_course_registration,name='delete-subject-registration'),
    
    path('take-attendance',take_attendance,name='take-attendance'),
    path('attendance-persent/<int:id>/<subject>',attendance_persent,name='attendance-persent'),
    path('attendance-absent/<int:id>/<subject>',attendance_absent,name='attendance-absent'),

    path('attendance-record',attendance_record,name='attendance-record'),

    path('attendance-view',attendance_view,name='attendance-view'),
    path('update-attendance-record/<int:id>',update_attendance_record,name='update-attendance-record'),
    path('delete-attendance-record/<int:id>',delete_attendance_record,name='delete-attendance-record'),
    path('delete-all-attendance',delete_all_attendance,name='delete-all-attendance'),
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
    path('change-password',change_password,name='change-password'),

    path('fetch-subject/<int:id>',fetch_subject,name='fetch-subject'),
    path('fetch-student/<int:id>',fetch_student,name='fetch-student'),
    path('fetch-student-attendance/<int:id>',fetch_student_attendance,name='fetch-student-attendance'),

    path('fetch-student-result/<int:id>',fetch_student_result,name='fetch-student-result'),
    path('result-information',result_information,name='result-information'),
    path('update-result-information/<int:id>',update_result_information,name='update-result-information'),
    path('delete-result-information/<int:id>',delete_result_information,name='delete-result-information'),
    path('delete-selected-attendance',delete_selected_attendance,name='delete-selected-attendance'),
    path('forgot-password/',forgot_password,name='forgot-password'),
    path('send-forgot-password-email',send_forgot_password_email,name='send-forgot-password-email'),
    path('password-reset-email-done',password_reset_email_done,name='password-reset-email-done'),

    path('password-reset-done',password_reset_done,name='password-reset-done'),

]
if settings.DEBUG:
        urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns,allowed=['json','html'])
