from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
# Create your tests here.
from management.models import Course
from management.forms import SignUpForm , LoginForm
from django.test import Client
from django.urls import reverse
from management.views import signup_view


class BaseTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(first_name='rajmal',last_name='psatidar',username='rajmal123',email='rajmalpatidar2248@gmail.com',password='dprv7231')
		
		self.user_same_username_email = {'first_name':'rajmal','last_name':'patidar','username':'rajmal123','email':'rajmalpatidar2248@gmail.com','password':'dprv7231','confirm_password':'dprv7231'}

		self.user_unmatching_password={'first_name':'rajmal','last_name':'patidar','username':'rajmal123789','email':'rajmalpatidar2248@gmail.com','password':'dprv7231','confirm_password':'dprv'}

		return super().setUp()

class SignUpFormTest(BaseTest):	
	def test_email_required(self):
		form = SignUpForm()
		self.assertEqual(form.fields['email'].required,True)

	def test_clean_first_name(self):
		form = SignUpForm({'first_name':'rajmal'})
		self.assertEqual(form['first_name'].errors,[])
	
	def test_clean_last_name(self):
		form = SignUpForm({'last_name':'patidar'})
		self.assertEqual(form['last_name'].errors,[])
	
	def test_email_unique(self):
		form = SignUpForm(self.user_same_username_email)
		self.assertEqual(form['email'].errors,[])

	def test_clean_confirm_password(self):
		form = SignUpForm(self.user_unmatching_password)
		self.assertEqual(form['confirm_password'].errors,[])

	def test_username_unique(self):
		form = SignUpForm(self.user_same_username_email)
		self.assertEqual(form['username'].errors,[])


class SignupViewTest(TestCase):
	def setUp(self):
		self.register_url=reverse('management:signup')
		self.user_register = {'first_name':'rajmal','last_name':'patidar','username':'rajmal123','email':'rajmalpatidar2248@gmail.com','password':'dprv7231','confirm_password':'dprv7231'}
	
	def test_can_view_page_correctly(self):
		response = self.client.get(self.register_url)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'management/signup.html')
	
	def test_can_register_user(self):
		response= self.client.post(self.register_url,self.user_register,format='text/html')
		self.assertEqual(response.status_code,302)
		self.assertEqual(User.objects.count(), 1)
		print(User.objects.all())
	
	def test_can_register_after_get_redirect_url(self):
		response= self.client.post(self.register_url,self.user_register,format='text/html')
		redirect = self.client.get(reverse('management:login'))
		self.assertEqual(redirect.status_code,200)
	
	def test_form_is_valid_or_invalid(self):
		form = SignUpForm({'first_name':'rajmal','last_name':'patidar','username':'','email':'rajmalpatidar2248@gmail.com','password':'dprv7231','confirm_password':'dprv7231'})
		self.assertIs(form.is_valid(),False)


class LoginFormTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='rajmal123', password='dprv7231')
	def test_correct_username(self):
		form = LoginForm({'username':'rajmal123','password':'dprv7231'})
		self.assertEqual(form.is_valid(),True)

class LoginViewTest(TestCase):
	def setUp(self):
		self.url = reverse('management:login')
		self.user = User.objects.create_user(username='rajmal123', password='dprv7231')
		
	def test_correct_username_password(self):
		form = LoginForm({'username':'rajmal123','password':'dprv7231'})
		self.assertIs(form.is_valid(),True)
		user = authenticate(username='rajmal123',password='dprv7231')
		self.assertIs((user is not None) and user.is_authenticated,True) 

	def test_pass_wrong_username(self):
		form = LoginForm({'username':'username','password':'dprv7231'})
		self.assertEqual(form['username'].errors,[])
		user = authenticate(username='username',password='dprv7231')
		self.assertIs((user is not None) and user.is_authenticated,False) 

	def test_pass_wrong_password(self):
		form = LoginForm({'username':'rajmal123','password':'password'})
		self.assertEqual(form['password'].errors,[])
		user = authenticate(username='rajmal123',password='password')
		self.assertIs((user is not None) and user.is_authenticated,False) 







'''
class CourseModelTest(TestCase):
	def test_is_this_thing_on(self):
		self.assertEqual(1, 1)

	def test_name_label(self):
		course = Course(id=1)
		field_label = course._meta.get_field('name').verbose_name
		self.assertEqual(field_label,'name')

	def test_name_max_length(self):
		course = Course(id=1)
		max_length = course._meta.get_field('name').max_length
		self.assertEqual(max_length,200)

	def test_object_name_is_name(self):
		course = Course(id=1)
		obj_name = f'{course.name}'
		self.assertEqual(str(course),obj_name)
'''
	