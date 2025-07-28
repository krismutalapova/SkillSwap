from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import Profile, Skill, Message, Rating
from decimal import Decimal


class ProfileModelTest(TestCase):
    """Test cases for Profile model functionality"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = self.user.profile  # Auto-created via signal

    def test_profile_auto_creation(self):
        """Test that Profile is automatically created when User is created"""
        new_user = User.objects.create_user(
            username="newuser", email="newuser@example.com", password="newpass123"
        )
        self.assertTrue(hasattr(new_user, "profile"))
        self.assertIsInstance(new_user.profile, Profile)

    def test_profile_string_representation(self):
        """Test Profile __str__ method"""
        self.assertEqual(str(self.profile), "testuser's profile")

    def test_is_profile_complete_empty_profile(self):
        """Test is_profile_complete with empty profile"""
        self.assertFalse(self.profile.is_profile_complete)

    def test_is_profile_complete_partial_profile(self):
        """Test is_profile_complete with partial profile"""
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.profile.city = "Stockholm"
        self.profile.save()
        # Still missing country and skills
        self.assertFalse(self.profile.is_profile_complete)

    def test_is_profile_complete_full_profile(self):
        """Test is_profile_complete with complete profile"""
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.profile.city = "Stockholm"
        self.profile.country = "Sweden"
        self.profile.skills_offered = "Python, Django"
        self.profile.save()
        self.assertTrue(self.profile.is_profile_complete)

    def test_completion_percentage_calculation(self):
        """Test completion percentage calculation"""
        # Empty profile should be 0%
        self.assertEqual(self.profile.completion_percentage, 0)

        # Add fields one by one
        self.user.first_name = "John"
        self.user.save()
        self.assertEqual(
            self.profile.completion_percentage, 12
        )  # 1/8 = 12.5% rounded to 12%

        self.user.last_name = "Doe"
        self.user.save()
        self.assertEqual(self.profile.completion_percentage, 25)  # 2/8 = 25%

        self.profile.city = "Stockholm"
        self.profile.save()
        self.assertEqual(
            self.profile.completion_percentage, 38
        )  # 3/8 = 37.5% rounded to 38%

    def test_missing_required_fields(self):
        """Test missing_required_fields property"""
        missing = self.profile.missing_required_fields
        expected = [
            "First Name",
            "Last Name",
            "City",
            "Country",
            "Skills (offered or needed)",
        ]
        self.assertEqual(set(missing), set(expected))

        # Add some fields
        self.user.first_name = "John"
        self.user.save()
        self.profile.city = "Stockholm"
        self.profile.save()

        missing = self.profile.missing_required_fields
        expected = ["Last Name", "Country", "Skills (offered or needed)"]
        self.assertEqual(set(missing), set(expected))

    def test_missing_critical_fields(self):
        """Test missing_critical_fields property"""
        missing = self.profile.missing_critical_fields
        expected = ["First Name", "Last Name", "City", "Country"]
        self.assertEqual(set(missing), set(expected))

    def test_missing_skills_only(self):
        """Test missing_skills_only property"""
        # With critical fields missing, should be False
        self.assertFalse(self.profile.missing_skills_only)

        # Complete critical fields but no skills
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.profile.city = "Stockholm"
        self.profile.country = "Sweden"
        self.profile.save()

        self.assertTrue(self.profile.missing_skills_only)

        # Add skills
        self.profile.skills_offered = "Python"
        self.profile.save()
        self.assertFalse(self.profile.missing_skills_only)

    def test_completion_status_type(self):
        """Test completion_status_type property"""
        # Empty profile
        self.assertEqual(self.profile.completion_status_type, "critical_missing")

        # Complete critical fields but no skills
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        self.profile.city = "Stockholm"
        self.profile.country = "Sweden"
        self.profile.save()

        self.assertEqual(self.profile.completion_status_type, "skills_missing")

        # Complete profile
        self.profile.skills_offered = "Python"
        self.profile.save()
        self.assertEqual(self.profile.completion_status_type, "complete")

    def test_update_skills_from_skill_objects(self):
        """Test skill synchronization from Skill objects"""
        # Create some skills
        Skill.objects.create(
            user=self.user,
            title="Python Programming",
            description="Web development with Python",
            skill_type="offer",
            category="technology",
        )
        Skill.objects.create(
            user=self.user,
            title="Spanish",
            description="Native Spanish speaker",
            skill_type="request",
            category="languages",
        )

        # Update profile skills
        self.profile.update_skills_from_skill_objects()

        self.assertEqual(self.profile.skills_offered, "Python Programming")
        self.assertEqual(self.profile.skills_needed, "Spanish")

    def test_overall_rating_no_ratings(self):
        """Test overall_rating with no ratings"""
        self.assertEqual(self.profile.overall_rating, 0.0)

    def test_overall_rating_with_ratings(self):
        """Test overall_rating calculation"""
        # Create skills and ratings
        skill1 = Skill.objects.create(
            user=self.user,
            title="Python",
            description="Programming",
            skill_type="offer",
            category="technology",
        )
        skill2 = Skill.objects.create(
            user=self.user,
            title="Django",
            description="Web framework",
            skill_type="offer",
            category="technology",
        )

        rater = User.objects.create_user(username="rater", password="pass123")
        Rating.objects.create(skill=skill1, user=rater, rating=4)
        Rating.objects.create(skill=skill2, user=rater, rating=5)

        # Should be average of 4 and 5 = 4.5
        self.assertEqual(self.profile.overall_rating, 4.5)


class SkillModelTest(TestCase):
    """Test cases for Skill model functionality"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="skilluser", password="testpass123"
        )
        self.skill = Skill.objects.create(
            user=self.user,
            title="Python Programming",
            description="Learn Python from basics to advanced",
            skill_type="offer",
            category="technology",
        )

    def test_skill_creation(self):
        """Test basic skill creation"""
        self.assertEqual(self.skill.title, "Python Programming")
        self.assertEqual(self.skill.skill_type, "offer")
        self.assertEqual(self.skill.category, "technology")
        self.assertTrue(self.skill.is_active)

    def test_skill_string_representation(self):
        """Test Skill __str__ method"""
        expected = "Skill Offered: Python Programming"
        self.assertEqual(str(self.skill), expected)

    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        expected_url = f"/skills/{self.skill.pk}/"
        self.assertEqual(self.skill.get_absolute_url(), expected_url)

    def test_get_category_icon(self):
        """Test get_category_icon method"""
        self.assertEqual(self.skill.get_category_icon(), "fa-solid fa-code")

        # Test with different category
        music_skill = Skill.objects.create(
            user=self.user,
            title="Guitar",
            description="Learn guitar",
            skill_type="offer",
            category="music",
        )
        self.assertEqual(music_skill.get_category_icon(), "fa-solid fa-music")

    def test_average_rating_no_ratings(self):
        """Test average_rating with no ratings"""
        self.assertEqual(self.skill.average_rating, 0.0)

    def test_average_rating_with_ratings(self):
        """Test average_rating calculation"""
        rater1 = User.objects.create_user(username="rater1", password="pass")
        rater2 = User.objects.create_user(username="rater2", password="pass")

        Rating.objects.create(skill=self.skill, user=rater1, rating=4)
        Rating.objects.create(skill=self.skill, user=rater2, rating=5)

        self.assertEqual(self.skill.average_rating, 4.5)

    def test_rating_count(self):
        """Test rating_count property"""
        self.assertEqual(self.skill.rating_count, 0)

        rater = User.objects.create_user(username="rater", password="pass")
        Rating.objects.create(skill=self.skill, user=rater, rating=5)

        self.assertEqual(self.skill.rating_count, 1)

    def test_star_range(self):
        """Test star_range property"""
        expected_range = range(1, 6)
        self.assertEqual(list(self.skill.star_range), list(expected_range))

    def test_skill_ordering(self):
        """Test that skills are ordered by creation date (newest first)"""
        skill2 = Skill.objects.create(
            user=self.user,
            title="Django",
            description="Web framework",
            skill_type="offer",
            category="technology",
        )

        skills = Skill.objects.all()
        self.assertEqual(skills[0], skill2)  # Newest first
        self.assertEqual(skills[1], self.skill)


class MessageModelTest(TestCase):
    """Test cases for Message model functionality"""

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
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            skill=self.skill,
            subject="Question about Python",
            message="Hi, I'd like to learn Python. Can you help?",
        )

    def test_message_creation(self):
        """Test basic message creation"""
        self.assertEqual(self.message.sender, self.sender)
        self.assertEqual(self.message.receiver, self.receiver)
        self.assertEqual(self.message.skill, self.skill)
        self.assertFalse(self.message.is_read)

    def test_message_string_representation(self):
        """Test Message __str__ method"""
        expected = "Message from sender to receiver: Question about Python"
        self.assertEqual(str(self.message), expected)

    def test_message_without_skill(self):
        """Test message creation without associated skill"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject="General question",
            message="Hello!",
        )
        self.assertIsNone(message.skill)

    def test_message_ordering(self):
        """Test that messages are ordered by creation date (newest first)"""
        message2 = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            subject="Reply",
            message="Sure, I can help!",
        )

        messages = Message.objects.all()
        self.assertEqual(messages[0], message2)  # Newest first
        self.assertEqual(messages[1], self.message)


class RatingModelTest(TestCase):
    """Test cases for Rating model functionality"""

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
        self.rating = Rating.objects.create(
            skill=self.skill, user=self.rater, rating=5, comment="Excellent teacher!"
        )

    def test_rating_creation(self):
        """Test basic rating creation"""
        self.assertEqual(self.rating.skill, self.skill)
        self.assertEqual(self.rating.user, self.rater)
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.comment, "Excellent teacher!")

    def test_rating_string_representation(self):
        """Test Rating __str__ method"""
        expected = "rater rated Python: 5/5"
        self.assertEqual(str(self.rating), expected)

    def test_unique_together_constraint(self):
        """Test that a user can only rate a skill once"""
        with self.assertRaises(IntegrityError):
            Rating.objects.create(skill=self.skill, user=self.rater, rating=4)

    def test_rating_choices(self):
        """Test rating value constraints"""
        # Valid ratings (1-5)
        for rating_value in [1, 2, 3, 4, 5]:
            new_rater = User.objects.create_user(
                username=f"rater{rating_value}", password="pass"
            )
            rating = Rating.objects.create(
                skill=self.skill, user=new_rater, rating=rating_value
            )
            self.assertEqual(rating.rating, rating_value)

    def test_rating_ordering(self):
        """Test that ratings are ordered by creation date (newest first)"""
        rater2 = User.objects.create_user(username="rater2", password="pass")
        rating2 = Rating.objects.create(skill=self.skill, user=rater2, rating=4)

        ratings = Rating.objects.all()
        self.assertEqual(ratings[0], rating2)  # Newest first
        self.assertEqual(ratings[1], self.rating)


class SignalTest(TestCase):
    """Test cases for Django signals"""

    def test_profile_creation_signal(self):
        """Test that Profile is created when User is created"""
        self.assertEqual(Profile.objects.count(), 0)

        user = User.objects.create_user(username="testuser", password="testpass123")

        self.assertEqual(Profile.objects.count(), 1)
        self.assertTrue(hasattr(user, "profile"))

    def test_skill_update_profile_signal(self):
        """Test that profile skills are updated when Skill is saved"""
        user = User.objects.create_user(username="testuser", password="pass")
        profile = user.profile

        # Initially no skills
        self.assertEqual(profile.skills_offered, "")
        self.assertEqual(profile.skills_needed, "")

        # Create a skill
        skill = Skill.objects.create(
            user=user,
            title="Python",
            description="Programming",
            skill_type="offer",
            category="technology",
        )

        # Profile should be updated automatically
        profile.refresh_from_db()
        self.assertEqual(profile.skills_offered, "Python")

    def test_skill_delete_profile_signal(self):
        """Test that profile skills are updated when Skill is deleted"""
        user = User.objects.create_user(username="testuser", password="pass")

        skill1 = Skill.objects.create(
            user=user,
            title="Python",
            description="Programming",
            skill_type="offer",
            category="technology",
        )
        skill2 = Skill.objects.create(
            user=user,
            title="JavaScript",
            description="Web dev",
            skill_type="offer",
            category="technology",
        )

        profile = user.profile
        profile.refresh_from_db()
        self.assertIn("Python", profile.skills_offered)
        self.assertIn("JavaScript", profile.skills_offered)

        # Delete one skill
        skill1.delete()

        profile.refresh_from_db()
        self.assertNotIn("Python", profile.skills_offered)
        self.assertIn("JavaScript", profile.skills_offered)
