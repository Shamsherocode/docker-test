
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .manager import UserManager
from .choices import *
from random import randint


class RegisterUser(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email

def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 ,null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        self.password = random_with_N_digits(12)
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email



class QuizCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    img = models.ImageField(upload_to='media', blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class QuizOption(models.Model):
    option1 = models.CharField(max_length=255, unique=False, blank=False)
    option2 = models.CharField(max_length=255, unique=False, blank=False)

    def __str__(self):
        return self.option1 + self.option2



class Quizs(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    point = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    options = models.OneToOneField(QuizOption, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='media', blank=False, null=False)
    publish_date = models.DateTimeField()
    end_date = models.DateTimeField()
    notice = models.TextField()

    def __str__(self):
        return self.name


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class UserProfile(models.Model):
    user = models.OneToOneField(RegisterUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='media', blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    public_key = models.CharField(max_length=12,  unique=True, blank=True, null=True)
    private_key = models.CharField(max_length=16, unique=True, blank=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, blank=True, null=True)


    def save(self, *args, **kwargs):
        self.public_key = random_with_N_digits(12)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.public_key


class Transaction(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Quizs, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    user_points = models.IntegerField(null=False, blank=False)  
    points_method = models.CharField(max_length=50, choices=POINTS, null=True, blank=True)
    points_status = models.CharField(max_length=50, choices=POINTS_STATUS, null=True, blank=True)

    def __str__(self):
        return self.user.email