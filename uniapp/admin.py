from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project, Task

# Extend Django's built-in User admin
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register User model
admin.site.register(User, CustomUserAdmin)

# Register Project model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'end_date')
    filter_horizontal = ('assigned_students',)

# Register Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_student', 'project', 'deadline', 'stage')
    list_filter = ('stage', 'deadline', 'project')
