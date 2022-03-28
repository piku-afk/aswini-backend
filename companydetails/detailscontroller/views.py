
from xml.dom import ValidationErr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed ,ParseError,ValidationError,PermissionDenied
from companydetails.models import Address, User,Company
from ..serializers import AddressSerializer, AddressSerializer, UserSerializer,CompanySerializer
from ..jwt import Authenticate

class CompanyDetailsView(APIView):

	def get(self,request):
		
		user_id=Authenticate(request)
		user=User.objects.get(id=user_id)

		try:
			companies=Company.objects.filter(user=user)
			response=[]
			for company in companies:
				serializer=CompanySerializer(company)
				address=company.address
				addresserializer=AddressSerializer(address)
				res=serializer.data
				res.update({"address":addresserializer.data})
				response.append(res)
			return Response(response)
		except:
			raise ParseError("Something went wrong")

	def post(self,request):
		user_id=Authenticate(request)
		try:
			data=request.data
			company=Company()
			company.name=data['name']
			company.website=data['website']
			company.phn_no=data['phn_no']
			company.user_id=user_id
			company.industry=data.get('industry','')
			address=Address()
			address.address_1=data.get('address_1','')
			address.address_2=data.get('address_2','')
			address.city=data['city']
			address.state=data['state']
			address.country=data['country']
			address.pin_code=data['pincode']
			
			address.save()
			company.address=address
			company.save()
			serializer=CompanySerializer(company)
			return Response(serializer.data)
		except:
			raise ParseError()


	

	
	


			

class CompanyDeleteView(APIView):

	def delete(self,request,cid):
		print(cid)
		user_id=Authenticate(request)
		
	

		if int(cid) is not None:
			
			obj=Company.objects.get(id=int(cid))
			if obj.user_id==user_id:
				add=obj.address
				add.delete()
				obj.delete()
				return Response({"message":"deleted successfully"})
			else:
				raise PermissionDenied()

			

		
		raise ParseError("Invalid parameters")



class CompanyUpdateView(APIView):
	def put(self,request,cid):
		user_id=Authenticate(request)
		if int(cid) is None:
			raise ValidationError("Invalid Input")
		try:
			obj=Company.objects.get(id=int(cid))
			data=request.data
			obj.name=data['name']
			obj.website=data['website']
			obj.phn_no=data['phn_no']
			obj.user_id=user_id
			obj.industry=data.get('industry','')
			address=obj.address
			address.address_1=data.get('address_1','')
			address.address_2=data.get('address_2','')
			address.city=data['city']
			address.state=data['state']
			address.country=data['country']
			address.pin_code=data['pincode']
				
			address.save()
			obj.save()
			serializer=CompanySerializer(obj)
			return Response(serializer.data)
		except:
			raise ValidationError("invalid id")