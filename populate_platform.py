#!/usr/bin/env python3
"""
Quick script to populate SkillSwap with sample users.
This is a wrapper around the Django management command.

Usage:
    python populate_platform.py          # Create 20 users
    python populate_platform.py 50       # Create 50 users
    python populate_platform.py --clear  # Clear and create 20 users
"""

import os
import sys
import subprocess


def run_populate_command(args):
    """Run the Django management command with given arguments"""
    cmd = ["python", "manage.py", "populate_users"] + args

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def main():
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print(
            "Error: manage.py not found. Please run this script from the Django project root."
        )
        sys.exit(1)

    # Parse simple arguments
    args = []

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == "--clear":
                args.append("--clear")
            elif arg.isdigit():
                args.extend(["--count", arg])
            else:
                print(f"Unknown argument: {arg}")
                print("Usage: python populate_platform.py [count] [--clear]")
                sys.exit(1)

    print("🚀 Populating SkillSwap platform with sample users...")
    print("=" * 50)

    run_populate_command(args)

    print("=" * 50)
    print("✅ Population complete!")
    print("\n💡 Tips:")
    print("- All users have password: 'skillswap123'")
    print("- Usernames are: user001, user002, user003, etc.")
    print("- You can now test the platform with realistic data!")
    print("- Run 'python manage.py runserver' to start the development server")


if __name__ == "__main__":
    main()
