
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter, SimpleRouter
from management import views
from rest_framework.routers import DefaultRouter
#from django_rest_passwordreset.views import ResetPasswordRequestToken
router = DefaultRouter(trailing_slash=True)
router.register(r'users',views.UserViewSet)

'''
router.register(
    r'validate_token',
    ResetPasswordRequestToken,
    basename='reset-password-request'
)
'''
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    #path(r'reset/', ResetPasswordRequestToken.as_view(), name="reset-password-request"),

    path('api-auth/',include('rest_framework.urls' ,namespace='rest_framework')),
    path('password_reset/',include('django_rest_passwordreset.urls',namespace='password_reset')),
    path('management/',include('management.urls')),
    

]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

