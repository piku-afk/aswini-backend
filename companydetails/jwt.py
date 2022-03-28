

from email.policy import HTTP
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed,APIException,ParseError
SECRET='mf'

def access_token(id):
	payload={
			'id':id,
			'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
			'iat':datetime.datetime.utcnow()
		}	

	token=jwt.encode(payload,SECRET,algorithm='HS256')
	return token

def get_access(token):
	try:
		payload=jwt.decode(token,SECRET,algorithms='HS256')
		return payload['id']
	except:
		raise AuthenticationFailed("Invalid Token")



def refresh_token(id):
	payload={
			'id':id,
			'exp':datetime.datetime.utcnow()+datetime.timedelta(days=7),
			'iat':datetime.datetime.utcnow()
		}	

	token=jwt.encode(payload,SECRET,algorithm='HS256')
	return token

def Authenticate(request):
	if request.headers.get('Authorization') is not None:
		token=request.headers.get('Authorization').split()[1]
		return get_access(token)


# def destroyjwt(token):
# 	try:
# 		jwt.destroy(token)
# 	except:
# 		raise ParseError({"error":"something went wrong"})