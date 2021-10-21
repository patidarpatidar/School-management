from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models.fields import URLField
from django.core.validators import URLValidator
from django.contrib.auth.hashers import make_password , check_password

class UserSerializer(serializers.ModelSerializer):
	#url = serializers.HyperlinkedIdentityField(view_name='user-detail',read_only=True)
	#first_name = serializers.CharField(max_length=20 )
	#last_name = serializers.CharField(max_length=200 )
	#username = serializers.CharField(max_length=200 )
	#email = serializers.EmailField(required=True )
	password = serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'Password'})
	confirm_password=serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'ConfirmPassword'})
	
	class Meta:
		model = User
		fields = ['url','first_name','last_name','email' ,'username', 'password','confirm_password']
		
	def validate_email(self,email):
		user = User.objects.filter(email=email).first()
		if user:
			raise serializers.ValidationError("This email id already taken you can not use this email id!")
		return email

	def validate_username(self,username):
		user = User.objects.filter(username=username).first()
		if user:
			raise serializers.ValidationError("Username must be unique! You can use difrent username!")
		return username
	
	def validate(self,data):
		password = data.get('password')
		confirm_password = data.get('confirm_password')
		if(password!=confirm_password):
			raise serializers.ValidationError("password does not match")
		return data
	
	def create(self,validated_data):
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		email=validated_data['email']
		username=validated_data['username']
		password = validated_data['password']
		return User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
	
	def update(self,instance,validated_data):
		instance.first_name=validated_data.get('first_name',instance.first_name)
		instance.last_name=validated_data.get('last_name',instance.last_name)
		instance.username=validated_data.get('username',instance.username)
		instance.email=validated_data.get('email',instance.email)
		instance.set_password(validated_data.get('password',instance.password))
		instance.save()
		return instance

 

class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(write_only=True,style={'input_type': 'password', 'placeholder': 'Old Password'})
	new_password = serializers.CharField(write_only=True,style={'input_type':'password','placeholder':'New Password'})
	confirm_new_password = serializers.CharField(write_only=True,style={'input_type':'password','placeholder':'Confirm New Password'})		

	def validate_old_password(self,old_password):
		user = self.context.get('user')
		if not check_password(old_password,user.password):
			raise serializers.ValidationError("Old password is wrong!")
		return old_password

	def validate(self,data):
		new_password = data.get('new_password')
		confirm_new_password = data.get('confirm_new_password')
		if(new_password!=confirm_new_password):
			raise serializers.ValidationError("New password and confirm new password do not match!")
		return data
