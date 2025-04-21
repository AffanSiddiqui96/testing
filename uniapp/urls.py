from django.urls import path
from .views import (
    ProjectListCreateAPIView, ProjectDetailAPIView,
    TaskListCreateAPIView, TaskDetailAPIView,
    TeacherDashboardAPIView, StudentDashboardAPIView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/token/', obtain_auth_token, name='api-token'),
    path('projects/', ProjectListCreateAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view()),
    path('dashboard/teacher/', TeacherDashboardAPIView.as_view()),
    path('dashboard/student/', StudentDashboardAPIView.as_view()),
]
