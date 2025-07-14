"""
Django management command to clean up incomplete user profiles
Usage:
    python manage.py cleanup_profiles --dry-run  # Show what would be deleted
    python manage.py cleanup_profiles --delete   # Delete incomplete profiles
    python manage.py cleanup_profiles --stats    # Show profile completion statistics
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile


class Command(BaseCommand):
    help = "Clean up incomplete user profiles and show statistics"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without deleting anything",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete users with incomplete profiles",
        )
        parser.add_argument(
            "--stats",
            action="store_true",
            help="Show profile completion statistics",
        )

    def handle(self, *args, **options):
        if options["stats"]:
            self.show_statistics()
        elif options["delete"]:
            self.cleanup_profiles(dry_run=False)
        else:
            self.cleanup_profiles(dry_run=True)

    def show_statistics(self):
        """Show profile completion statistics"""
        total_users = (
            User.objects.filter(is_active=True).exclude(is_superuser=True).count()
        )
        complete_profiles = 0
        incomplete_profiles = 0

        users = (
            User.objects.filter(is_active=True)
            .exclude(is_superuser=True)
            .select_related("profile")
        )

        completion_stats = {}

        for user in users:
            try:
                profile = user.profile
                completion = profile.completion_percentage

                if profile.is_profile_complete:
                    complete_profiles += 1
                else:
                    incomplete_profiles += 1
                if completion == 100:
                    range_key = "100%"
                elif completion >= 80:
                    range_key = "80-99%"
                elif completion >= 60:
                    range_key = "60-79%"
                elif completion >= 40:
                    range_key = "40-59%"
                elif completion >= 20:
                    range_key = "20-39%"
                else:
                    range_key = "0-19%"

                completion_stats[range_key] = completion_stats.get(range_key, 0) + 1

            except Profile.DoesNotExist:
                incomplete_profiles += 1

        self.stdout.write(self.style.SUCCESS("\n=== PROFILE COMPLETION STATISTICS ==="))
        self.stdout.write(f"Total Users: {total_users}")
        self.stdout.write(
            f"Complete Profiles: {complete_profiles} ({(complete_profiles/total_users*100):.1f}%)"
        )
        self.stdout.write(
            f"Incomplete Profiles: {incomplete_profiles} ({(incomplete_profiles/total_users*100):.1f}%)"
        )

        self.stdout.write("\n--- Completion Distribution ---")
        for range_key in ["100%", "80-99%", "60-79%", "40-59%", "20-39%", "0-19%"]:
            count = completion_stats.get(range_key, 0)
            if count > 0:
                self.stdout.write(f"{range_key}: {count} users")

    def cleanup_profiles(self, dry_run=True):
        """Clean up users with incomplete profiles"""
        users_to_remove = []

        users = (
            User.objects.filter(is_active=True)
            .exclude(is_superuser=True)
            .select_related("profile")
        )

        for user in users:
            try:
                profile = user.profile
                if not profile.is_profile_complete:
                    missing_fields = profile.missing_required_fields
                    users_to_remove.append(
                        {
                            "user": user,
                            "missing_fields": missing_fields,
                            "completion": profile.completion_percentage,
                        }
                    )
            except Profile.DoesNotExist:
                users_to_remove.append(
                    {
                        "user": user,
                        "missing_fields": ["Profile not found"],
                        "completion": 0,
                    }
                )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\n____DRY RUN - {len(users_to_remove)} users would be removed____"
                )
            )
            for item in users_to_remove:
                user = item["user"]
                missing = ", ".join(item["missing_fields"])
                completion = item["completion"]
                self.stdout.write(
                    f"• {user.username} ({user.first_name} {user.last_name}) - "
                    f"{completion}% complete - Missing: {missing}"
                )

            if users_to_remove:
                self.stdout.write(
                    self.style.WARNING(
                        f"\nTo permanently delete these users, run: "
                        f"python manage.py cleanup_profiles --delete"
                    )
                )
            else:
                self.stdout.write(self.style.SUCCESS("No incomplete profiles found!"))
        else:
            self.stdout.write(
                self.style.ERROR(f"\n=== DELETING {len(users_to_remove)} users ===")
            )
            for item in users_to_remove:
                user = item["user"]
                self.stdout.write(f"Deleting: {user.username}")
                user.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted {len(users_to_remove)} incomplete profiles"
                )
            )
