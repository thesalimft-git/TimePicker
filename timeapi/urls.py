from django.urls import path,include
from .views import (
    
    StudentDetailView,
   StudentListcreatView,
   CourseViewSet
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("courses", CourseViewSet, basename="courses")


urlpatterns = [
    path("", StudentListcreatView.as_view(), name="create-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("", include(router.urls)),
    
]
