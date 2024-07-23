from django.db import models
import secrets
import hashlib
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db import models


class UserAccountManager(BaseUserManager):
    class Meta:
        db_table = 'Users'
    def create_user(self, email, username, first_name, last_name, password):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(email, username, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

class Users(AbstractBaseUser):
    class Meta:
        db_table = 'Users'
    
    username= models.CharField(primary_key=True,max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    last_login = ""
    is_superuser = True
    is_staff = True
    is_active = True
    is_admin = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name' , 'last_name']

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
            return self.is_admin

    objects = UserAccountManager()