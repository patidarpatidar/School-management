from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):

	def has_permission(self,request,view):
		if request.user.is_superuser:
			return True
		return False
	
	
	#def has_object_permission(self,request,view,obj):
		
	