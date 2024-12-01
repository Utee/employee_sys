from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Count
from .models import Employee, Task, Notification, AuditLog
from .serializers import EmployeeSerializer, TaskSerializer, NotificationSerializer
from .utils import generate_id_card
from django.core.cache import cache



class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        id_card_path = generate_id_card(Employee)
        Employee.id_card = id_card_path  
        Employee.save()
        serializer.save()

        return Response({"message": "Employee registered and ID card created."})
        

class EmployeeLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_object(self):
        return self.request.user  

# Update Profile
class EmployeeProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_object(self):
        return self.request.user
    

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
class AssignTaskView(generics.CreateAPIView):
    permission_classes = [IsAdminUser] 
    serializer_class = TaskSerializer

class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
class UpdateTaskStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.select_related('assigned_employee').all()

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        task.status = request.data.get("status", task.status)
        task.save()
        return Response({"status": "Task status updated"})
    

class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    
# Send Notification (Admin Only)
class SendNotificationView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Only admins should be able to send notifications
    serializer_class = NotificationSerializer

# View Notifications
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-priority', '-created_at')

# Mark Notification as Read
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})
    
class EmployeeActivationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        action = request.data.get("action")

        if action == "deactivate":
            employee.is_active = False
        elif action == "activate":
            employee.is_active = True

        employee.save()
        AuditLog.objects.create(user=request.user, action=f"{status} account for {employee.name}")
        status = "activated" if employee.is_active else "deactivated"
        return Response({"message": f"Employee account {status}"})
    
    
class AuditLogView(APIView):
    def get(self, request):
        logs = AuditLog.objects.all().order_by('-timestamp')
        data = [{"user": log.user.name, "action": log.action, "timestamp": log.timestamp} for log in logs]
        return Response(data)

    


class AnalyticsDashboardView(APIView):
    def get(self, request):
        analytics_data = cache.get('analytics_data')

        if not analytics_data:
            task_count = Task.objects.count()
            completed_tasks = Task.objects.filter(status='completed').count()
            employee_count = Employee.objects.count()
            notifications_sent = Notification.objects.count()

            analytics_data = {
                "total_tasks": task_count,
                "completed_tasks": completed_tasks,
                "total_employees": employee_count,
                "notifications_sent": notifications_sent,
            }

            # Cache for 10 minutes
            cache.set('analytics_data', analytics_data, timeout=600)

        return Response(analytics_data)

