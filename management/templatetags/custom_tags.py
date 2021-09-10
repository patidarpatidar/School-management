from django import template
from management.models import Attendance
register = template.Library()

@register.simple_tag
def student_attendance(student):
	if Attendance.objects.filter(student=student).exists():
		return {'true':1}
	else:
		return {'false':0}

