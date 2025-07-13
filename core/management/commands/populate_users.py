"""
Django management command to populate the SkillSwap platform with sample users.
Usage:
    python manage.py populate_users
    python manage.py populate_users --count 50
    python manage.py populate_users --clear
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = "Populate the platform with sample users and profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of users to create (default: 20)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing sample users before creating new ones",
        )

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]

        if clear:
            self.clear_sample_users()

        self.stdout.write(self.style.SUCCESS(f"Creating {count} sample users..."))

        created_count = 0
        for i in range(count):
            try:
                user_data = self.generate_user_data(i)
                if self.create_user_and_profile(user_data):
                    created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating user {i+1}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} users with profiles!"
            )
        )
        self.stdout.write(
            self.style.WARNING(
                'Note: All users have the password "skillswap123" for testing'
            )
        )

    def clear_sample_users(self):
        sample_users = User.objects.filter(username__startswith="user").exclude(
            is_superuser=True
        )

        count = sample_users.count()
        sample_users.delete()

        self.stdout.write(self.style.SUCCESS(f"Cleared {count} existing sample users"))

    def generate_user_data(self, index):

        first_names = [
            "Alex",
            "Taylor",
            "Jordan",
            "Casey",
            "Morgan",
            "Riley",
            "Avery",
            "Cameron",
            "Quinn",
            "Sage",
            "Robin",
            "Dana",
            "Jamie",
            "Skylar",
            "Parker",
            "Blake",
            "Drew",
            "Hayden",
            "Kendall",
            "Reese",
            "Sam",
            "Kai",
            "River",
            "Phoenix",
            "Emery",
            "Rowan",
            "Finley",
            "Charlie",
            "Elliot",
            "Harley",
            "Luna",
            "Nova",
            "Sage",
            "Ari",
        ]

        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
            "Walker",
            "Young",
            "Allen",
            "King",
            "Wright",
        ]

        cities = [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
            "Austin",
            "Jacksonville",
            "Fort Worth",
            "Columbus",
            "Charlotte",
            "San Francisco",
            "Indianapolis",
            "Seattle",
            "Denver",
            "Washington",
            "Boston",
            "Nashville",
            "Baltimore",
            "Portland",
            "Las Vegas",
            "Detroit",
            "Memphis",
            "Louisville",
            "Milwaukee",
            "Albuquerque",
            "Stockholm",
            "London",
            "Berlin",
            "Paris",
            "Tokyo",
            "Sydney",
            "Toronto",
            "Vancouver",
            "Amsterdam",
            "Barcelona",
        ]

        countries = [
            "United States",
            "Canada",
            "United Kingdom",
            "Germany",
            "France",
            "Netherlands",
            "Sweden",
            "Australia",
            "Japan",
            "Spain",
            "Italy",
            "Brazil",
            "Mexico",
            "India",
            "South Korea",
        ]

        skills_offered = [
            "Python Programming",
            "Web Development",
            "Graphic Design",
            "Digital Marketing",
            "Data Analysis",
            "Photography",
            "Writing",
            "Language Translation",
            "Music Production",
            "Video Editing",
            "Cooking",
            "Gardening",
            "Fitness Training",
            "Yoga Instruction",
            "Public Speaking",
            "Project Management",
            "UI/UX Design",
            "Machine Learning",
            "Mobile App Development",
            "SEO Optimization",
            "Social Media Management",
            "Content Creation",
            "Illustration",
            "Voice Acting",
            "Podcast Production",
            "Event Planning",
            "Financial Planning",
            "Legal Advice",
            "Career Coaching",
            "Guitar Lessons",
            "Piano Lessons",
            "Dance Instruction",
            "Art Therapy",
            "Life Coaching",
            "Business Strategy",
        ]

        skills_needed = [
            "JavaScript",
            "React Development",
            "Database Design",
            "Cloud Computing",
            "Cybersecurity",
            "DevOps",
            "AI/ML",
            "Blockchain Development",
            "Mobile Development",
            "Game Development",
            "Foreign Languages",
            "Public Speaking",
            "Leadership Skills",
            "Negotiation",
            "Time Management",
            "Creative Writing",
            "Video Production",
            "Podcasting",
            "Social Media Strategy",
            "Email Marketing",
            "Sales Techniques",
            "Customer Service",
            "Meditation",
            "Mindfulness",
            "Stress Management",
            "Nutrition",
            "Interior Design",
            "Fashion Design",
            "Woodworking",
            "Electronics",
            "Car Maintenance",
            "Home Renovation",
            "Investment Strategies",
            "Cryptocurrency",
            "Real Estate",
        ]

        bio_templates = [
            "Passionate about {interest} and always eager to learn new skills. I believe in the power of sharing knowledge to build stronger communities.",
            "Experienced {profession} looking to expand my skillset and connect with like-minded individuals. Love helping others achieve their goals!",
            "Creative soul with expertise in {skill}. Always excited to teach what I know and learn something new in return.",
            "Technology enthusiast and {profession}. I enjoy solving problems and sharing innovative solutions with others.",
            "Lifelong learner with a background in {field}. I'm here to both share my experience and discover new passions.",
            "Professional {title} who believes that everyone has something valuable to teach. Let's learn together!",
            "Dedicated to personal growth and helping others succeed. My expertise in {area} has taught me the value of collaboration.",
            "Entrepreneur and creative thinker passionate about {topic}. I love connecting with people and exchanging knowledge.",
        ]

        professions = [
            "software developer",
            "designer",
            "teacher",
            "consultant",
            "entrepreneur",
            "artist",
            "writer",
            "photographer",
            "marketer",
            "analyst",
            "coach",
            "freelancer",
        ]

        interests = [
            "technology",
            "arts",
            "education",
            "wellness",
            "creativity",
            "innovation",
            "sustainability",
            "community building",
        ]

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"user{index+1:03d}"
        email = f"{username}@skillswap.demo"

        offered_skills = random.sample(skills_offered, random.randint(2, 5))
        needed_skills = random.sample(skills_needed, random.randint(1, 4))

        bio_template = random.choice(bio_templates)
        bio_vars = {
            "interest": random.choice(interests),
            "profession": random.choice(professions),
            "skill": random.choice(offered_skills),
            "field": random.choice(["technology", "design", "business", "education"]),
            "title": random.choice(professions),
            "area": random.choice(offered_skills),
            "topic": random.choice(interests),
        }

        bio = bio_template.format(**bio_vars)

        return {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": "skillswap123",
            "profile": {
                "bio": bio,
                "city": random.choice(cities),
                "country": random.choice(countries),
                "gender": random.choice(["M", "F", "O"]),
                "skills_offered": ", ".join(offered_skills),
                "skills_needed": ", ".join(needed_skills),
            },
        }

    def create_user_and_profile(self, user_data):
        if User.objects.filter(username=user_data["username"]).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User {user_data['username']} already exists, skipping..."
                )
            )
            return False

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )
        try:
            profile = Profile.objects.get(user=user)
            profile.bio = user_data["profile"]["bio"]
            profile.city = user_data["profile"]["city"]
            profile.country = user_data["profile"]["country"]
            profile.gender = user_data["profile"]["gender"]
            profile.skills_offered = user_data["profile"]["skills_offered"]
            profile.skills_needed = user_data["profile"]["skills_needed"]
            profile.save()

            self.stdout.write(
                f"✓ Created user: {user.username} ({user.first_name} {user.last_name})"
            )
            return True

        except Profile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Profile not found for user {user.username}")
            )
            return False
