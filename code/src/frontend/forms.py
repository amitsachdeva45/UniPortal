from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

################################################FORM 2######
SEMESTER_CHOICES = [
    ('1', 'Fall'),
    ('2', 'Spring'),
    ('3', 'Summer')
]
DEGREE_CHOICES = [
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master')
]
COURSE_CHOICES = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('CIVIL','CIVIL')
]
YEAR = [x for x in range(1980,2040)]
STARTING_YEAR = [('2019', '2019'),
    ('2020', '2020')]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    date_of_birth = forms.DateField(label="Enter your Date of birth", initial="2010-02-12", required=True, widget=forms.SelectDateWidget(years=YEAR))
    semester_choice = forms.CharField(label="Select Intake Semester", widget=forms.Select(choices=SEMESTER_CHOICES), required=True)
    branch_choice = forms.CharField(label="Select Degree", widget=forms.Select(choices=DEGREE_CHOICES), required=True)
    course_choice = forms.CharField(label="Select Course", widget=forms.Select(choices=COURSE_CHOICES), required=True)
    type_of_user = forms.CharField(initial="candidate", disabled=True)
    starting_year = forms.CharField(widget=forms.Select(choices=STARTING_YEAR), required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth',
                  'semester_choice', 'branch_choice', 'type_of_user', 'starting_year')
        widgets = {'type_of_user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=120, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password_a = self.cleaned_data.get('password')
        user_obj = User.objects.filter(email = email).first()
        if not user_obj:
            raise forms.ValidationError("Invalid Credentials")
        else:
            if not user_obj.check_password(password_a):
                raise forms.ValidationError("Invalid Credentials")
            if not user_obj.is_active:
                raise forms.ValidationError("Inactive User. Please confirm email address")
        return super(UserLoginForm,self).clean(*args,**kwargs)