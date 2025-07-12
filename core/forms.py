from django import forms
from .models import Profile


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
