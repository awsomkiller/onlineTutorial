from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db.models.deletion import PROTECT
from django.db.models.expressions import Value

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, mobile, email, name, password=None, isActive=True, isStaff=False, isAdmin=False):
        if not mobile:
            raise ValueError("MobileNumber is Required")
        if not email:
            raise ValueError("EmailAddress is Required")
        if not name:
            raise ValueError("name is Required")
        if not password:
            raise ValueError("Password is Required")
        
        user_obj = self.model(
            email = self.normalize_email(email),
            mobile = mobile,
            name = name,
        )
        user_obj.mobileConfirm = True
        user_obj.set_password(password)
        user_obj.staff = isStaff
        user_obj.active = isActive
        user_obj.admin = isAdmin
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, mobile, email, name, password=None):
        user_obj = self.create_user(
            mobile,
            email,
            name,
            password=password,
            isStaff=True,
            isAdmin=True
        )
        return user_obj
    def create_staffuser(self, mobile, email, name, password=None):
        user_obj = self.create_user(
            mobile,
            email,
            password=password,
            isStaff=True
        )
        return user_obj
    

class User(AbstractBaseUser):
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    emailConfirm = models.BooleanField(default=False)
    mobileConfirm = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    fees = models.BooleanField(default=False)

    USERNAME_FIELD ="mobile"
    REQUIRED_FIELDS = ['email','name']
    objects = UserManager()
    def __str__(self):
        return self.name
    
    # def get_shortname(self):
    #     return self.firstname
    
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property 
    def is_active(self):
        return self.active

class otpModel(models.Model):
    id = models.AutoField(primary_key=True)
    phonenumber = models.BigIntegerField( unique=True, )
    otp = models.IntegerField()
    current_time = models.DateTimeField()
    success = models.BooleanField(default=False)
    attempt = models.IntegerField(default=1)

class contactus(models.Model):
    CHOICES =(
        ('1','Technical/Website Related Issues'),
        ('2','Payment Issues'),
        ('3','Content Issues'),
        ('4','Doubts')
    )
    id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=20,choices=CHOICES)
    user = models.ForeignKey(User, on_delete=PROTECT, null=True)
    message = models.TextField()

    def __str__(self):
        strs =self.reason
        if strs == '1':
            strs ='Technical/Website Related Issues'
        elif strs == '2':
            strs = 'Payment Issues'
        elif strs == '3':
            strs = "Content Issues"
        else:
            strs = "Doubts"
        return strs
