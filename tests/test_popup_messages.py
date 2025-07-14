#!/usr/bin/env python3
"""
Test script for all profile popup messages scenarios - profile completion and update
"""
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.contrib.messages import get_messages
from core.models import Profile


def test_all_popup_scenarios():
    print("Testing All Profile Popup Scenarios\n")

    # Test Scenario 1: Incomplete → Complete
    print("🔸 1: Incomplete → Complete")
    user1 = User.objects.get(username="testcompletion")
    profile1 = user1.profile
    profile1.city = ""
    profile1.skills_offered = ""
    profile1.skills_needed = ""
    profile1.save()

    print(
        f"   Before: Complete={profile1.is_profile_complete}, Missing={profile1.missing_required_fields}"
    )

    client1 = Client()
    client1.login(username="testcompletion", password="test123")

    response1 = client1.post(
        "/profile/edit/",
        {
            "bio": "Test bio",
            "skills_offered": "Python",
            "skills_needed": "Django",
            "city": "New York",
            "country": "USA",
            "gender": "M",
        },
    )

    profile1.refresh_from_db()
    messages1 = list(get_messages(response1.wsgi_request))
    print(
        f"   After: Complete={profile1.is_profile_complete}, Missing={profile1.missing_required_fields}"
    )
    print(f"   Message: {messages1[0] if messages1 else 'None'}")
    print(
        f"   Expected: profile_completed ✅"
        if messages1 and str(messages1[0]) == "profile_completed"
        else "   ❌ Wrong message"
    )
    print()

    # Test Scenario 2: Complete → Complete (update)
    print("🔸 2: Complete → Complete (update)")
    print(f"   Before: Complete={profile1.is_profile_complete}")
    client2 = Client()
    client2.login(username="testcompletion", password="test123")

    response2 = client2.post(
        "/profile/edit/",
        {
            "bio": "Updated bio",
            "skills_offered": "Python, JavaScript",
            "skills_needed": "Django, React",
            "city": "San Francisco",
            "country": "USA",
            "gender": "M",
        },
    )

    profile1.refresh_from_db()
    messages2 = list(get_messages(response2.wsgi_request))
    print(f"   After: Complete={profile1.is_profile_complete}")
    print(f"   Message: {messages2[0] if messages2 else 'None'}")
    print(
        f"   Expected: profile_updated ✅"
        if messages2 and str(messages2[0]) == "profile_updated"
        else "   ❌ Wrong message"
    )
    print()

    # Test Scenario 3: Incomplete → Incomplete (update)
    print("🔸 3: Incomplete → Incomplete (update)")
    profile1.city = ""
    profile1.save()

    print(
        f"   Before: Complete={profile1.is_profile_complete}, Missing={profile1.missing_required_fields}"
    )

    client3 = Client()
    client3.login(username="testcompletion", password="test123")

    response3 = client3.post(
        "/profile/edit/",
        {
            "bio": "Another updated bio",
            "skills_offered": "Python, Go",
            "skills_needed": "Kubernetes",
            "city": "",
            "country": "USA",
            "gender": "F",
        },
    )

    profile1.refresh_from_db()
    messages3 = list(get_messages(response3.wsgi_request))
    print(
        f"   After: Complete={profile1.is_profile_complete}, Missing={profile1.missing_required_fields}"
    )
    print(f"   Message: {messages3[0] if messages3 else 'None'}")
    print(
        f"   Expected: profile_updated ✅"
        if messages3 and str(messages3[0]) == "profile_updated"
        else "   ❌ Wrong message"
    )
    print()

    print("Test Summary:\n")
    print("All three scenarios should show appropriate popups:")
    print("✅ Incomplete → Complete: Green 'Profile Complete!' popup")
    print("✅ Complete → Complete: Blue 'Profile Updated!' popup")
    print("✅ Incomplete → Incomplete: Blue 'Profile Updated!' popup")


if __name__ == "__main__":
    test_all_popup_scenarios()
