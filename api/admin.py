from django.contrib import admin
from .models import Student, Course, CalendarSlot


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'name', 'instructor', 'credits', 'created_at']
    list_filter = ['credits', 'created_at']
    search_fields = ['course_code', 'name', 'instructor']
    ordering = ['course_code']


@admin.register(CalendarSlot)
class CalendarSlotAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'day_of_week', 'start_time', 'end_time', 'is_recurring', 'date']
    list_filter = ['day_of_week', 'is_recurring', 'course', 'created_at']
    search_fields = ['course__course_code', 'course__name', 'student__first_name', 'student__last_name', 'student__student_id']
    ordering = ['day_of_week', 'start_time']
    date_hierarchy = 'date'
