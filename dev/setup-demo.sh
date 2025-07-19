#!/bin/bash

echo "SkillSwap Demo Users Setup"
echo "=========================="
echo ""

# Get the project root directory (parent of dev/)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not detected. Activating skillswap_env..."
    if [ -d "skillswap_env" ]; then
        source skillswap_env/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Error: skillswap_env not found. Please create virtual environment first."
        exit 1
    fi
fi

echo "🏗️  Setting up demo users..."
echo ""

# Run migrations first
echo "📋 Running migrations..."
python manage.py migrate

echo ""
echo "👥 Creating demo users..."
python manage.py create_demo_users --clear

echo ""
echo "🎲 Adding random users for variety..."
python manage.py populate_users --count 15

echo ""
echo "🔄 Syncing profile skills..."
python manage.py sync_profile_skills

echo ""
echo "✅ Demo setup complete!"
echo ""
echo "🚀 Demo Users Created:"
echo "   • Sarah Martinez (sarah_martinez) - Django developer seeking Italian"
echo "   • Marco Rossi (marco_rossi) - Italian teacher seeking web dev"
echo "   • Emma Johnson (emma_johnson) - UI/UX designer seeking photography"
echo "   • Liam Chen (liam_chen) - Photographer seeking German"
echo "   • Sofia Andersson (sofia_andersson) - Chef seeking business skills"
echo "   • Alex Müller (alex_müller) - Business consultant seeking guitar"
echo "   • Plus 15 additional random users"
echo ""
echo "🔑 Demo Credentials:"
echo "   • Demo users password: demo123"
echo "   • Admin panel: admin / admin123"
echo ""
echo "🎯 Ready for your presentation!"
echo "   Start server: dev/dev-server.sh"
echo "   Visit: http://localhost:8000"
