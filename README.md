# SkillSwap

A Django web platform for skill exchange and learning. Connect with others to teach what you know and learn what you need.

## Features

- **User Authentication**: Secure signup/login with modern UI
- **Profile Management**: Complete profiles with skills, bio, and profile pictures
- **User Search**: Browse other users with quality-filtered results
- **Modern Design**: Modern UI with responsive design
- **Auto-dismiss Notifications**: Popup system for user feedback

## Quick Start

```bash
# Setup environment
python -m venv skillswap_env
source skillswap_env/bin/activate
pip install django pillow

# Initialize database
python manage.py migrate
python manage.py createsuperuser

# Run server
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

```bash
# Populate test users
python manage.py populate_users --count 15

# Run tests
python tests/test_popup_messages.py
```

---

Built with Django, featuring modern UI design and professional development practices.
