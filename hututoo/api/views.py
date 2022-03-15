from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from .models import *
from .serializers import *
from .email import sendOTP
from functools import partial
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

import json
import threading
import hashlib

class EmailThread(threading.Thread):
    def __init__(self, sendOTP):
        self.sendOTP = sendOTP
        threading.Thread.__init__(self)

    def run(self):
        self.sendOTP()
       
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class MyPermission(permissions.BasePermission):
    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return request.method in self.allowed_methods

class UserRegister(APIView):
    # permission_classes = [ReadOnly]
    def post(self, request):
        try:
            data = request.data
            serializer = RegitserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                sendOTP(data['email'])
                return Response({
                    'status': 200,
                    'message': 'Verification code sent on the mail address. Please check',
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class LoginUser(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
        print('1111111111111')
        try:
            data = request.data
            print(data, 'ssssss')
            serializer = LoginSerializer(data)
            print(serializer.data, 'ssssssssssssssssssssssssss')
            verify_user = User.objects.filter(email = data['email'])
            print(verify_user, 'vvvvvvvvvvvvvvv')
            if not verify_user:
                print('iiiiiiiiiiiiiiiiii')
                user = User(email = data['email'])
                user.save()
            else:
                user = verify_user[0]
                print(user, 'uuuuuuuuuuuuuuuuuu')
            sendOTP(user)
            return Response({
            'status': 200,
            'message': 'Verification code sent on the mail address. Please check',
            'data': serializer.data,
            })
        except: 
            return Response({
            'status': 400,
            'message': 'Please Type correct Email Address',
            })

class UserProfileView(APIView):
    # permission_classes = [ReadOnly]
    def get(self, request, user):
        try: 
            user_profile = UserProfile.objects.get(user__email=user)
            profile_serializer = UserProfileSerializer(user_profile)
            return Response({'status': 200, 'payload': profile_serializer.data})
        except:
            return Response({'status': 400, 'message': 'Unauthenticted User'})

class EventOptionView(APIView):
    # permission_classes = [ReadOnly]
    def get(self, request):
        data = QuizOption.objects.all()
        serializer = QuizOptionSerializer(data, many=True)
        return Response({'status': 200, 'payload': serializer.data})

class EventCategoryView(APIView):
    # permission_classes = [ReadOnly]
    def get(self, request):
        data = QuizCategory.objects.all()
        serializer = QuizCategorySerializer(data, many=True)
        return Response({'status': 200, 'payload': serializer.data})

class VerifyOTP(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyUserOTPSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                try:
                    user = User.objects.get(email=email)
                    if user.otp != otp:
                        return Response({
                            'status': 400,
                            'message': 'Invalid OTP. Please enter corrent OTP',  
                        })
                    else:
                        if not user.is_verified:
                            user.is_verified = True
                            user.save()
                            privat_key_gen = make_password(user.email + str(user.id))
                            # privat_key_gen = hashlib.md5(user.email + str(user.id).encode('utf-8')).hexdigest() 
                            # key = privat_key_gen.hexdigest()
                            # profile = UserProfile(user = user, private_key = privat_key_gen)
                            # profile.save()
                            # points = Transaction(user = user, user_points=10000, points_method='SignUp Bonus', points_status='Credit')
                            # points.save()
                        user = User.objects.get(email = serializer.data['email'])
                        refresh = RefreshToken.for_user(user)
                        return Response({
                                'status': 200,
                                'message': 'Email Verification is Successfully Completed.',
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)
                            })
                except:
                    return Response({
                        'status': 400,
                        'message': 'Email not found. Please enter the correct Email Address',
                        
                    })

            return Response({
                        'status': 400,
                        'payload': serializer.errors,
                        
                    })
        except:
            return Response({
                        'status': 400,
                        'message': 'Something Went Wrong',
                    })

class EventView(APIView):
    # permission_classes = [ReadOnly]
    def get(self, request):
        quizs = Quizs.objects.all()
        serializer = QuizSerializer(quizs, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self, request):
        serializer = QuizSerializer(data = request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'payload': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()
        return Response({'status': 200, 'payload': serializer.data, 'message': 'You have successfully Created Quiz.'})


    def put(self, request):
        try:
            quizs = Quizs.objects.get(id = request.data['id'])
            serializer = QuizSerializer(quizs, data = request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status': 403, 'payload': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': 'You have successfully Created Quiz.'})

        except Exception as e:
            print(e)
            return Response({'status': 403, 'message': 'Invalid ID'})

    def patch(self, request):
        try:
            quizs = Quizs.objects.get(id = request.data['id'])
            serializer = QuizSerializer(quizs, data = request.data, partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status': 403, 'payload': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': 'You have successfully Created Quiz.'})

        except Exception as e:
            print(e)
            return Response({'status': 403, 'message': 'Invalid ID'})


    def delete(self, request):
        try:
            id = request.GET.get('id')
            quizs = Quizs.objects.get(id=id)
            quizs.delete()
            return Response({'status': 200, 'message': 'Quiz Successfully deleted'})
        
        except Exception as e:
            print(e)
            return Response({'status': 403, 'message': 'Invalid ID'})

class TransactionView(APIView):
    def get(self, request, user):
        try: 
            transaction = Transaction.objects.filter(user__email=user)
            serializer = TransactionSerializer(transaction, many=True)
            total = 0
            for i in serializer.data:
                if i['points_status'] == 'Credit':
                    total = total+i['user_points']
                    print(total, 'sssssssssss')
                else:
                    total = total - i['user_points']

            return Response({'status': 200, 'payload': serializer.data, 'total_points': total})
        except:
            return Response({'status': 400, 'message': 'Unauthenticted User'})


def view_404(request, exception=None):
    return Response({'status': 500, 'message': 'Invalid Request'})


class PredictView(APIView):
    def post(self, request, **kwargs):
        print(kwargs)
        user = get_object_or_404(RegisterUser, email=kwargs['user'])# RegisterUser.object.get(email = user)
        print(user, 'ssssssss')
        event = get_object_or_404(Quizs, id=kwargs['event_id'])
        print(event, 'eve')
        # try:
        # Create  Validator for points 
        trans = Transaction(
            user = user,
            event = event,
            user_points = event.point,
            points_method ="Events Points",
            points_status = "Debit"
        )
        trans.save()
        return Response({'status': 200, 'message': 'success'})
        # except:
        #     return Response({'status': 200, 'message': 'Error'})
        

 