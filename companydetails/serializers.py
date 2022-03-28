
from rest_framework import serializers
from .models import Address, Company, User
from django.contrib.auth.hashers import make_password
# from rest_framework import status
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=['id','username','first_name','last_name','email','mobile','password','is_active']
		write_only_fields = ('password',)
		extra_kwargs = {'password': {'write_only': True}}
	    

	def create(self, validated_data):
		
		if validated_data['username'] is None or validated_data['first_name'] is None or validated_data['password'] is None:
			raise serializers.ValidationError({"error":"fill all required fields"})
			

		try:
			username=validated_data['username']
			first_name=validated_data['first_name']
			last_name=validated_data['last_name']
			email=validated_data['email']
			mobile=validated_data['mobile']
			
			password = make_password(validated_data['password'])
			user=User(first_name=first_name,last_name=last_name,email=email,username=username,password=password,mobile=mobile)
			user.save()
			return user.id
		
		except:
			raise serializers.ValidationError({"error":"Something went wrong"})


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model=Company
		fields=['id','name','website','phn_no','industry','address','user']

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model=Address
		fields=['id','address_1','address_2','city','state','country','pin_code']