from django import forms

from .models import Post
################################################FORM 1######
class PostModelForm(forms.ModelForm):
    class Meta: #It means that data which is not field
        model = Post
        fields = ["description","degree", "course", "public"]
        labels = {
            "description": "Enter a description",
            "degree": "Enter the degree",
            "course": "Enter the course",
            "public": "Select type of notification"
        }
        error_messages = {
            "description": {
                "required": "This description is required"
            },
            "degree": {
                "required": "The degree field is required"
            },
            "course": {
                "required": "The course field is required"
            },
            "public": {
                "required": "The public field is required"
            }
        }