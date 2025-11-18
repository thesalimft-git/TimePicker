from rest_framework import generics
from .models import Student,Course
from .serializers import StudentSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import CourseSerializer
from rest_framework.permissions import AllowAny




class StudentListcreatView(generics.ListCreateAPIView):
   
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveAPIView):
   
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
   

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    http_method_names = ['get', 'post', 'delete']