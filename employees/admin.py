from django.contrib import admin
from .models import Employee, Task, Notification

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Notification)
