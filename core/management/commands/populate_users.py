"""
Django management command to populate the SkillSwap platform with sample users and skills.
Creates users with complete profiles and individual Skill objects properly categorized.
Usage:
    python manage.py populate_users
    python manage.py populate_users --count 50
    python manage.py populate_users --clear
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Skill, Rating


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
        all_users = []
        for i in range(count):
            try:
                user_data = self.generate_user_data(i)
                user = self.create_user_and_profile(user_data)
                if user:
                    all_users.append(user)
                    created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating user {i+1}: {str(e)}")
                )

        # Create ratings for skills after all users are created
        if all_users:
            self.stdout.write(self.style.SUCCESS("Creating skill ratings..."))
            ratings_created = self.create_skill_ratings(all_users)
            self.stdout.write(
                self.style.SUCCESS(f"Created {ratings_created} ratings for skills")
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

        skill_count = Skill.objects.filter(user__in=sample_users).count()
        rating_count = Rating.objects.filter(skill__user__in=sample_users).count()
        user_count = sample_users.count()

        sample_users.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Cleared {user_count} existing sample users, {skill_count} associated skills, and {rating_count} ratings"
            )
        )

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

        locations = {
            "United Kingdom": [
                "London",
                "Manchester",
                "Birmingham",
                "Liverpool",
                "Edinburgh",
                "Glasgow",
            ],
            "Germany": [
                "Berlin",
                "Munich",
                "Hamburg",
                "Cologne",
                "Frankfurt",
            ],
            "France": [
                "Paris",
                "Lyon",
                "Marseille",
                "Toulouse",
                "Nice",
            ],
            "Netherlands": [
                "Amsterdam",
                "Rotterdam",
                "The Hague",
                "Utrecht",
                "Eindhoven",
            ],
            "Sweden": [
                "Stockholm",
                "Gothenburg",
                "Malmö",
                "Uppsala",
                "Linköping",
            ],
            "Spain": [
                "Madrid",
                "Barcelona",
                "Valencia",
                "Seville",
                "Zaragoza",
                "Alicante",
            ],
            "Italy": [
                "Rome",
                "Milan",
                "Naples",
                "Turin",
                "Palermo",
            ],
            "Poland": [
                "Warsaw",
                "Kraków",
                "Łódź",
                "Wrocław",
                "Poznań",
                "Gdańsk",
            ],
        }

        # Skills with their categories - structured for proper Skill model creation
        skills_data = {
            "technology": [
                "Python Programming",
                "Web Development",
                "JavaScript",
                "React Development",
                "Database Design",
                "Machine Learning",
                "Mobile App Development",
                "UI/UX Design",
                "Cloud Computing",
                "Cybersecurity",
                "DevOps",
                "AI/ML",
                "Blockchain Development",
                "Game Development",
                "SEO Optimization",
            ],
            "business": [
                "Digital Marketing",
                "Data Analysis",
                "Project Management",
                "Social Media Management",
                "Financial Planning",
                "Business Strategy",
                "Sales Techniques",
                "Customer Service",
                "Investment Strategies",
                "Real Estate",
                "Email Marketing",
                "Leadership Skills",
                "Negotiation",
            ],
            "music": [
                "Music Production",
                "Guitar Lessons",
                "Piano Lessons",
                "Voice Acting",
                "Podcast Production",
                "Video Production",
                "Podcasting",
                "Dance Instruction",
                "Art Therapy",
                "Illustration",
            ],
            "academic": [
                "Writing",
                "Language Translation",
                "Public Speaking",
                "Creative Writing",
                "Foreign Languages",
                "Time Management",
                "Career Coaching",
                "Life Coaching",
                "Legal Advice",
            ],
            "health": [
                "Fitness Training",
                "Yoga Instruction",
                "Meditation",
                "Mindfulness",
                "Stress Management",
                "Nutrition",
            ],
            "cooking": [
                "Cooking",
                "Baking",
                "Meal Planning",
                "Food Photography",
                "Wine Tasting",
            ],
            "crafts": [
                "Gardening",
                "Woodworking",
                "Interior Design",
                "Home Renovation",
                "Electronics",
                "Car Maintenance",
            ],
            "fashion": [
                "Fashion Design",
                "Personal Styling",
                "Makeup Artistry",
                "Photography",
            ],
            "other": [
                "Photography",
                "Video Editing",
                "Content Creation",
                "Event Planning",
                "Cryptocurrency",
            ],
        }

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

        # Flatten skills data for bio generation
        all_skills = []
        for category_skills in skills_data.values():
            all_skills.extend(category_skills)

        bio_template = random.choice(bio_templates)
        bio_vars = {
            "interest": random.choice(interests),
            "profession": random.choice(professions),
            "skill": random.choice(all_skills),
            "field": random.choice(["technology", "design", "business", "education"]),
            "title": random.choice(professions),
            "area": random.choice(all_skills),
            "topic": random.choice(interests),
        }

        bio = bio_template.format(**bio_vars)

        # Select a random country and then a random city from that country
        country = random.choice(list(locations.keys()))
        city = random.choice(locations[country])

        return {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": "skillswap123",
            "profile": {
                "bio": bio,
                "city": city,
                "country": country,
                "gender": random.choice(["M", "F", "O"]),
                "skills_offered": "",  # Will be populated as individual Skill objects
                "skills_needed": "",  # Will be populated as individual Skill objects
            },
            "skills_data": skills_data,  # Pass skills data for Skill object creation
        }

    def create_user_and_profile(self, user_data):
        if User.objects.filter(username=user_data["username"]).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User {user_data['username']} already exists, skipping..."
                )
            )
            return None

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

            # Create individual Skill objects
            skills_created = self.create_user_skills(
                user, user_data["skills_data"], user_data["profile"]
            )

            self.stdout.write(
                f"✓ Created user: {user.username} ({user.first_name} {user.last_name}) with {skills_created} skills"
            )
            return user

        except Profile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Profile not found for user {user.username}")
            )
            return None

    def create_user_skills(self, user, skills_data, profile_data):
        skills_created = 0

        # Generate skill descriptions templates
        offer_descriptions = [
            "I have extensive experience in {skill} and would love to share my knowledge with others.",
            "Been working with {skill} for several years and enjoy teaching others.",
            "Passionate about {skill} and always excited to help fellow learners.",
            "Professional experience in {skill} - happy to mentor and guide others.",
            "Love sharing my {skill} expertise and helping others grow their skills.",
        ]

        request_descriptions = [
            "Looking to learn {skill} from someone with real experience.",
            "Interested in developing my {skill} abilities with proper guidance.",
            "Would love to find a mentor to help me master {skill}.",
            "Eager to learn {skill} and willing to exchange knowledge in return.",
            "Seeking guidance in {skill} to advance my skill set.",
        ]

        # Availability options
        availability_options = [
            "Weekends",
            "Evenings",
            "Flexible schedule",
            "Weekdays only",
            "By appointment",
            "Morning hours preferred",
        ]

        # Create 2-4 offered skills
        offered_count = random.randint(2, 4)
        created_categories = []

        for _ in range(offered_count):
            # Select a random category that hasn't been used yet
            available_categories = [
                cat for cat in skills_data.keys() if cat not in created_categories
            ]
            if not available_categories:
                break

            category = random.choice(available_categories)
            created_categories.append(category)
            skill_title = random.choice(skills_data[category])

            description = random.choice(offer_descriptions).format(skill=skill_title)

            # Improved location and remote logic
            delivery_type = random.choice(
                ["online_only", "in_person_only", "both_options", "flexible"]
            )

            if delivery_type == "online_only":
                location_choice = "Online"
                is_remote = True
            elif delivery_type == "in_person_only":
                # In-person requires a specific location - use the user's location
                location_choice = f"{profile_data['city']}, {profile_data['country']}"
                is_remote = False
            elif delivery_type == "both_options":
                # Both options - provide location but also available online
                location_choice = f"{profile_data['city']}, {profile_data['country']} (also available online)"
                is_remote = True
            else:  # flexible
                # Can adapt to student's preference
                location_choice = f"Flexible - {profile_data['city']}, {profile_data['country']} or online"
                is_remote = True

            skill = Skill.objects.create(
                user=user,
                title=skill_title,
                description=description,
                skill_type="offer",
                category=category,
                location=location_choice,
                availability=random.choice(availability_options),
                is_remote=is_remote,
            )
            skills_created += 1

        # Create 1-3 requested skills
        requested_count = random.randint(1, 3)

        for _ in range(requested_count):
            category = random.choice(list(skills_data.keys()))
            skill_title = random.choice(skills_data[category])

            description = random.choice(request_descriptions).format(skill=skill_title)

            # Improved location and remote
            delivery_type = random.choice(
                ["online_only", "in_person_only", "both_options", "flexible"]
            )

            if delivery_type == "online_only":
                location_choice = "Online"
                is_remote = True
            elif delivery_type == "in_person_only":
                # In-person requires a specific location - use the user's location
                location_choice = f"{profile_data['city']}, {profile_data['country']}"
                is_remote = False
            elif delivery_type == "both_options":
                # Both options - provide location but also available online
                location_choice = f"{profile_data['city']}, {profile_data['country']} (also available online)"
                is_remote = True
            else:  # flexible
                # Can adapt to teacher's preference
                location_choice = f"Flexible - {profile_data['city']}, {profile_data['country']} or online"
                is_remote = True

            skill = Skill.objects.create(
                user=user,
                title=skill_title,
                description=description,
                skill_type="request",
                category=category,
                location=location_choice,
                availability=random.choice(availability_options),
                is_remote=is_remote,
            )
            skills_created += 1

        return skills_created

    def create_skill_ratings(self, all_users):
        """Create ratings for offered skills from other users"""
        ratings_created = 0

        # Get all offered skills
        offered_skills = Skill.objects.filter(
            user__in=all_users, skill_type="offer", is_active=True
        )

        if not offered_skills.exists():
            return 0

        rating_comments = [
            "Great teacher! Very patient and knowledgeable.",
            "Excellent experience. Learned a lot in a short time.",
            "Really helpful and explained concepts clearly.",
            "Fantastic mentor! Highly recommend.",
            "Very professional and well-prepared lessons.",
            "Amazing skills and great communication.",
            "Super helpful and encouraging throughout.",
            "Clear explanations and practical examples.",
            "Patient and understanding teacher.",
            "Exceeded my expectations! Great experience.",
            "Knowledgeable and passionate about the subject.",
            "Made learning fun and engaging.",
            "Very responsive and accommodating.",
            "Great attention to detail and quality.",
            "Inspiring teacher with real-world experience.",
        ]

        for skill in offered_skills:
            # Each skill gets 1-5 ratings from random users (excluding the skill owner)
            num_ratings = random.randint(1, 5)
            potential_raters = [u for u in all_users if u != skill.user]

            if len(potential_raters) < num_ratings:
                num_ratings = len(potential_raters)

            raters = random.sample(potential_raters, num_ratings)

            for rater in raters:
                # Check if rating already exists (unique constraint)
                if not Rating.objects.filter(skill=skill, user=rater).exists():
                    # Generate rating with higher probability for good ratings
                    rating_value = random.choices(
                        [1, 2, 3, 4, 5],
                        weights=[5, 10, 20, 35, 30],  # Weighted towards higher ratings
                    )[0]

                    # 70% chance of having a comment
                    comment = ""
                    if random.random() < 0.7:
                        comment = random.choice(rating_comments)

                    Rating.objects.create(
                        skill=skill, user=rater, rating=rating_value, comment=comment
                    )
                    ratings_created += 1

        return ratings_created
