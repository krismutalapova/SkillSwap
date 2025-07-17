from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message, Rating, Message, Rating


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
        ]
        widgets = {
            "bio": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell others about yourself..."}
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
            "bio": "Optional: Tell others about your background and interests",
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            "title",
            "description",
            "skill_type",
            "category",
            "location",
            "availability",
            "is_remote",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g., Python Programming, Guitar Lessons, French Conversation",
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe your skill in detail. What level can you teach? What experience do you have?",
                    "class": "form-control",
                }
            ),
            "skill_type": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g., Stockholm, Online, My place, Coffee shops",
                    "class": "form-control",
                }
            ),
            "availability": forms.TextInput(
                attrs={
                    "placeholder": "e.g., Weekends, Evenings after 6pm, Flexible",
                    "class": "form-control",
                }
            ),
            "is_remote": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "title": "Give the skill a clear, descriptive title",
            "description": "Provide some details about the skill you want to teach/learn and your level",
            "skill_type": "Are you offering to teach this skill or do you want to learn it?",
            "category": "Choose the category that best fits your skill",
            "location": "Where can this skill be taught/learned? (optional)",
            "availability": "When are you available? (optional)",
            "is_remote": "Check if this skill can be taught/learned online",
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title.strip() if title else title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description and len(description.strip()) < 10:
            raise forms.ValidationError(
                "Description must be at least 10 characters long."
            )
        return description.strip() if description else description


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "message")
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Subject",
                    "class": "form-control",
                    "maxlength": "200",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here...",
                    "class": "form-control",
                    "rows": 5,
                    "maxlength": "1000",
                }
            ),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")
        if subject and len(subject.strip()) < 3:
            raise forms.ValidationError("Subject must be at least 3 characters long.")
        return subject.strip() if subject else subject

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if message and len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message.strip() if message else message


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={"class": "rating-radio"}),
        label="Your Rating",
    )

    class Meta:
        model = Rating
        fields = ("rating", "comment")
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Share your experience (optional)...",
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": "500",
                }
            ),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")
        if comment:
            return comment.strip()
        return comment
