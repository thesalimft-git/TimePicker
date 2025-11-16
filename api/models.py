from django.db import models
from django.core.validators import EmailValidator


class Student(models.Model):
    """Model representing a student"""
    student_id = models.CharField(max_length=50, unique=True, help_text="Unique student identifier")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    """Model representing a course"""
    course_code = models.CharField(max_length=20, unique=True, help_text="Unique course code (e.g., CS101)")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=200, blank=True, null=True)
    credits = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.course_code} - {self.name}"


class CalendarSlot(models.Model):
    """Model representing a time slot in the calendar"""
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='calendar_slots')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='calendar_slots', null=True, blank=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(null=True, blank=True, help_text="Specific date if this is a one-time slot")
    is_recurring = models.BooleanField(default=True, help_text="If True, this slot repeats weekly")
    room = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = 'Calendar Slot'
        verbose_name_plural = 'Calendar Slots'
        indexes = [
            models.Index(fields=['day_of_week', 'start_time']),
            models.Index(fields=['course']),
            models.Index(fields=['student']),
        ]

    def __str__(self):
        student_info = f" - {self.student}" if self.student else ""
        date_info = f" on {self.date}" if self.date else ""
        return f"{self.course.course_code} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}{student_info}{date_info}"

    def clean(self):
        """Validate that end_time is after start_time"""
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
