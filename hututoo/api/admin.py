from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Quizs)
admin.site.register(QuizCategory)
admin.site.register(QuizOption)
admin.site.register(RegisterUser)
admin.site.register(UserProfile)
admin.site.register(Transaction)