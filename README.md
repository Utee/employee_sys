# employee_sys

Employee Management System
A web-based application to manage employees efficiently. Features include employee registration, ID generator, task assignment, notifications, analytics dashboard, and audit logging.

### Features
- Authentication: Secure login and registration for employees.
- Employee Management: Create, update, and manage employee profiles.
- Task Management: Assign, update, and track task statuses.
- Notifications: Send notifications to employees and mark them as read.
- Analytics Dashboard: Visualize key metrics like tasks, employee data, and notifications.
- Audit Logs: Track system activities for compliance and transparency.
- Password Reset: Allow employees to reset passwords securely.

## Tech Stack
- Backend: Django (REST API)
- Frontend: React.js (still in works)
- Database: PostgreSQL
- Authentication: Token-based (using Django REST Framework)
- Deployment: To be hosted on a cloud provider (e.g., AWS, Heroku).


### API endpoints

| Endpoint                              | Method | Description                          |
|---------------------------------------|--------|--------------------------------------|
| `/api/employees/register/`            | POST   | Register a new employee              |
| `/api/employees/login/`               | POST   | Login an employee                    |
| `/api/employees/profile/`             | GET    | Get employee profile                 |
| `/api/employees/profile/update/`      | PUT    | Update employee profile              |
| `/api/password_reset/`                | POST   | Initiate password reset              |
| `/api/tasks/`                         | GET    | Fetch all tasks                      |
| `/api/tasks/create/`                  | POST   | Create a new task                    |
| `/api/tasks/assign/`                  | POST   | Assign a task to an employee         |
| `/api/tasks/status/<int:pk>/`         | PATCH  | Update task status                   |
| `/api/notifications/`                 | GET    | Fetch notifications                  |
| `/api/notifications/send/`            | POST   | Send a notification to an employee   |
| `/api/notifications/create/`          | POST   | Create a custom notification         |
| `/api/notifications/read/<int:pk>/`   | PATCH  | Mark a notification as read          |
| `/api/employee/<int:pk>/activate/`    | PATCH  | Activate an employee account         |
| `/api/analytics/`                     | GET    | View analytics data                  |
| `/api/audit-logs/`                    | GET    | View audit logs                      |

