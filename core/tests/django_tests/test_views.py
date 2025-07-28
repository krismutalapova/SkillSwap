from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404
from core.models import Profile, Skill, Message, Rating
from core.forms import CustomUserCreationForm, ProfileForm, SkillForm
import json


class AuthenticationViewTest(TestCase):
    """Test cases for authentication-related views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_signup_view_get(self):
        """Test SignupView GET request"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_signup_view_post_valid(self):
        """Test SignupView POST with valid data"""
        data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        response = self.client.post(reverse("signup"), data)

        # Should redirect to home after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Check that profile was created
        new_user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(new_user, "profile"))

    def test_signup_view_post_invalid(self):
        """Test SignupView POST with invalid data"""
        data = {
            "username": "",  # Missing required field
            "first_name": "John",
            "last_name": "Doe",
            "password1": "pass123",
            "password2": "different123",  # Passwords don't match
        }
        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="").exists())
        # Check that the form has errors
        self.assertContains(response, "error")

    def test_complete_name_view_authenticated(self):
        """Test complete_name view with authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("complete_name"))
        self.assertEqual(response.status_code, 200)

    def test_complete_name_view_anonymous(self):
        """Test complete_name view with anonymous user"""
        response = self.client.get(reverse("complete_name"))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class ProfileViewTest(TestCase):
    """Test cases for profile-related views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            first_name="Jane",
            last_name="Smith",
            password="testpass123",
        )

    def test_view_my_profile_authenticated(self):
        """Test view_my_profile with authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("view_my_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertTrue(response.context["is_own_profile"])

    def test_view_my_profile_anonymous(self):
        """Test view_my_profile with anonymous user"""
        response = self.client.get(reverse("view_my_profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_view_user_profile_valid_user(self):
        """Test view_user_profile with valid user ID"""
        response = self.client.get(
            reverse("view_user_profile", args=[self.other_user.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile_user"], self.other_user)
        self.assertFalse(response.context["is_own_profile"])

    def test_view_user_profile_own_profile(self):
        """Test view_user_profile when viewing own profile"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("view_user_profile", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_own_profile"])

    def test_view_user_profile_invalid_user(self):
        """Test view_user_profile with invalid user ID"""
        response = self.client.get(reverse("view_user_profile", args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_edit_my_profile_get(self):
        """Test edit_my_profile GET request"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("edit_my_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")

    def test_edit_my_profile_post_valid(self):
        """Test edit_my_profile POST with valid data"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "bio": "Updated bio",
            "city": "Stockholm",
            "country": "Sweden",
            "gender": "M",
            "skills_offered": "Python, Django",
            "skills_needed": "JavaScript",
        }
        response = self.client.post(reverse("edit_my_profile"), data)

        self.assertEqual(response.status_code, 302)  # Redirect after successful edit
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "Updated bio")
        self.assertEqual(self.user.profile.city, "Stockholm")

    def test_edit_my_profile_anonymous(self):
        """Test edit_my_profile with anonymous user"""
        response = self.client.get(reverse("edit_my_profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class SkillViewTest(TestCase):
    """Test cases for skill-related views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.skill = Skill.objects.create(
            user=self.user,
            title="Python Programming",
            description="Learn Python basics",
            skill_type="offer",
            category="technology",
        )

    def test_add_skill_get_authenticated(self):
        """Test add_skill GET request with authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("add_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add New Skill")

    def test_add_skill_post_valid(self):
        """Test add_skill POST with valid data"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "Django Web Development",
            "description": "Learn Django framework",
            "skill_type": "offer",
            "category": "technology",
            "location": "Stockholm",
            "availability": "Weekends",
            "is_remote": True,
        }
        response = self.client.post(reverse("add_skill"), data)

        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Skill.objects.filter(title="Django Web Development").exists())

    def test_add_skill_anonymous(self):
        """Test add_skill with anonymous user"""
        response = self.client.get(reverse("add_skill"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_skill_with_next_parameter(self):
        """Test add_skill with next parameter for redirection"""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "Test Skill",
            "description": "Test description",
            "skill_type": "offer",
            "category": "technology",
        }
        response = self.client.post(
            reverse("add_skill") + "?next=view_my_profile", data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("view_my_profile"))

    def test_skills_list_search_no_filters(self):
        """Test skills_list_search without filters"""
        response = self.client.get(reverse("skills_list_search"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")

    def test_skills_list_search_with_filters(self):
        """Test skills_list_search with filters"""
        # Create another skill with different type
        Skill.objects.create(
            user=self.other_user,
            title="Spanish Lessons",
            description="Learn Spanish",
            skill_type="request",
            category="languages",
        )

        # Filter by skill type
        response = self.client.get(reverse("skills_list_search") + "?skill_type=offer")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")
        self.assertNotContains(response, "Spanish Lessons")

    def test_skill_detail_page(self):
        """Test skill_detail_page view"""
        response = self.client.get(reverse("skill_detail_page", args=[self.skill.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")
        self.assertEqual(response.context["skill"], self.skill)

    def test_skill_edit_owner(self):
        """Test skill_edit by skill owner"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("skill_edit", args=[self.skill.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Skill")

    def test_skill_edit_non_owner(self):
        """Test skill_edit by non-owner"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(reverse("skill_edit", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 404)

    def test_delete_skill_owner(self):
        """Test delete_skill by skill owner"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("delete_skill", args=[self.skill.pk]))

        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(
            Skill.objects.filter(pk=self.skill.pk, is_active=True).exists()
        )

    def test_delete_skill_non_owner(self):
        """Test delete_skill by non-owner"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(reverse("delete_skill", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 404)

    def test_my_skills(self):
        """Test my_skills view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("my_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming")


class MessageViewTest(TestCase):
    """Test cases for message-related views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
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
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            skill=self.skill,
            subject="Question",
            message="Hello!",
        )

    def test_send_message_with_skill_id(self):
        """Test send_message view with skill_id"""
        self.client.login(username="sender", password="testpass123")
        response = self.client.get(reverse("send_message", args=[self.skill.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send Message")

    def test_send_message_with_user_id(self):
        """Test send_message view with user_id"""
        self.client.login(username="sender", password="testpass123")
        response = self.client.get(
            reverse("send_message_to_user", args=[self.receiver.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send Message")

    def test_send_message_post_valid(self):
        """Test send_message POST with valid data"""
        self.client.login(username="sender", password="testpass123")
        data = {"subject": "Test Subject", "message": "Test message content"}
        response = self.client.post(reverse("send_message", args=[self.skill.pk]), data)

        self.assertEqual(response.status_code, 302)  # Redirect after sending
        self.assertTrue(Message.objects.filter(subject="Test Subject").exists())

    def test_send_message_anonymous(self):
        """Test send_message with anonymous user"""
        response = self.client.get(reverse("send_message", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_inbox_view(self):
        """Test inbox view"""
        self.client.login(username="receiver", password="testpass123")
        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question")  # Message subject

    def test_sent_messages_view(self):
        """Test sent_messages view"""
        self.client.login(username="sender", password="testpass123")
        response = self.client.get(reverse("sent_messages"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question")  # Message subject


class SearchViewTest(TestCase):
    """Test cases for search functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1", first_name="John", last_name="Doe", password="testpass123"
        )
        self.user1.profile.city = "Stockholm"
        self.user1.profile.country = "Sweden"
        self.user1.profile.save()

        self.user2 = User.objects.create_user(
            username="user2",
            first_name="Jane",
            last_name="Smith",
            password="testpass123",
        )
        self.user2.profile.city = "Oslo"
        self.user2.profile.country = "Norway"
        self.user2.profile.gender = "F"
        self.user2.profile.save()

    def test_search_no_query(self):
        """Test search view without query"""
        response = self.client.get(reverse("search"))

        self.assertEqual(response.status_code, 200)
        # Should show all users when no query
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")

    def test_search_with_name_query(self):
        """Test search with name query"""
        response = self.client.get(reverse("search") + "?search=John")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertNotContains(response, "Jane Smith")

    def test_search_with_location_filter(self):
        """Test search with location filter"""
        response = self.client.get(reverse("search") + "?location=Stockholm")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertNotContains(response, "Jane Smith")

    def test_search_with_gender_filter(self):
        """Test search with gender filter"""
        response = self.client.get(reverse("search") + "?gender=F")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")

    def test_search_combined_filters(self):
        """Test search with multiple filters"""
        response = self.client.get(reverse("search") + "?location=Oslo&gender=F")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")


class ErrorViewTest(TestCase):
    """Test cases for error handling views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_custom_404_view(self):
        """Test custom 404 error page"""
        response = self.client.get("/nonexistent-page/")
        self.assertEqual(response.status_code, 404)

    def test_home_view(self):
        """Test home view"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SkillSwap")


class ViewPermissionTest(TestCase):
    """Test cases for view permissions and access control"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.skill = Skill.objects.create(
            user=self.user,
            title="Test Skill",
            description="Test description",
            skill_type="offer",
            category="technology",
        )

    def test_authenticated_required_views(self):
        """Test views that require authentication"""
        auth_required_urls = [
            reverse("view_my_profile"),
            reverse("edit_my_profile"),
            reverse("add_skill"),
            reverse("my_skills"),
            reverse("inbox"),
            reverse("sent_messages"),
        ]

        for url in auth_required_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                302,
                f"URL {url} should redirect when not authenticated",
            )

    def test_skill_owner_required_views(self):
        """Test views that require skill ownership"""
        other_user = User.objects.create_user(username="other", password="pass123")
        self.client.login(username="other", password="pass123")

        # Should return 404 when trying to edit/delete others' skills
        response = self.client.get(reverse("skill_edit", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse("delete_skill", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 404)


class ViewRedirectionTest(TestCase):
    """Test cases for view redirections and next parameters"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_add_skill_next_parameter(self):
        """Test add_skill redirection with next parameter"""
        self.client.login(username="testuser", password="testpass123")

        # Test different next parameter values
        next_urls = [
            ("view_my_profile", reverse("view_my_profile")),
            ("my_skills", reverse("my_skills")),
            ("skills_list_search", reverse("skills_list_search")),
        ]

        for next_param, expected_redirect in next_urls:
            data = {
                "title": f"Test Skill {next_param}",
                "description": "Test description",
                "skill_type": "offer",
                "category": "technology",
            }
            response = self.client.post(
                reverse("add_skill") + f"?next={next_param}", data
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, expected_redirect)

    def test_add_skill_next_id_parameter(self):
        """Test add_skill redirection with next_id parameter"""
        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "Test Skill",
            "description": "Test description",
            "skill_type": "offer",
            "category": "technology",
        }
        response = self.client.post(
            reverse("add_skill") + f"?next_id={self.user.id}", data
        )

        self.assertEqual(response.status_code, 302)
        expected_url = reverse("view_user_profile", args=[self.user.id])
        self.assertRedirects(response, expected_url)
