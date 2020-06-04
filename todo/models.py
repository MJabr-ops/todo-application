from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import BaseUserManager as UserManager



class KarbarManager(UserManager):
    use_in_migrations=True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email,first_name,last_name,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not first_name:
            raise ValueError('first name should given')
        if not last_name:
            raise ValueError('last name should given')
        print("this method is called")

        return self._create_user(email=email,password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class Karbar(AbstractUser):
    email = models.EmailField(_('email address'),unique=True)
    USERNAME_FIELD = 'email'
    username = None
    first_name = models.CharField(max_length=250,null=False)
    REQUIRED_FIELDS = []
    objects = KarbarManager()

    class Meta:
        verbose_name = 'Karbar'
        verbose_name_plural = 'Karbar ha'

user=get_user_model()
class TodoBasket(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='karbaresh')
    title=models.CharField(max_length=250,null=False,unique=True)

    def __str__(self):
        return self.title

class todo(models.Model):
    todoBasket=models.ForeignKey(TodoBasket,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    done=models.BooleanField(default=False)
    dateCreated=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} ...".format(self.text[0:20])





