from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not username:
            raise ValueError('please enter your username')
        if not email:
            raise ValueError('please enter your email')

        user= self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user= self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        ) 
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email=models.EmailField(max_length=70,unique=True, verbose_name="Email")
    username=models.CharField(max_length=70, verbose_name="Username")
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_prof=models.BooleanField(default=False)
    batch=models.SmallIntegerField(default=0)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Notes(models.Model ):
    userid= models.IntegerField()
    slotid= models.CharField(max_length=100)
    notes = models.TextField(max_length=1000)

class Algo(models.Model ):
    slot_id=models.IntegerField( primary_key=True)
    prof_name=models.CharField( max_length=50)
    prof_id=models.IntegerField()
    subject=models.CharField( max_length=50)
    subject_id=models.CharField(max_length=50)
    batch=models.CharField( max_length=50)
    batch_id=models.IntegerField()
    day=models.IntegerField()
    time=models.IntegerField()
    email=models.EmailField(max_length=150)

