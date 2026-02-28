from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from .models import User


def validate_college_email(email):
    """
    Validates that the email belongs to an allowed college domain.
    Allowed domains are defined in settings.ALLOWED_EMAIL_DOMAINS.
    """
    allowed_domains = getattr(settings, 'ALLOWED_EMAIL_DOMAINS', [])
    domain = email.split('@')[-1].lower()

    if allowed_domains and domain not in allowed_domains:
        raise forms.ValidationError(
            f"Registration is restricted to college email addresses. "
            f"Allowed domains: {', '.join(['@' + d for d in allowed_domains])}"
        )
    return email


class StudentRegistrationForm(UserCreationForm):
    """
    Registration form for students with college email validation.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@college.edu'
        })
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    college_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your College / University name'
        })
    )
    graduation_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 2026'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username',
            'college_name', 'graduation_year', 'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        # Run college domain validation
        validate_college_email(email)
        # Check uniqueness
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class StudentLoginForm(AuthenticationForm):
    """
    Custom login form using email instead of username.
    """
    username = forms.EmailField(
        label='College Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@college.edu',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your password'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tell others about yourself...'
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    college_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    graduation_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio',
            'phone', 'profile_picture', 'college_name', 'graduation_year'
        ]