from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Student, Course, CalendarSlot
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    CalendarSlotSerializer,
    CalendarSlotListSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Student instances.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    filterset_fields = ['student_id', 'email']


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    search_fields = ['course_code', 'name', 'instructor']
    filterset_fields = ['course_code', 'credits']


class CalendarSlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing CalendarSlot instances.
    """
    queryset = CalendarSlot.objects.select_related('course', 'student').all()
    serializer_class = CalendarSlotSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['course', 'student', 'day_of_week', 'is_recurring', 'date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CalendarSlotListSerializer
        return CalendarSlotSerializer
    
    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """Get all calendar slots for a specific course"""
        course_id = request.query_params.get('course_id', None)
        if course_id:
            slots = self.queryset.filter(course_id=course_id)
            serializer = self.get_serializer(slots, many=True)
            return Response(serializer.data)
        return Response({'error': 'course_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get all calendar slots for a specific student"""
        student_id = request.query_params.get('student_id', None)
        if student_id:
            slots = self.queryset.filter(student_id=student_id)
            serializer = self.get_serializer(slots, many=True)
            return Response(serializer.data)
        return Response({'error': 'student_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_day(self, request):
        """Get all calendar slots for a specific day of week"""
        day = request.query_params.get('day', None)
        if day:
            slots = self.queryset.filter(day_of_week=day.upper())
            serializer = self.get_serializer(slots, many=True)
            return Response(serializer.data)
        return Response({'error': 'day parameter is required (MON, TUE, WED, etc.)'}, status=status.HTTP_400_BAD_REQUEST)
