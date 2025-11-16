from rest_framework import serializers
from .models import Student, Course, CalendarSlot


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'name', 'description', 'instructor', 'credits', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CalendarSlotSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    student_name = serializers.SerializerMethodField()
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = CalendarSlot
        fields = [
            'id', 'course', 'course_code', 'course_name', 'student', 'student_name',
            'day_of_week', 'day_of_week_display', 'start_time', 'end_time',
            'date', 'is_recurring', 'room', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_student_name(self, obj):
        if obj.student:
            return obj.student.full_name
        return None
    
    def validate(self, data):
        """Validate that end_time is after start_time"""
        if 'start_time' in data and 'end_time' in data:
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time.")
        return data


class CalendarSlotListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CalendarSlot
        fields = [
            'id', 'course_code', 'course_name', 'student_name',
            'day_of_week', 'start_time', 'end_time', 'is_recurring', 'date', 'room'
        ]
    
    def get_student_name(self, obj):
        if obj.student:
            return obj.student.full_name
        return None

