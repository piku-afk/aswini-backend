from django.urls import path
from .LoginController import views as v1
from .detailscontroller import views as v2
urlpatterns = [

	path('Register/', v1.RegistrationView.as_view(), name ='Register'),
	path('Login/', v1.LoginView.as_view(), name ='Login'),
	path('User/',v1.UserView.as_view(),name='User'),
	path('Logout/',v1.LogoutView.as_view(),name='Logout'),
	path('companydetails/',v2.CompanyDetailsView.as_view(),name='User'),
	path('companydetails/delete/<int:cid>',v2.CompanyDeleteView.as_view(),name='delete'),
	path('companydetails/update/<int:cid>',v2.CompanyUpdateView.as_view(),name='Update')
	# path('User/',v1.UserView.as_view(),name='User'),
]