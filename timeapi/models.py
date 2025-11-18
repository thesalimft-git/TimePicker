from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CalendarSlot(models.Model):
    DAY_CHOICES = [
        ("sat", "Saturday"),
        ("sun", "Sunday"),
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
    ]

    SLOT_CHOICES = [
        ("3-5", "3 PM - 5 PM"),
        ("5-7", "5 PM - 7 PM"),
        ("7-9", "7 PM - 9 PM"),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    slot_time = models.CharField(max_length=10, choices=SLOT_CHOICES)

    empty = models.BooleanField(default=True)

    # Many-to-many relationship with students
    students = models.ManyToManyField(Student, related_name="slots", blank=True)

    count_student = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.day} - {self.slot_time}"

    def update_count(self):
        """Update student count manually."""
        self.count_student = self.students.count()
        self.empty = self.count_student == 0
        self.save()


class Course(models.Model):
    name = models.CharField(max_length=100)

    # One-to-many: many courses can use the same calendar slot
    calendar_slot = models.ForeignKey(
        CalendarSlot, on_delete=models.CASCADE, related_name="courses"
    )

    def __str__(self):
        return self.name



