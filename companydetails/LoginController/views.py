from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed ,ParseError
from companydetails.models import User
from ..serializers import UserSerializer
import json
from django.contrib.auth.hashers import check_password
from ..jwt import access_token,refresh_token,Authenticate

class RegistrationView(APIView):
	def post(self,request):
		serializer=UserSerializer(data=json.loads(request.body))
		
		if serializer.is_valid(raise_exception=True):
			id=serializer.create(serializer.validated_data)
			response=serializer.data
			response['id']=id
			return Response([response,{"Registration":"Successful"}])
		
		
class LoginView(APIView):
	
	def post(self,request):
		email=request.data['email']
		password=request.data['password']
		user=User.objects.filter(email=email).values()
		
	
		if len(user)==0:
			raise AuthenticationFailed("User not found")
			
		if check_password(password ,user[0].get('password')) is False:
			raise AuthenticationFailed("Incorrect Password")

		atoken=access_token(user[0].get('id'))
		reftoken=refresh_token(user[0].get('id'))
		
		response=Response()
		# response.set_cookie(key='jwt',value=token,httponly=True)
		response.data={"access":atoken,"refresh":reftoken}
		return response


class UserView(APIView):
	def get(self,request):
		user_id=Authenticate(request)
		try:
			user=User.objects.get(id=user_id)
			user.is_active=True
			user.save()
			serializer=UserSerializer(user)
			response=serializer.data
			response["login"]="success"
			return Response(response)
		except:
			raise ParseError({"detail":"Something went wrong"})

class LogoutView(APIView):

	def post(self,request):
		id=request.data['id']
		user=User.objects.get(id=id)
		user.is_active=False
		user.save()




