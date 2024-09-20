"""
URL configuration for LMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.LoginAndRegister.welcome,name="welcome"),
    path('login',views.LoginAndRegister.login,name="login"),
    path('register',views.LoginAndRegister.register,name="register"),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('profile/', views.profile_view, name='profile'),
    path('tests/add/', views.addTest, name='addTest'),
    path('delete_user/', views.delete_user_view, name='delete_user'),
    path('newTests/', views.newTests, name='newTests'),
    path('completed-test/<str:test_gid>/', views.completed_test_view, name='completed_test'),
    path('tests/view/<str:test_gid>/', views.test_view, name='test'),
    path('tests/viewCreated/<str:test_gid>/', views.viewCreated, name='viewCreated'),
    path('tests/remake/<str:test_gid>/', views.remakeTest, name='remakeTest'),
    path('tests/saveTestWeights/<str:test_gid>/', views.save_test_weights, name='save_test_weights'),
    path('test/<uuid:test_gid>/', views.completeTest, name='completeTest'),
    path('test/<uuid:test_gid>/submit/', views.submitTest, name='submitTest'),
    path('grades/', views.viewGrades, name='viewGrades'),
    path('professor-grades/', views.viewProfessorGrades, name='viewProfessorGrades'),
    path('professor-grades/<uuid:class_group_id>/', views.viewClassGroupTestTypeAverages, name='viewClassGroupTestTypeAverages'),
    path('professor-grades/<uuid:class_group_id>/<str:type>/', views.viewClassGroupTestAverages, name='viewClassGroupTestAverages'),
    path('professor-grades/<uuid:class_group_id>/<str:type>/<uuid:test_gid>/', views.viewTestResults, name='viewTestResults'),
    path('questions/', views.my_test_questions, name='my_test_questions'),
    path('questions/view/<str:type>/', views.questions_by_type, name='questions_by_type'),
    path('questions/add/', views.addQuestion, name='addQuestion'),
    path('questions/view/<str:type>/<str:question_gid>/', views.question_analysis, name='question_analysis'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
