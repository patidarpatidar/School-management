from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models.fields import URLField
from django.core.validators import URLValidator
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
	
	#first_name = serializers.CharField(max_length=20 )
	#last_name = serializers.CharField(max_length=200 )
	#username = serializers.CharField(max_length=200 )
	#email = serializers.EmailField(required=True )
	password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'},write_only=True)
	#confirm_password=serializers.CharField(write_only=True,required=True,style={'input_type': 'password', 'placeholder': 'ConfirmPassword'})
	
	class Meta:
		model = User
		fields = ['url','first_name','last_name','email' ,'username', 'password']
	
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

	def validate_password(self,password):
		return make_password(password)
	
	
	'''
	def validate(self,data):
		password = data.get('password')
		confirm_password = data.get('confirm_password')
		if(password!=confirm_password):
			raise serializers.ValidationError("password does not match")
		return data
	'''
	
	
	'''
	def create(self,validated_data):
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		email=validated_data['email']
		username=validated_data['username']
		password = validated_data['password']
		return User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
	

	'''
	'''
	def update(self,instance,validated_data):
		instance.first_name=validated_data.get('first_name',instance.first_name)
		instance.last_name=validated_data.get('last_name',instance.last_name)
		instance.username=validated_data.get('username',instance.username)
		instance.email=validated_data.get('email',instance.email)
		instance.set_password(validated_data.get('password',instance.password))
		instance.save()
		return instance
	
	def create(self,validated_data):
		return User.objects.create_user(**validated_data)
	'''