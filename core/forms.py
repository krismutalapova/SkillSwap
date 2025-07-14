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
            "bio": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell others about yourself..."}
            ),
            "skills_offered": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What skills can you help others with? You can always add these later.",
                }
            ),
            "skills_needed": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What skills are you looking to learn? You can always add these later.",
                }
            ),
            "city": forms.TextInput(
                attrs={"placeholder": "e.g., Stockholm (Required)"}
            ),
            "country": forms.TextInput(
                attrs={"placeholder": "e.g., Sweden (Required)"}
            ),
        }
        help_texts = {
            "city": "Required for your profile to appear in search results",
            "country": "Required for your profile to appear in search results",
            "skills_offered": "List skills you can teach or help with (optional but recommended)",
            "skills_needed": "List skills you want to learn (optional but recommended)",
            "bio": "Optional: Tell others about your background and interests",
        }
