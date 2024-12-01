from django.db import models
from django.conf import settings
from django.utils import timezone 
import uuid

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate a unique employee ID
            self.employee_id = self.generate_unique_employee_id()
        super(Employee, self).save(*args, **kwargs)

    def generate_unique_employee_id(self):
        # Keep generating a new ID until it's unique
        while True:
            new_id = uuid.uuid4().hex[:10].upper()
            if not Employee.objects.filter(employee_id=new_id).exists():
                return new_id

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Task(models.Model):
    title = models.CharField(max_length=200, default="Untitled Task")
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ], default='Pending')
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f"Notification for {self.user.first_name} {self.user.last_name}"
    
class AuditLog(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"


