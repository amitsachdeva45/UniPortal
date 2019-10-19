from django.db import models
from django.utils import timezone

DEGREE_CHOICES = [
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master')
]
COURSE_CHOICES = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('Civil','Civil')
]
SEMESTER_CHOICES = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('Civil','Civil')
]
INTS_CHOICES = [tuple([str(x),x]) for x in range(1,9)]
# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=120)
    Description = models.TextField(blank=False, null=False)
    branch_choice = models.CharField(choices=DEGREE_CHOICES, max_length=120)
    course_course = models.CharField(choices=COURSE_CHOICES, max_length=120)
    semester = models.CharField(choices=INTS_CHOICES, max_length=120)