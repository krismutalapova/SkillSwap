#!/bin/bash

echo "Starting SkillSwap Demo Setup..."

# Wait a moment for any file system to settle
sleep 2

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Create demo users for presentations
echo "Creating consistent demo users..."
python manage.py create_demo_users --clear

# Create additional random users for variety
echo "Adding variety with random users..."
python manage.py populate_users --count 15

# Sync profile skills
echo "Syncing profile skills..."
python manage.py sync_profile_skills

echo "Demo setup complete!"
echo ""
echo "SkillSwap is ready for presentation!"
echo "Admin credentials: admin / admin123"
echo "Demo users are available with complete profiles and skills"
echo ""

# Start the development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
