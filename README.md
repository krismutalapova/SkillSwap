# 🔄 SkillSwap

**A modern Django web platform connecting people through skill exchange and collaborative learning.**

SkillSwap enables users to discover others in their community, share expertise, and learn new skills through a peer-to-peer exchange system. Whether you're looking to teach programming, learn cooking, or trade language lessons for music instruction, SkillSwap makes meaningful connections simple.

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Key Features

### 🧑‍🤝‍🧑 **Smart User Discovery**
- Browse community members with complete profiles
- Advanced filtering by skills, location, and user preferences
- Optional combinable filters (apply one, multiple, or none)
- Intelligent search across skill titles and descriptions

### 🎯 **Skill Management System**
- **Offer Skills**: Share your expertise (Programming, Music, Cooking, Languages, etc.)
- **Request Skills**: Find what you want to learn
- **Categories**: Technology, Art, Language, Sports, Lifestyle, and more
- **Personal Dashboard**: Manage all your skills in one place

### ⭐ **Dynamic Rating System**
- Star-based ratings (1-5) for individual skills
- Calculated overall user ratings across all offerings
- Visual feedback with filled, half, and empty stars
- Community-driven trust building

### 👤 **Complete Profile Experience**
- Profile completion tracking with smart guidance
- Bio, location, and profile picture management
- Skills showcase with offerings and requests
- Real-time completion status notifications

### 🎨 **Modern User Experience**
- **Glassmorphism Design**: Contemporary, accessible interface
- **Responsive Layout**: Seamless mobile and desktop experience
- **Smart Notifications**: Auto-dismissing feedback system
- **Intuitive Navigation**: User-focused design patterns

## 🚀 Quick Start

### 🐳 **Demo Setup (Docker - Recommended)**

Perfect for presentations, demos, or quick evaluation:

```bash
# One-command setup with realistic demo data
docker-compose up --build
```

**What you get:**
- ✅ Complete environment in 30 seconds
- ✅ 6 consistent demo users for presentations
- ✅ 15 additional random users for variety  
- ✅ 50+ skills across all categories with realistic ratings
- ✅ Cross-user ratings demonstrating trust system
- ✅ Admin access: http://localhost:8000/admin/ (`admin`/`admin123`)

**Demo Users** (password: `demo123`):
- **Sarah Martinez** - Django developer ↔ Italian learner
- **Marco Rossi** - Italian teacher ↔ Web dev student  
- **Emma Johnson** - UI/UX designer ↔ Photography student
- **Liam Chen** - Photographer ↔ German learner
- **Sofia Andersson** - Chef ↔ Business student
- **Alex Müller** - Business consultant ↔ Guitar student

🌐 **Access:** http://localhost:8000

### 💻 **Development Setup**

For local development and customization:

```bash
# 1. Setup virtual environment
python -m venv skillswap_env
source skillswap_env/bin/activate  # macOS/Linux
# skillswap_env\Scripts\activate   # Windows

# 2. Install dependencies
pip install django pillow

# 3. Initialize database
python manage.py migrate
python manage.py createsuperuser

# 4. Setup demo data (choose one option)
dev/setup-demo.sh                  # Consistent demo users for presentations
python manage.py populate_users --count 20  # Random users for development

# 5. Start development server
python manage.py runserver
```

**Convenience Scripts** (for ongoing development):
```bash
dev/dev-server.sh                  # Auto-activates env and starts server
dev/manage.sh migrate               # Run Django commands with auto-env
./manage.sh populate_users --count 15
```

## 🏗️ Technical Architecture

### **Django MVT Excellence**
- **Single-App Architecture**: Focused, maintainable codebase
- **Model Layer**: Efficient relationships with computed properties
- **View Layer**: Function-based views with class-based authentication
- **Template Layer**: Inheritance-based design with custom tags

### **Database Design**
```
User (Django Auth) → Profile (Extended user data)
                   ↓
                  Skill (Individual offerings/requests)
                   ↓
                  Rating (Community feedback)
                   ↓
                  Message (User communication)
```

### **Key Technical Features**
- **Django Signals**: Automatic profile creation and synchronization
- **Custom Management Commands**: Data population and maintenance
- **Template Tags**: Reusable rating and utility components
- **Media Handling**: Secure file uploads with Pillow
- **Responsive Design**: Mobile-first CSS with glassmorphism

## 📊 Platform Statistics

| Feature | Implementation |
|---------|---------------|
| **Models** | User, Profile, Skill, Rating, Message |
| **Views** | 15+ function-based views + custom auth |
| **Templates** | Inheritance-based with 20+ templates |
| **Categories** | Technology, Art, Language, Sports, Lifestyle+ |
| **Filters** | Type, Category, Location, Search, Gender |
| **Rating System** | 1-5 stars with mathematical averaging |

## 🛠️ Development Commands

### **Data Management**
```bash
# Populate realistic demo users
python manage.py populate_users --count 25

# Sync profile skills from individual skill objects  
python manage.py sync_profile_skills

# Clean up incomplete profiles
python manage.py cleanup_profiles
```

### **Testing & Quality**
```bash
# Run custom test suite
python tests/test_popup_messages.py

# Django development server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic
```

## 🏗️ Project Structure

```
skillswap/
├── 📁 core/                    # Main application
│   ├── models.py              # User, Profile, Skill, Rating, Message
│   ├── views.py               # Function-based views + SignupView
│   ├── forms.py               # Custom forms with validation
│   ├── admin.py               # Django admin configuration
│   ├── urls.py                # URL routing patterns
│   ├── 📁 templates/core/     # HTML templates with inheritance
│   ├── 📁 templatetags/       # Custom template filters and tags
│   ├── 📁 management/commands/ # populate_users, sync_profile_skills
│   └── 📁 migrations/         # Database schema versions
├── 📁 skillswap/              # Project configuration
├── 📁 static/                 # CSS, JavaScript, images
├── 📁 media/                  # User-uploaded files
├── 📁 tests/                  # Custom test suite
└── 🐳 docker-compose.yml      # Container orchestration
```

## 🚀 Deployment & Production

### **Docker Production**
```bash
# Production-ready containerized deployment
docker-compose -f docker-compose.prod.yml up -d
```

### **Traditional Deployment**
```bash
# Install production dependencies
pip install -r requirements.txt

# Configure production settings
export DJANGO_SETTINGS_MODULE=skillswap.settings.production

# Static files and database
python manage.py collectstatic --noinput
python manage.py migrate
```