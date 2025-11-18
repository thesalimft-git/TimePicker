from rest_framework import serializers
from .models import Student
from .models import Course, CalendarSlot



class StudentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Student
        fields = ["id", "name", "phone"]

    def validate_phone(self, value):
      
        phone = value.replace(" ", "").strip()

        if not phone.isdigit():
            raise serializers.ValidationError("Phone must contain only digits.")

        if len(phone) < 7:
            raise serializers.ValidationError("Phone number is too short.")

        return phone


class CourseSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Course
        fields = ["id", "name", "calendar_slot"]

    def validate_calendar_slot(self, value):
        
        if not CalendarSlot.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected calendar slot does not exist.")
        return value
