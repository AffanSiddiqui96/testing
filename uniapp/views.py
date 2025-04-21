from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent

class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        print(111111111111111111111111111)

        # STUDENT: Can only update stage or attachments, and only for their own task
        if request.user.role == 'student':
            if request.user != task.assigned_student:
                return Response({"detail": "You can only update your own tasks."}, status=403)

            allowed_fields = {'stage', 'attachments'}
            if not any(field in request.data for field in allowed_fields):
                return Response({"detail": "You can only update 'stage' or 'attachments'."}, status=403)

            # Create partial update dict
            update_data = {field: request.data[field] for field in allowed_fields if field in request.data}
            serializer = TaskSerializer(task, data=update_data, partial=True)

        else:
            # Admin/Teacher can update anything
            serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        projects = Project.objects.all()
        tasks = Task.objects.all()
        return Response({
            "projects": ProjectSerializer(projects, many=True).data,
            "tasks": TaskSerializer(tasks, many=True).data
        })

class StudentDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        tasks = Task.objects.filter(assigned_student=request.user)
        return Response({
            "tasks": TaskSerializer(tasks, many=True).data
        })