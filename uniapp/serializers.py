from rest_framework import serializers
from .models import Project, Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    assigned_students = serializers.PrimaryKeyRelatedField(
    many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Project
        fields = '__all__'