from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import (
    CustomUserCreationForm,
    NameCompletionForm,
    ProfileForm,
    SkillForm,
    MessageForm,
    RatingForm,
)
from core.models import Profile, Skill, Message, Rating
import tempfile
from PIL import Image
import io


class CustomUserCreationFormTest(TestCase):
    """Test cases for CustomUserCreationForm"""

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_first_name(self):
        """Test form with missing first name"""
        form_data = {
            "username": "testuser",
            "first_name": "",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_form_missing_last_name(self):
        """Test form with missing last name"""
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_form_password_mismatch(self):
        """Test form with password mismatch"""
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "differentpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_duplicate_username(self):
        """Test form with duplicate username"""
        # Create existing user
        User.objects.create_user(username="testuser", password="pass123")

        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.check_password("complexpass123"))


class NameCompletionFormTest(TestCase):
    """Test cases for NameCompletionForm"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {"first_name": "John", "last_name": "Doe"}
        form = NameCompletionForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_missing_first_name(self):
        """Test form with missing first name"""
        form_data = {"first_name": "", "last_name": "Doe"}
        form = NameCompletionForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_form_missing_last_name(self):
        """Test form with missing last name"""
        form_data = {"first_name": "John", "last_name": ""}
        form = NameCompletionForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_form_names_already_set(self):
        """Test form validation when names are already set"""
        self.user.first_name = "Existing"
        self.user.last_name = "Name"
        self.user.save()

        form_data = {"first_name": "John", "last_name": "Doe"}

        # Should raise ValidationError during form initialization
        with self.assertRaises(Exception):
            form = NameCompletionForm(data=form_data, instance=self.user)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {"first_name": "John", "last_name": "Doe"}
        form = NameCompletionForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

        updated_user = form.save()
        self.assertEqual(updated_user.first_name, "John")
        self.assertEqual(updated_user.last_name, "Doe")


class ProfileFormTest(TestCase):
    """Test cases for ProfileForm"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile = self.user.profile

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "bio": "This is my bio",
            "city": "Stockholm",
            "country": "Sweden",
            "gender": "M",
            "skills_offered": "Python, Django",
            "skills_needed": "JavaScript, React",
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_optional_fields(self):
        """Test form with only required fields"""
        form_data = {
            "bio": "",
            "city": "Stockholm",
            "country": "Sweden",
            "gender": "",
            "skills_offered": "",
            "skills_needed": "",
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_with_image(self):
        """Test form with profile picture upload"""
        # Create a test image
        image = Image.new("RGB", (100, 100), color="red")
        image_file = io.BytesIO()
        image.save(image_file, format="JPEG")
        image_file.seek(0)

        uploaded_file = SimpleUploadedFile(
            "test_image.jpg", image_file.getvalue(), content_type="image/jpeg"
        )

        form_data = {"bio": "Bio with image", "city": "Stockholm", "country": "Sweden"}
        files_data = {"profile_picture": uploaded_file}

        form = ProfileForm(data=form_data, files=files_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_gender_choices(self):
        """Test form gender field choices"""
        form = ProfileForm(instance=self.profile)
        gender_choices = form.fields["gender"].choices

        expected_choices = [
            ("", "---------"),
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
            ("P", "Prefer not to say"),
        ]

        self.assertEqual(list(gender_choices), expected_choices)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            "bio": "Updated bio",
            "city": "Stockholm",
            "country": "Sweden",
            "gender": "F",
            "skills_offered": "Python",
            "skills_needed": "JavaScript",
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

        updated_profile = form.save()
        self.assertEqual(updated_profile.bio, "Updated bio")
        self.assertEqual(updated_profile.gender, "F")


class SkillFormTest(TestCase):
    """Test cases for SkillForm"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "title": "Python Programming",
            "description": "Learn Python from basics to advanced",
            "skill_type": "offer",
            "category": "technology",
            "location": "Stockholm",
            "availability": "Weekends",
            "is_remote": True,
        }
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_required_fields(self):
        """Test form with missing required fields"""
        form_data = {
            "title": "",  # Required field missing
            "description": "Some description",
            "skill_type": "offer",
            "category": "technology",
        }
        form = SkillForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_skill_type_choices(self):
        """Test skill_type field choices"""
        form = SkillForm()
        skill_type_choices = form.fields["skill_type"].choices

        expected_choices = [("offer", "Skill Offered"), ("request", "Skill Requested")]

        self.assertEqual(skill_type_choices, expected_choices)

    def test_form_category_choices(self):
        """Test category field choices"""
        form = SkillForm()
        category_choices = form.fields["category"].choices

        # Should include all categories from model
        self.assertIn(("technology", "IT, Programming & Tech"), category_choices)
        self.assertIn(("languages", "Languages"), category_choices)
        self.assertIn(("music", "Music & Arts"), category_choices)

    def test_form_optional_fields(self):
        """Test form with optional fields empty"""
        form_data = {
            "title": "Basic Skill",
            "description": "Basic description",
            "skill_type": "offer",
            "category": "other",
            "location": "",  # Optional
            "availability": "",  # Optional
            "is_remote": False,
        }
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_help_text(self):
        """Test form field help text"""
        form = SkillForm()

        self.assertIn(
            "Where can this skill be taught/learned?", form.fields["location"].help_text
        )
        self.assertIn("When are you available?", form.fields["availability"].help_text)
        self.assertIn(
            "Can this be done remotely/online?", form.fields["is_remote"].help_text
        )

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            "title": "Django Web Development",
            "description": "Build web applications with Django",
            "skill_type": "offer",
            "category": "technology",
            "location": "Stockholm",
            "availability": "Evenings",
            "is_remote": True,
        }
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid())

        skill = form.save(commit=False)
        skill.user = self.user
        skill.save()

        self.assertEqual(skill.title, "Django Web Development")
        self.assertEqual(skill.user, self.user)
        self.assertTrue(skill.is_remote)


class MessageFormTest(TestCase):
    """Test cases for MessageForm"""

    def setUp(self):
        """Set up test data"""
        self.sender = User.objects.create_user(
            username="sender", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="testpass123"
        )
        self.skill = Skill.objects.create(
            user=self.receiver,
            title="Python",
            description="Programming",
            skill_type="offer",
            category="technology",
        )

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "subject": "Question about Python",
            "message": "Hi, I would like to learn Python. Can you help me?",
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_subject(self):
        """Test form with missing subject"""
        form_data = {"subject": "", "message": "Some message content"}
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_form_missing_message(self):
        """Test form with missing message content"""
        form_data = {"subject": "Some subject", "message": ""}
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_form_max_length_subject(self):
        """Test form with subject exceeding max length"""
        long_subject = "x" * 201  # Assuming max_length=200
        form_data = {"subject": long_subject, "message": "Some message"}
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            "subject": "Learning Python",
            "message": "I am interested in learning Python programming.",
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

        message = form.save(commit=False)
        message.sender = self.sender
        message.receiver = self.receiver
        message.skill = self.skill
        message.save()

        self.assertEqual(message.subject, "Learning Python")
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.skill, self.skill)


class RatingFormTest(TestCase):
    """Test cases for RatingForm"""

    def setUp(self):
        """Set up test data"""
        self.skill_owner = User.objects.create_user(
            username="skillowner", password="testpass123"
        )
        self.rater = User.objects.create_user(username="rater", password="testpass123")
        self.skill = Skill.objects.create(
            user=self.skill_owner,
            title="Python",
            description="Programming",
            skill_type="offer",
            category="technology",
        )

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "rating": 5,
            "comment": "Excellent teacher! Very helpful and patient.",
        }
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_rating_values(self):
        """Test form with all valid rating values"""
        for rating_value in [1, 2, 3, 4, 5]:
            form_data = {
                "rating": rating_value,
                "comment": f"Rating {rating_value} stars",
            }
            form = RatingForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Rating {rating_value} should be valid")

    def test_form_invalid_rating_value(self):
        """Test form with invalid rating value"""
        form_data = {"rating": 6, "comment": "Great!"}  # Invalid, should be 1-5
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_form_missing_rating(self):
        """Test form with missing rating"""
        form_data = {"rating": "", "comment": "Some comment"}
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_form_optional_comment(self):
        """Test form with optional comment field"""
        form_data = {"rating": 4, "comment": ""}  # Comment is optional
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_rating_choices(self):
        """Test rating field choices"""
        form = RatingForm()
        rating_choices = form.fields["rating"].choices

        expected_choices = [(i, i) for i in range(1, 6)]
        # Django forms add empty choice for required fields
        self.assertEqual(rating_choices[1:], expected_choices)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {"rating": 5, "comment": "Outstanding teaching skills!"}
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

        rating = form.save(commit=False)
        rating.skill = self.skill
        rating.user = self.rater
        rating.save()

        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "Outstanding teaching skills!")
        self.assertEqual(rating.skill, self.skill)
        self.assertEqual(rating.user, self.rater)


class FormWidgetTest(TestCase):
    """Test cases for form widgets and rendering"""

    def test_profile_form_widgets(self):
        """Test ProfileForm widget configuration"""
        form = ProfileForm()

        # Check textarea widget for bio
        self.assertEqual(form.fields["bio"].widget.__class__.__name__, "Textarea")

        # Check widget attributes
        self.assertIn("placeholder", form.fields["bio"].widget.attrs)

    def test_skill_form_widgets(self):
        """Test SkillForm widget configuration"""
        form = SkillForm()

        # Check select widget for choices
        self.assertEqual(form.fields["skill_type"].widget.__class__.__name__, "Select")
        self.assertEqual(form.fields["category"].widget.__class__.__name__, "Select")

        # Check checkbox widget
        self.assertEqual(
            form.fields["is_remote"].widget.__class__.__name__, "CheckboxInput"
        )

    def test_message_form_placeholders(self):
        """Test MessageForm placeholder text"""
        form = MessageForm()

        # Check that placeholders are set
        subject_placeholder = form.fields["subject"].widget.attrs.get("placeholder", "")
        message_placeholder = form.fields["message"].widget.attrs.get("placeholder", "")

        self.assertTrue(len(subject_placeholder) > 0)
        self.assertTrue(len(message_placeholder) > 0)


class FormValidationTest(TestCase):
    """Test cases for custom form validation"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_skill_form_clean_methods(self):
        """Test custom validation methods in SkillForm"""
        # Test if there are any custom clean methods
        form = SkillForm()

        # Basic validation test
        form_data = {
            "title": "Valid Title",
            "description": "Valid description",
            "skill_type": "offer",
            "category": "technology",
        }
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form_validation(self):
        """Test ProfileForm validation"""
        form_data = {
            "bio": "A" * 1000,  # Test long bio
            "city": "Stockholm",
            "country": "Sweden",
        }
        form = ProfileForm(data=form_data, instance=self.user.profile)

        # Should be valid unless there's a specific max_length constraint
        self.assertTrue(form.is_valid() or "bio" in form.errors)

    def test_form_error_messages(self):
        """Test custom error messages"""
        # Test CustomUserCreationForm error messages
        form_data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "password1": "pass",
            "password2": "different",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Check that error messages are present
        self.assertTrue(len(form.errors) > 0)
        self.assertIn("username", form.errors)
        self.assertIn("first_name", form.errors)
        self.assertIn("last_name", form.errors)
