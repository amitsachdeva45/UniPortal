from django import forms

from .models import Course
################################################FORM 1######
class CourseModelForm(forms.ModelForm):
    class Meta: #It means that data which is not field
        model = Course
        fields = ["course_name", "Description", "branch_choice", "course_course", "semester"]
        labels = {
            "Description": "Enter a description",
            "course_name": "Enter Course Name",
            "course_choice": "Enter the Course Choice",
            "branch_course": "Enter the Branch course",
            "semester": "Enter your semester"
        }
        error_messages = {
            "Description": {
                "required": "This description is required"
            },
            "branch_choice": {
                "required": "The Branch Choice is required"
            },
            "course_choice": {
                "required": "The course field is required"
            },
            "course_name": {
                "required": "The Course Name field is required"
            },
            "semester": {
                "required": "The Semester field is required"
            }
        }