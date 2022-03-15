from django.conf import settings
from django.core.mail import send_mail
import random
# from .models import User
from .models import RegisterUser, User


def sendOTP(user):
    subject = 'welcome to Hututoo World'
    otp = random.randint(100000, 999999)
    message = f'Hii {user.email}\nYour OTP is {otp} for email verification'
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, [user.email] )
    # user = RegisterUser.objects.get(email = email)
    user.otp = otp
    user.save()


