from django.urls import path, include
from .views import (
    AnalyticsDashboardView,
    AssignTaskView,
    AuditLogView,
    EmployeeActivationView,
    EmployeeProfileUpdateView,
    EmployeeRegistrationView,
    EmployeeLoginView,
    EmployeeProfileView,
    MarkNotificationReadView,
    SendNotificationView,
    TaskCreateView,
    TaskListView,
    NotificationCreateView,
    NotificationListView,
    UpdateTaskStatusView
)

urlpatterns = [
    # Employee endpoints
    path('api/employees/register/', EmployeeRegistrationView.as_view(), name='employee-register'),
    path('api/employees/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('api/employees/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('api/employees/profile/update/', EmployeeProfileUpdateView.as_view(), name='employee-profile-update'),
    path('api/employees/<int:pk>/activate/', EmployeeActivationView.as_view(), name='employee-activate'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # Task endpoints
    path('api/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/assign/', AssignTaskView.as_view(), name='assign-task'),
    path('api/tasks/status/<int:pk>/', UpdateTaskStatusView.as_view(), name='update-task-status'),

    # Notification endpoints
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/create/', NotificationCreateView.as_view(), name='notification-create'),
    path('api/notifications/send/', SendNotificationView.as_view(), name='send-notification'),
    path('api/notifications/read/<int:pk>/', MarkNotificationReadView.as_view(), name='mark-notification-read'),

    # Analytics and Audit endpoints
    path('api/analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('api/audit-logs/', AuditLogView.as_view(), name='audit-log'),
]
