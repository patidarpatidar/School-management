
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from management import views

router = DefaultRouter()
router.register('users',views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    
    path('api-auth/',include('rest_framework.urls' ,namespace='rest_framework')),
    path('management/',include('management.urls')),
    

]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
