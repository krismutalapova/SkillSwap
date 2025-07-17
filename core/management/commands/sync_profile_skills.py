"""
Django management command to sync profile skills with individual Skill objects.
This updates the skills_offered and skills_needed text fields based on active Skill objects.

Usage:
    python manage.py sync_profile_skills
    python manage.py sync_profile_skills --user username
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = "Sync profile skills_offered and skills_needed fields from individual Skill objects"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            type=str,
            help="Sync skills for specific username only",
        )

    def handle(self, *args, **options):
        username = options.get("user")

        if username:
            try:
                user = User.objects.get(username=username)
                users = [user]
                self.stdout.write(f"Syncing skills for user: {username}")
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User '{username}' not found"))
                return
        else:
            users = User.objects.filter(is_active=True)
            self.stdout.write(f"Syncing skills for all {users.count()} active users...")

        synced_count = 0
        for user in users:
            try:
                profile = user.profile
                old_offered = profile.skills_offered
                old_needed = profile.skills_needed

                # Update skills from Skill objects
                profile.update_skills_from_skill_objects()

                # Check if anything changed
                profile.refresh_from_db()
                if (
                    old_offered != profile.skills_offered
                    or old_needed != profile.skills_needed
                ):
                    synced_count += 1
                    self.stdout.write(
                        f"✓ {user.username}: "
                        f"offers='{profile.skills_offered}', "
                        f"needs='{profile.skills_needed}'"
                    )

            except Profile.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"No profile found for user: {user.username}")
                )
                continue
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error syncing {user.username}: {str(e)}")
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f"Successfully synced skills for {synced_count} users!")
        )
