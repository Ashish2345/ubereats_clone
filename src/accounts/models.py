from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import FileExtensionValidator

from .middleware import get_current_user

def profile_path(instance, filename):
    return f"accounts/{get_current_user().id}/profile.jpg"

class AuditField(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email,is_active, password=None):
        if not first_name:
            raise ValueError("User must have an first name")
        if not last_name:
            raise ValueError("User must have an last name")
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    gender= (
        (('M', 'Male')),
        (('F', 'Female')),
        (('O', 'Others')),
    )
    first_name = models.CharField(max_length=15,verbose_name="First name")
    last_name = models.CharField(max_length=15,verbose_name="Last name")
    email =  models.EmailField(max_length=30, unique=True, verbose_name="Email")
    contact_no = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(default='M' ,verbose_name='user_gender', max_length=10,
        choices=gender)
    profile_picture = models.FileField(upload_to=profile_path, 
        validators=[FileExtensionValidator(allowed_extensions=settings.VALID_IMAGE_FORMAT)], null=True)

    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name_plural = "Users"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class UserToken(AuditField):
    user_id = models.IntegerField()
    token = models.CharField(max_length=100)
    exipired_at = models.DateTimeField()

    def __str__(self):
        return self.user_id

class Test(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
        