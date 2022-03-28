
from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractUser):

        username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
        email = models.EmailField(unique = True)
        mobile = models.CharField(max_length = 10)
        is_active=models.BooleanField(default=False)
       

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
        def __str__(self):
            return "{}".format(self.email)
        
        objects = UserManager()

class Company(models.Model):
	user=models.ForeignKey("User",on_delete=models.CASCADE,related_name='%(class)s_requests_created')
	name=models.CharField(max_length=100,null=False,unique=True)
	website=models.CharField(max_length=100,null=True,blank=True)
	phn_no = models.CharField(max_length = 10)
	address=models.ForeignKey("Address",null=True,on_delete=models.SET_NULL)
	industry=models.TextField(max_length=200,blank=True)
	
    

class Address(models.Model):
    address_1 = models.CharField( max_length=128)
    address_2 = models.CharField(max_length=128, blank=True,null=True)
    city = models.CharField(max_length=64, null=False,blank=False)
    state = models.CharField( max_length=64,null=False,blank=False)
    country = models.CharField( max_length=64,null=False,blank=False)
    pin_code = models.CharField( max_length=5, null=False,blank=False)