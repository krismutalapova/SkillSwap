#!/bin/bash

echo "SkillSwap Demo - Available Test Users"
echo "===================================="
echo ""

# Check if container is running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Demo is not running. Start with: ./demo-start.sh"
    exit 1
fi

echo "✅ Demo is running at: http://localhost:8000"
echo ""
echo "🔧 Admin Access:"
echo "   URL: http://localhost:8000/admin/"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "👥 Demo includes 25 test users with:"
echo "   • Complete profiles with photos"
echo "   • Diverse skills across all categories"
echo "   • Realistic locations and availability"
echo "   • Sample ratings and reviews"
echo ""
echo "📋 Key Demo Users for Presentation:"
echo "   • Sarah Martinez - Web Developer (offers Django, needs Italian)"
echo "   • Marco Rossi - Italian Teacher (offers Italian, needs Web Dev)"
echo "   • Emma Johnson - UI/UX Designer (offers Design, needs Photography)"
echo "   • Plus 22 more diverse profiles..."
echo ""
echo "🚀 Ready for your presentation!"
echo ""
echo "Commands:"
echo "   • Stop demo: docker-compose down"
echo "   • Restart demo: docker-compose restart"
echo "   • Fresh setup: docker-compose up --build"
