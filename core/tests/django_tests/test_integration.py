from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Profile, Skill, Message, Rating
from django.db import transaction
import time


class UserRegistrationWorkflowTest(TestCase):
    """Test complete user registration and profile setup workflow"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_complete_user_registration_workflow(self):
        """Test complete user registration → profile setup → skill creation workflow"""

        # Step 1: User registration
        signup_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        response = self.client.post(reverse("signup"), signup_data)

        # Should redirect after successful signup
        self.assertEqual(response.status_code, 302)

        # Verify user was created
        user = User.objects.get(username="newuser")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

        # Verify profile was auto-created
        self.assertTrue(hasattr(user, "profile"))
        profile = user.profile
        self.assertFalse(profile.is_profile_complete)

        # Step 2: User login
        login_success = self.client.login(username="newuser", password="complexpass123")
        self.assertTrue(login_success)

        # Step 3: Complete profile
        profile_data = {
            "bio": "I am a software developer interested in learning new skills.",
            "city": "Stockholm",
            "country": "Sweden",
            "gender": "M",
            "skills_offered": "Python, Django, Web Development",
            "skills_needed": "Machine Learning, Data Science",
        }
        response = self.client.post(reverse("edit_my_profile"), profile_data)
        self.assertEqual(response.status_code, 302)

        # Verify profile completion
        profile.refresh_from_db()
        self.assertTrue(profile.is_profile_complete)
        self.assertEqual(profile.completion_status_type, "complete")

        # Step 4: Create first skill
        skill_data = {
            "title": "Python Programming for Beginners",
            "description": "I can teach Python basics to complete beginners.",
            "skill_type": "offer",
            "category": "technology",
            "location": "Stockholm, Sweden",
            "availability": "Weekends",
            "is_remote": True,
        }
        response = self.client.post(reverse("add_skill"), skill_data)
        self.assertEqual(response.status_code, 302)

        # Verify skill creation
        skill = Skill.objects.get(title="Python Programming for Beginners")
        self.assertEqual(skill.user, user)
        self.assertEqual(skill.skill_type, "offer")

        # Step 5: Create second skill (request)
        skill_request_data = {
            "title": "Machine Learning Basics",
            "description": "I want to learn the fundamentals of machine learning.",
            "skill_type": "request",
            "category": "technology",
            "is_remote": True,
        }
        response = self.client.post(reverse("add_skill"), skill_request_data)
        self.assertEqual(response.status_code, 302)

        # Verify profile skills were updated via signals
        profile.refresh_from_db()
        self.assertIn("Python Programming for Beginners", profile.skills_offered)
        self.assertIn("Machine Learning Basics", profile.skills_needed)

        # Step 6: View own profile
        response = self.client.get(reverse("view_my_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Programming for Beginners")
        self.assertContains(response, "Machine Learning Basics")


class SkillDiscoveryWorkflowTest(TestCase):
    """Test skill discovery and search functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        # Create users with different skills and profiles
        self.user1 = User.objects.create_user(
            username="pythondev",
            first_name="Alice",
            last_name="Smith",
            password="testpass123",
        )
        self.user1.profile.city = "Stockholm"
        self.user1.profile.country = "Sweden"
        self.user1.profile.gender = "F"
        self.user1.profile.save()

        self.user2 = User.objects.create_user(
            username="jsdev",
            first_name="Bob",
            last_name="Johnson",
            password="testpass123",
        )
        self.user2.profile.city = "Oslo"
        self.user2.profile.country = "Norway"
        self.user2.profile.gender = "M"
        self.user2.profile.save()

        # Create skills
        self.python_skill = Skill.objects.create(
            user=self.user1,
            title="Advanced Python Programming",
            description="Learn advanced Python concepts",
            skill_type="offer",
            category="technology",
            location="Stockholm",
            is_remote=True,
        )

        self.js_skill = Skill.objects.create(
            user=self.user2,
            title="JavaScript and React",
            description="Modern JavaScript and React development",
            skill_type="offer",
            category="technology",
            location="Oslo",
            is_remote=False,
        )

        self.cooking_skill = Skill.objects.create(
            user=self.user1,
            title="Italian Cooking",
            description="Learn to cook authentic Italian dishes",
            skill_type="offer",
            category="cooking",
            location="Stockholm",
            is_remote=False,
        )

    def test_skill_search_workflow(self):
        """Test complete skill search and discovery workflow"""

        # Step 1: Browse all skills
        response = self.client.get(reverse("skills_list_search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Python Programming")
        self.assertContains(response, "JavaScript and React")
        self.assertContains(response, "Italian Cooking")

        # Step 2: Filter by skill type (offers only)
        response = self.client.get(reverse("skills_list_search") + "?skill_type=offer")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Python Programming")

        # Step 3: Filter by category (technology)
        response = self.client.get(
            reverse("skills_list_search") + "?category=technology"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Python Programming")
        self.assertContains(response, "JavaScript and React")
        self.assertNotContains(response, "Italian Cooking")

        # Step 4: Search by keyword
        response = self.client.get(reverse("skills_list_search") + "?search=Python")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Python Programming")
        self.assertNotContains(response, "JavaScript and React")

        # Step 5: Combined filters
        response = self.client.get(
            reverse("skills_list_search")
            + "?skill_type=offer&category=technology&search=JavaScript"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "JavaScript and React")
        self.assertNotContains(response, "Advanced Python Programming")

        # Step 6: View skill detail
        response = self.client.get(
            reverse("skill_detail_page", args=[self.python_skill.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Advanced Python Programming")
        self.assertContains(response, "Alice Smith")

    def test_user_search_workflow(self):
        """Test user discovery and search workflow"""

        # Step 1: Browse all users
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Bob Johnson")

        # Step 2: Search by name
        response = self.client.get(reverse("search") + "?search=Alice")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertNotContains(response, "Bob Johnson")

        # Step 3: Filter by location
        response = self.client.get(reverse("search") + "?location=Stockholm")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertNotContains(response, "Bob Johnson")

        # Step 4: Filter by gender
        response = self.client.get(reverse("search") + "?gender=F")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertNotContains(response, "Bob Johnson")

        # Step 5: View user profile
        response = self.client.get(reverse("view_user_profile", args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Stockholm")


class MessagingWorkflowTest(TestCase):
    """Test complete messaging system workflow"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.sender = User.objects.create_user(
            username="sender",
            first_name="John",
            last_name="Sender",
            password="testpass123",
        )

        self.receiver = User.objects.create_user(
            username="receiver",
            first_name="Jane",
            last_name="Receiver",
            password="testpass123",
        )

        self.skill = Skill.objects.create(
            user=self.receiver,
            title="Python Tutoring",
            description="Learn Python programming",
            skill_type="offer",
            category="technology",
        )

    def test_complete_messaging_workflow(self):
        """Test complete messaging workflow: skill discovery → contact → message exchange"""

        # Step 1: Sender discovers skill
        response = self.client.get(reverse("skill_detail_page", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Tutoring")

        # Step 2: Sender logs in and sends message
        self.client.login(username="sender", password="testpass123")

        message_data = {
            "subject": "Interested in Python tutoring",
            "message": "Hi Jane, I saw your Python tutoring offer and I'm very interested. I'm a complete beginner and would love to learn. Are you available for sessions?",
        }
        response = self.client.post(
            reverse("send_message_skill", args=[self.skill.pk]), message_data
        )
        self.assertEqual(response.status_code, 302)

        # Verify message creation
        message = Message.objects.get(subject="Interested in Python tutoring")
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.skill, self.skill)
        self.assertFalse(message.is_read)

        # Step 3: Check sender's sent messages
        response = self.client.get(reverse("sent_messages"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Interested in Python tutoring")

        # Step 4: Receiver logs in and checks inbox
        self.client.logout()
        self.client.login(username="receiver", password="testpass123")

        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Interested in Python tutoring")
        self.assertContains(response, "John Sender")

        # Step 5: Receiver replies via direct message to user
        reply_data = {
            "subject": "Re: Interested in Python tutoring",
            "message": "Hi John! I'd be happy to help you learn Python. I have availability on weekends. Let's schedule a session!",
        }
        response = self.client.post(
            reverse("send_message_user", args=[self.sender.pk]), reply_data
        )
        self.assertEqual(response.status_code, 302)

        # Step 6: Verify reply was sent
        reply_message = Message.objects.get(subject="Re: Interested in Python tutoring")
        self.assertEqual(reply_message.sender, self.receiver)
        self.assertEqual(reply_message.receiver, self.sender)

        # Step 7: Sender sees reply in inbox
        self.client.logout()
        self.client.login(username="sender", password="testpass123")

        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Re: Interested in Python tutoring")


class RatingWorkflowTest(TestCase):
    """Test skill rating and review workflow"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.skill_owner = User.objects.create_user(
            username="teacher",
            first_name="Alice",
            last_name="Teacher",
            password="testpass123",
        )

        self.student1 = User.objects.create_user(
            username="student1", password="testpass123"
        )

        self.student2 = User.objects.create_user(
            username="student2", password="testpass123"
        )

        self.skill = Skill.objects.create(
            user=self.skill_owner,
            title="Python Programming",
            description="Learn Python from scratch",
            skill_type="offer",
            category="technology",
        )

    def test_rating_and_review_workflow(self):
        """Test complete rating workflow: skill interaction → rating → calculations"""

        # Step 1: Students rate the skill
        rating1 = Rating.objects.create(
            skill=self.skill,
            user=self.student1,
            rating=5,
            comment="Excellent teacher! Very clear explanations.",
        )

        rating2 = Rating.objects.create(
            skill=self.skill,
            user=self.student2,
            rating=4,
            comment="Good course, learned a lot.",
        )

        # Step 2: Verify rating calculations
        self.assertEqual(self.skill.average_rating, 4.5)  # (5 + 4) / 2
        self.assertEqual(self.skill.rating_count, 2)

        # Step 3: Check profile overall rating
        profile_rating = self.skill_owner.profile.overall_rating
        self.assertEqual(profile_rating, 4.5)

        # Step 4: View skill detail page with ratings
        response = self.client.get(reverse("skill_detail_page", args=[self.skill.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Excellent teacher")
        self.assertContains(response, "Good course")

        # Step 5: Add third rating
        student3 = User.objects.create_user(username="student3", password="testpass123")
        Rating.objects.create(
            skill=self.skill, user=student3, rating=3, comment="Average experience."
        )

        # Step 6: Verify updated calculations
        self.skill.refresh_from_db()
        expected_average = (5 + 4 + 3) / 3  # 4.0
        self.assertEqual(self.skill.average_rating, 4.0)
        self.assertEqual(self.skill.rating_count, 3)


class ProfileCompletionWorkflowTest(TestCase):
    """Test profile completion tracking and status updates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile = self.user.profile

    def test_profile_completion_progression(self):
        """Test profile completion status as user adds information"""

        # Step 1: Initial state - empty profile
        self.assertFalse(self.profile.is_profile_complete)
        self.assertEqual(self.profile.completion_status_type, "critical_missing")
        self.assertEqual(self.profile.completion_percentage, 0)

        missing_fields = self.profile.missing_required_fields
        self.assertIn("First Name", missing_fields)
        self.assertIn("Last Name", missing_fields)
        self.assertIn("City", missing_fields)
        self.assertIn("Country", missing_fields)
        self.assertIn("Skills (offered or needed)", missing_fields)

        # Step 2: Add names
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()

        # Should still be critical_missing (location fields missing)
        self.assertEqual(self.profile.completion_status_type, "critical_missing")
        self.assertEqual(self.profile.completion_percentage, 25)  # 2/8 fields

        # Step 3: Add location
        self.profile.city = "Stockholm"
        self.profile.country = "Sweden"
        self.profile.save()

        # Should now be skills_missing
        self.assertEqual(self.profile.completion_status_type, "skills_missing")
        self.assertTrue(self.profile.missing_skills_only)
        self.assertEqual(self.profile.completion_percentage, 50)  # 4/8 fields

        # Step 4: Add skills
        self.profile.skills_offered = "Python, Django"
        self.profile.save()

        # Should now be complete
        self.assertTrue(self.profile.is_profile_complete)
        self.assertEqual(self.profile.completion_status_type, "complete")
        self.assertEqual(self.profile.completion_percentage, 62)  # 5/8 fields

        # Step 5: Add optional fields
        self.profile.bio = "Software developer"
        self.profile.save()

        self.assertEqual(self.profile.completion_percentage, 75)  # 6/8 fields


class SkillSynchronizationTest(TestCase):
    """Test skill synchronization between Profile and Skill models"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile = self.user.profile

    def test_skill_synchronization_workflow(self):
        """Test that profile skills stay synchronized with Skill objects"""

        # Step 1: Initially no skills
        self.assertEqual(self.profile.skills_offered, "")
        self.assertEqual(self.profile.skills_needed, "")

        # Step 2: Create offer skill
        skill1 = Skill.objects.create(
            user=self.user,
            title="Python Programming",
            description="Web development",
            skill_type="offer",
            category="technology",
        )

        # Profile should be updated automatically via signal
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.skills_offered, "Python Programming")

        # Step 3: Create request skill
        skill2 = Skill.objects.create(
            user=self.user,
            title="Machine Learning",
            description="Want to learn ML",
            skill_type="request",
            category="technology",
        )

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.skills_needed, "Machine Learning")

        # Step 4: Create multiple skills of same type
        skill3 = Skill.objects.create(
            user=self.user,
            title="Django Framework",
            description="Web framework",
            skill_type="offer",
            category="technology",
        )

        self.profile.refresh_from_db()
        offered_skills = self.profile.skills_offered.split(", ")
        self.assertIn("Python Programming", offered_skills)
        self.assertIn("Django Framework", offered_skills)

        # Step 5: Deactivate a skill
        skill1.is_active = False
        skill1.save()

        self.profile.refresh_from_db()
        self.assertNotIn("Python Programming", self.profile.skills_offered)
        self.assertIn("Django Framework", self.profile.skills_offered)

        # Step 6: Delete a skill
        skill3.delete()

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.skills_offered, "")  # No active offer skills left


class CrossBrowserCompatibilityTest(TestCase):
    """Test key workflows work across different scenarios"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_anonymous_user_experience(self):
        """Test that anonymous users can browse but not interact"""

        # Create some public content
        user = User.objects.create_user(username="testuser", password="pass123")
        skill = Skill.objects.create(
            user=user,
            title="Test Skill",
            description="Description",
            skill_type="offer",
            category="technology",
        )

        # Anonymous users can view public pages
        public_urls = [
            reverse("home"),
            reverse("skills_list_search"),
            reverse("skill_detail_page", args=[skill.pk]),
            reverse("search"),
            reverse("view_user_profile", args=[user.pk]),
        ]

        for url in public_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])  # 200 OK or 302 redirect

        # Anonymous users are redirected for protected pages
        protected_urls = [
            reverse("view_my_profile"),
            reverse("edit_my_profile"),
            reverse("add_skill"),
            reverse("my_skills"),
            reverse("inbox"),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_data_consistency_across_operations(self):
        """Test that data remains consistent across different operations"""

        user = User.objects.create_user(username="testuser", password="pass123")

        # Test transaction consistency
        with transaction.atomic():
            skill = Skill.objects.create(
                user=user,
                title="Atomic Skill",
                description="Test atomic operations",
                skill_type="offer",
                category="technology",
            )

            # Profile should be updated within the same transaction
            user.profile.refresh_from_db()
            self.assertIn("Atomic Skill", user.profile.skills_offered)

        # Verify data persisted correctly
        user.profile.refresh_from_db()
        self.assertIn("Atomic Skill", user.profile.skills_offered)

        # Test cascading deletes
        user_id = user.id
        profile_id = user.profile.id
        skill_id = skill.id

        user.delete()

        # All related objects should be deleted
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(Profile.objects.filter(id=profile_id).exists())
        self.assertFalse(Skill.objects.filter(id=skill_id).exists())
