"""
Django management command to create specific demo users for presentations.
Creates consistent, named users with realistic profiles and skills for demos.

Usage:
    python manage.py create_demo_users
    python manage.py create_demo_users --clear
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Skill, Rating


class Command(BaseCommand):
    help = "Create specific demo users for presentations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing demo users before creating new ones",
        )

    def handle(self, *args, **options):
        clear = options["clear"]

        if clear:
            self.clear_demo_users()

        self.stdout.write(
            self.style.SUCCESS("Creating specific demo users for presentations...")
        )

        demo_users = self.get_demo_user_data()
        created_users = []

        for user_data in demo_users:
            try:
                user = self.create_demo_user(user_data)
                if user:
                    created_users.append(user)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Created demo user: {user.username} ({user.first_name} {user.last_name})"
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating user {user_data['username']}: {str(e)}"
                    )
                )

        # Create cross-user ratings for demo purposes
        if created_users:
            self.create_demo_ratings(created_users)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {len(created_users)} demo users!")
        )
        self.stdout.write(
            self.style.WARNING(
                'Note: All demo users have the password "demo123" for testing'
            )
        )

    def clear_demo_users(self):
        """Clear existing demo users"""
        demo_usernames = [
            "sarah_martinez",
            "marco_rossi",
            "emma_johnson",
            "liam_chen",
            "sofia_andersson",
            "alex_müller",
            "nina_patel",
            "erik_larsson",
            "marie_dubois",
            "carlos_garcia",
            "anna_kowalski",
            "david_smith",
        ]

        demo_users = User.objects.filter(username__in=demo_usernames)
        user_count = demo_users.count()
        demo_users.delete()

        self.stdout.write(
            self.style.SUCCESS(f"Cleared {user_count} existing demo users")
        )

    def get_demo_user_data(self):
        """Define specific demo users for consistent presentations"""
        return [
            {
                "username": "sarah_martinez",
                "email": "sarah.martinez@skillswap.demo",
                "first_name": "Sarah",
                "last_name": "Martinez",
                "profile": {
                    "bio": "Full-stack developer with 5 years of experience in Django and Python. Currently working at a tech startup in Stockholm. Passionate about clean code and helping others learn programming. Looking to learn Italian for my upcoming move to Rome!",
                    "city": "Stockholm",
                    "country": "Sweden",
                    "gender": "F",
                },
                "skills": [
                    {
                        "title": "Django Web Development",
                        "description": "Complete Django framework training from basics to advanced topics. Includes models, views, templates, REST APIs, and deployment strategies.",
                        "skill_type": "offer",
                        "category": "technology",
                        "location": "Stockholm or Remote",
                        "availability": "Evenings and weekends",
                        "is_remote": True,
                    },
                    {
                        "title": "Python Programming Fundamentals",
                        "description": "Learn Python from scratch or improve your existing skills. Perfect for beginners or those transitioning from other languages.",
                        "skill_type": "offer",
                        "category": "technology",
                        "location": "Stockholm or Remote",
                        "availability": "Flexible schedule",
                        "is_remote": True,
                    },
                    {
                        "title": "Italian Conversation Practice",
                        "description": "Looking for native Italian speaker to practice conversation. I'm beginner level but eager to learn for travel and work.",
                        "skill_type": "request",
                        "category": "languages",
                        "location": "Stockholm or Online",
                        "availability": "Evenings preferred",
                        "is_remote": True,
                    },
                ],
            },
            {
                "username": "marco_rossi",
                "email": "marco.rossi@skillswap.demo",
                "first_name": "Marco",
                "last_name": "Rossi",
                "profile": {
                    "bio": "Native Italian speaker and certified language teacher with 8 years of experience. Currently teaching at a language school in Stockholm. Love helping people discover the beauty of Italian language and culture. Interested in learning web development to create language learning tools.",
                    "city": "Stockholm",
                    "country": "Sweden",
                    "gender": "M",
                },
                "skills": [
                    {
                        "title": "Italian Language Lessons",
                        "description": "Complete Italian language instruction from beginner to advanced. Focus on conversation, grammar, and cultural context. Native speaker with teaching certification.",
                        "skill_type": "offer",
                        "category": "languages",
                        "location": "Stockholm or Online",
                        "availability": "Weekdays and weekends",
                        "is_remote": True,
                    },
                    {
                        "title": "Italian Cultural Immersion",
                        "description": "Learn about Italian culture, traditions, food, and travel tips from a native. Perfect complement to language learning.",
                        "skill_type": "offer",
                        "category": "languages",
                        "location": "Stockholm",
                        "availability": "Flexible",
                        "is_remote": False,
                    },
                    {
                        "title": "Web Development Basics",
                        "description": "Complete beginner looking to learn web development. Interested in HTML, CSS, JavaScript, and eventually backend development.",
                        "skill_type": "request",
                        "category": "technology",
                        "location": "Stockholm or Online",
                        "availability": "Evenings and weekends",
                        "is_remote": True,
                    },
                ],
            },
            {
                "username": "emma_johnson",
                "email": "emma.johnson@skillswap.demo",
                "first_name": "Emma",
                "last_name": "Johnson",
                "profile": {
                    "bio": "Senior UI/UX Designer with 7 years of experience creating digital experiences. Currently leading design at a fintech company in London. Passionate about user-centered design and accessibility. Looking to expand into photography for better visual storytelling.",
                    "city": "London",
                    "country": "United Kingdom",
                    "gender": "F",
                },
                "skills": [
                    {
                        "title": "UI/UX Design Fundamentals",
                        "description": "Complete design process from user research to final prototypes. Covers design thinking, wireframing, prototyping, and usability testing.",
                        "skill_type": "offer",
                        "category": "technology",
                        "location": "London or Remote",
                        "availability": "Weekends and some evenings",
                        "is_remote": True,
                    },
                    {
                        "title": "Figma & Design Tools",
                        "description": "Master Figma, Adobe Creative Suite, and other design tools. Learn professional workflows and collaboration techniques.",
                        "skill_type": "offer",
                        "category": "technology",
                        "location": "Remote",
                        "availability": "Flexible",
                        "is_remote": True,
                    },
                    {
                        "title": "Photography Basics",
                        "description": "Complete beginner wanting to learn photography fundamentals. Interested in composition, lighting, and basic editing for professional use.",
                        "skill_type": "request",
                        "category": "music",
                        "location": "London",
                        "availability": "Weekends",
                        "is_remote": False,
                    },
                ],
            },
            {
                "username": "liam_chen",
                "email": "liam.chen@skillswap.demo",
                "first_name": "Liam",
                "last_name": "Chen",
                "profile": {
                    "bio": "Professional photographer and visual artist based in Berlin. Specializing in portrait and event photography with 6 years of experience. Always excited to share photography knowledge and techniques. Looking to learn German to better connect with local clients.",
                    "city": "Berlin",
                    "country": "Germany",
                    "gender": "M",
                },
                "skills": [
                    {
                        "title": "Portrait Photography",
                        "description": "Learn professional portrait photography techniques including lighting, posing, and post-processing. Suitable for beginners to intermediate level.",
                        "skill_type": "offer",
                        "category": "music",
                        "location": "Berlin",
                        "availability": "Weekends",
                        "is_remote": False,
                    },
                    {
                        "title": "Photo Editing with Lightroom",
                        "description": "Master Adobe Lightroom for professional photo editing and workflow management. From basics to advanced techniques.",
                        "skill_type": "offer",
                        "category": "technology",
                        "location": "Berlin or Remote",
                        "availability": "Evenings",
                        "is_remote": True,
                    },
                    {
                        "title": "German Conversation Practice",
                        "description": "English speaker learning German. Looking for conversation practice to improve fluency for business and daily life in Berlin.",
                        "skill_type": "request",
                        "category": "languages",
                        "location": "Berlin",
                        "availability": "Flexible",
                        "is_remote": False,
                    },
                ],
            },
            {
                "username": "sofia_andersson",
                "email": "sofia.andersson@skillswap.demo",
                "first_name": "Sofia",
                "last_name": "Andersson",
                "profile": {
                    "bio": "Professional chef and culinary instructor with 10 years of experience in Nordic cuisine. Runs cooking workshops in Gothenburg. Passionate about sustainable cooking and local ingredients. Interested in learning business skills to expand my culinary ventures.",
                    "city": "Gothenburg",
                    "country": "Sweden",
                    "gender": "F",
                },
                "skills": [
                    {
                        "title": "Nordic Cuisine Cooking",
                        "description": "Learn traditional and modern Nordic cooking techniques. Focus on seasonal ingredients, fermentation, and sustainable practices.",
                        "skill_type": "offer",
                        "category": "cooking",
                        "location": "Gothenburg",
                        "availability": "Weekends",
                        "is_remote": False,
                    },
                    {
                        "title": "Sustainable Cooking Practices",
                        "description": "Learn how to cook sustainably, reduce food waste, and use local, seasonal ingredients for delicious and eco-friendly meals.",
                        "skill_type": "offer",
                        "category": "cooking",
                        "location": "Gothenburg",
                        "availability": "Flexible",
                        "is_remote": False,
                    },
                    {
                        "title": "Small Business Management",
                        "description": "Looking to learn business fundamentals for expanding my culinary business. Interested in marketing, finance, and operations.",
                        "skill_type": "request",
                        "category": "business",
                        "location": "Gothenburg or Online",
                        "availability": "Weekday evenings",
                        "is_remote": True,
                    },
                ],
            },
            {
                "username": "alex_müller",
                "email": "alex.mueller@skillswap.demo",
                "first_name": "Alex",
                "last_name": "Müller",
                "profile": {
                    "bio": "Business consultant and entrepreneur based in Munich. 12 years of experience helping startups and small businesses grow. Specialized in digital marketing and business strategy. Learning guitar in my spare time as a creative outlet.",
                    "city": "Munich",
                    "country": "Germany",
                    "gender": "M",
                },
                "skills": [
                    {
                        "title": "Digital Marketing Strategy",
                        "description": "Complete digital marketing training covering SEO, social media, content marketing, and analytics. Real-world case studies included.",
                        "skill_type": "offer",
                        "category": "business",
                        "location": "Munich or Remote",
                        "availability": "Evenings and weekends",
                        "is_remote": True,
                    },
                    {
                        "title": "Business Plan Development",
                        "description": "Help develop comprehensive business plans, financial projections, and go-to-market strategies for startups and small businesses.",
                        "skill_type": "offer",
                        "category": "business",
                        "location": "Munich or Remote",
                        "availability": "Flexible",
                        "is_remote": True,
                    },
                    {
                        "title": "Guitar Lessons for Beginners",
                        "description": "Complete beginner looking to learn acoustic guitar. Interested in folk and classic rock styles. Prefer in-person lessons.",
                        "skill_type": "request",
                        "category": "music",
                        "location": "Munich",
                        "availability": "Weekend afternoons",
                        "is_remote": False,
                    },
                ],
            },
        ]

    def create_demo_user(self, user_data):
        """Create a single demo user with profile and skills"""
        try:
            # Create user
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password="demo123",
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
            )

            # Update profile (created automatically by signal)
            profile = user.profile
            profile_data = user_data["profile"]
            profile.bio = profile_data["bio"]
            profile.city = profile_data["city"]
            profile.country = profile_data["country"]
            profile.gender = profile_data["gender"]
            profile.save()

            # Create skills
            skills_created = 0
            for skill_data in user_data["skills"]:
                skill = Skill.objects.create(
                    user=user,
                    title=skill_data["title"],
                    description=skill_data["description"],
                    skill_type=skill_data["skill_type"],
                    category=skill_data["category"],
                    location=skill_data["location"],
                    availability=skill_data["availability"],
                    is_remote=skill_data["is_remote"],
                )
                skills_created += 1

            self.stdout.write(
                f"    Created {skills_created} skills for {user.username}"
            )
            return user

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to create user {user_data['username']}: {str(e)}"
                )
            )
            return None

    def create_demo_ratings(self, users):
        """Create realistic cross-ratings between demo users"""
        ratings_created = 0

        # Define some realistic rating scenarios
        rating_scenarios = [
            # Sarah rates Marco's Italian lessons
            (
                "sarah_martinez",
                "marco_rossi",
                "Italian Language Lessons",
                5,
                "Excellent teacher! Marco made learning Italian fun and practical.",
            ),
            # Marco rates Sarah's Django lessons
            (
                "marco_rossi",
                "sarah_martinez",
                "Django Web Development",
                5,
                "Sarah is a fantastic teacher. Clear explanations and great examples.",
            ),
            # Emma rates Liam's photography
            (
                "emma_johnson",
                "liam_chen",
                "Portrait Photography",
                4,
                "Great photography tips! Really helped improve my composition skills.",
            ),
            # Liam rates Emma's UI/UX design
            (
                "liam_chen",
                "emma_johnson",
                "UI/UX Design Fundamentals",
                5,
                "Emma's design process is amazing. Learned so much about user research.",
            ),
            # Sofia rates Alex's business advice
            (
                "sofia_andersson",
                "alex_müller",
                "Digital Marketing Strategy",
                4,
                "Very practical marketing advice that I can apply to my cooking business.",
            ),
            # Alex rates Sofia's cooking
            (
                "alex_müller",
                "sofia_andersson",
                "Nordic Cuisine Cooking",
                5,
                "Amazing cooking class! Sofia's Nordic techniques are incredible.",
            ),
        ]

        for (
            rater_username,
            skill_owner_username,
            skill_title,
            rating_value,
            comment,
        ) in rating_scenarios:
            try:
                rater = User.objects.get(username=rater_username)
                skill = Skill.objects.get(
                    user__username=skill_owner_username, title=skill_title
                )

                rating, created = Rating.objects.get_or_create(
                    skill=skill,
                    user=rater,
                    defaults={
                        "rating": rating_value,
                        "comment": comment,
                    },
                )
                if created:
                    ratings_created += 1

            except (User.DoesNotExist, Skill.DoesNotExist) as e:
                self.stdout.write(f"    Could not create rating: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Created {ratings_created} demo ratings"))
