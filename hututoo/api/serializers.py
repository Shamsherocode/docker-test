from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'is_verified']

    # def create(self, validated_data):
    #     user = User.objects.create(email = validated_data['email'])
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        # fields = '__all__'
        fields = ['option1', 'option2']




class QuizCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCategory
        # fields = '__all__'
        fields = ['name']

    


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quizs
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['options'] = QuizOptionSerializer(instance.options).data
        rep['category'] = QuizCategorySerializer(instance.category).data
        return rep
    

class QuizSerializerTransaction(serializers.ModelSerializer):
    class Meta:
        model = Quizs
        fields = ['name']


    # def checkdate():
    #     date = datetime.now()
    #     return date

    # def validate(self, data):
    #     if data['created'] < self.checkdate():
    #         raise serializers.ValidationError({'error': 'Date must me valid..'})

    #     return data


class VerifyUserOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class RegitsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['id', 'email', 'is_verified']

class RegitserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_verified']


class RegitserSerializerTransaction(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # otp = serializers.CharField()
    # is_verified = serializers.BooleanField()
    # is_active = serializers.BooleanField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = RegitserSerializer(instance.user).data
        return rep


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'event', 'date_time', 'user_points', 'points_method', 'points_status']
        # depth = 1

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = RegitserSerializerTransaction(instance.user).data
        rep['event'] = QuizSerializerTransaction(instance.event).data
        return rep