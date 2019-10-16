import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

from django.db import models

from apps.core.models import TimestampedModel

class UserManager(BaseUserManager):
    """Creating our custom users."""

    def create_user(self,email,password=None,**extra_fields):
        if email is None:
            raise TypeError('Users must have a email.')

        user = self.model(email=self.normalize_email(email),
        **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self,email,password, **extra_fields):
        if password is None:
            raise TypeError("Superusers must have a password.")
        
        user = self.create_user(email,password,**extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser,PermissionsMixin,TimestampedModel):


    SEX_CHOICES = (
        ('M','Masculin'),
        ('F','FEMININ'),
    )

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1,choices=SEX_CHOICES,default='F')

    email = models.EmailField(unique=True, db_index=True, max_length=254)

    date_birth = models.DateField()

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=True)

    #created_at = models.DateTimeField(auto_now_add=True)

    #updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name','first_name','date_birth','sex']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_last_name(self):
        return self.last_name
    
    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id':self.pk,
            'exp':int(dt.strftime('%s'))
        },settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
