# SkillSwap

A Django web platform for skill exchange and learning. Connect with others to teach what you know and learn what you need.

## Features

- **User Authentication**: Secure signup/login with modern UI
- **Profile Management**: Complete profiles with skills, bio, and profile pictures
- **Skill Listings**: Create, browse, and manage skill offerings and requests
- **Advanced Search**: Comprehensive filtering by type, category, location and gender
- **Optional Filtering**: All filters work independently - apply none, one, or multiple filters
- **User Discovery**: Browse other users with quality-filtered results
- **Modern Design**: Modern UI and responsive design
- **Auto-dismiss Notifications**: Comprehensive popup system for user feedback

## Quick Start

### First Time Setup
```bash
# Setup environment
python -m venv skillswap_env
source skillswap_env/bin/activate
pip install django pillow

# Initialize database
python manage.py migrate
python manage.py createsuperuser
```

### Development (Convenience Scripts)
```bash
# Start development server (auto-activates environment)
./dev-server.sh

# Run Django commands (auto-activates environment)
./manage.sh migrate
./manage.sh createsuperuser
./manage.sh populate_users --count 15
./manage.sh sync_profile_skills
```

### Manual Method
```bash
# If you prefer to activate manually
source skillswap_env/bin/activate
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Project Structure

```
skillswap/
├── core/           # Main app with models, views, templates
├── tests/          # Test files
├── scripts/        # Utility scripts
├── media/          # User uploads
└── static/         # CSS, JS, images
```

## Commands

### Using Convenience Scripts (Recommended)
```bash
# Populate test users
./manage.sh populate_users --count 15

# Sync profile skills from individual Skill objects
./manage.sh sync_profile_skills

# Run tests
python tests/test_popup_messages.py

# Start development server
./dev-server.sh
```

### Manual Commands (with virtual environment activated)
```bash
# Populate test users
python manage.py populate_users --count 15

# Run tests
python tests/test_popup_messages.py
```

## Core Functionality

### Skill Management
- Create skill offerings (what you can teach)
- Create skill requests (what you want to learn)
- Browse all available skills with filtering
- Advanced search by title, description, category
- Personal skills dashboard for management

### User Profiles
- Complete profile system with location and bio
- Profile completion tracking with visual indicators
- Profile picture upload and management
- Skills offered and needed sections

### Discovery and Search
- Browse all users with complete profiles
- Comprehensive skill filtering by type (offered/requested), category, location, and gender
- Optional filtering system: apply any combination of filters or none at all
- Search functionality across skill titles and descriptions
- Unified search experience from home page to skills listing
- Pagination for efficient browsing with filter state preservation

---

Built with Django, featuring modern UI design and professional development practices.
