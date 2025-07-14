from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class NameCompletionForm(forms.ModelForm):
    """Form for existing users to add their first and last names (one-time only)"""

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"}),
        help_text="Your real first name (cannot be changed later)",
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
        help_text="Your real last name (cannot be changed later)",
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and (self.instance.first_name or self.instance.last_name):
            raise forms.ValidationError(
                "Names have already been set and cannot be changed."
            )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "bio",
            "city",
            "country",
            "gender",
            "skills_offered",
            "skills_needed",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "skills_offered": forms.Textarea(attrs={"rows": 4}),
            "skills_needed": forms.Textarea(attrs={"rows": 4}),
            "city": forms.TextInput(attrs={"placeholder": "e.g., Stockholm"}),
            "country": forms.TextInput(attrs={"placeholder": "e.g., Sweden"}),
        }
