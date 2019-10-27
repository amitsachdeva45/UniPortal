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
IS_PUBLIC = [
    ('1', 'Public'),
    ('0', 'Specific')
]
# Create your models here.
class Post(models.Model):
    description = models.TextField(blank=False, null=False)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=120)
    course = models.CharField(choices=COURSE_CHOICES, max_length=120)
    public = models.CharField(choices=IS_PUBLIC, max_length=120)

    #objects = PostManager()

