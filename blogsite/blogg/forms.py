from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Blog, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        # Add your validation logic here
        if any(char.isdigit() for char in username):
            raise forms.ValidationError("Username cannot contain numbers.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        if not username.isalnum():
            raise forms.ValidationError("Username must be alphanumeric.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content'] 
        labels = {
            'title': 'Blog Title',
            'content': 'Blog Content'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})  
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']