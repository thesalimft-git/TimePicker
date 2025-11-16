from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CourseViewSet, CalendarSlotViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'calendar-slots', CalendarSlotViewSet, basename='calendarslot')

urlpatterns = [
    path('', include(router.urls)),
]

