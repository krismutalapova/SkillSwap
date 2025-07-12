# SkillSwap

A modern Django web platform that enables users to exchange skills and knowledge with each other. Connect with others to teach what you know and learn what you need.

## 🌟 Project Overview

SkillSwap is designed to create a community where people can:
- **Offer their skills** to help others learn
- **Request skills** they want to develop
- **Connect with like-minded learners** and teachers
- **Build a network** of skill-sharing relationships

## ✨ Current Features

### 🔐 Authentication System
- **Modern Login/Signup Pages**: Facebook-style design with glassmorphism effects
- **Password Security**: Password reveal functionality with eye icons
- **Form Validation**: Comprehensive error handling with helpful messages
- **User Guidance**: Username and password requirement hints
- **Secure Sessions**: POST-based logout and proper session management

### 👤 User Profiles
- **Complete Profile Management**: Create and edit user profiles
- **Personal Information**: Name, bio, city, country, gender fields
- **Profile Pictures**: Upload and display profile pictures with edit functionality
- **Skills Sections**: Display skills offered and skills needed
- **Modern UI**: Glassmorphism design with clickable profile picture and hover effects
- **Auto-Profile Creation**: Profiles automatically created for new users

### 🎨 Modern UI/UX Design
- **Glassmorphism Effects**: Semi-transparent cards with backdrop blur
- **Gradient Backgrounds**: Beautiful purple-blue gradient theme throughout
- **Professional Branding**: Custom SkillSwap logo with Font Awesome icons
- **Responsive Design**: Mobile-friendly layouts and breakpoints
- **Smooth Animations**: Hover effects and smooth transitions
- **Professional Typography**: Clean font hierarchy and spacing

### 🔧 Navigation & Error Handling
- **Dynamic Header**: Conditional navigation based on authentication state
- **Professional Buttons**: Gradient and outline button styles with hover effects
- **Custom Error Pages**: Branded 404 and 500 error pages with recovery options
- **Route Management**: Proper handling of common navigation patterns
- **Professional Footer**: Branded footer with navigation links

### 🛡️ Security & Best Practices
- **Django Security**: Built-in CSRF protection and secure authentication
- **Proper HTTP Methods**: POST requests for sensitive operations
- **Error Handling**: Graceful error management with user-friendly messages
- **Development Tools**: Test routes for error page development

## 🛠️ Technology Stack

- **Backend**: Django 4.x (Python web framework)
- **Database**: SQLite (development) - easily configurable for PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Image Processing**: Pillow (for profile picture uploads)
- **Development**: Virtual environment with pip

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd skillswap
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv skillswap_env

# Activate virtual environment
# On macOS/Linux:
source skillswap_env/bin/activate
# On Windows:
skillswap_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django pillow
```

### 4. Set Up Database
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

### 6. Access the Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login Page**: http://127.0.0.1:8000/login/
- **Signup Page**: http://127.0.0.1:8000/signup/

## 📁 Project Structure

```
skillswap/
├── core/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── templates/               # HTML templates
│   │   ├── core/               # App-specific templates
│   │   │   ├── home.html       # Home page
│   │   │   ├── login.html      # Login page
│   │   │   ├── signup.html     # Signup page
│   │   │   ├── logout.html     # Logout confirmation
│   │   │   ├── profile_view.html # Profile display
│   │   │   └── profile_edit.html # Profile editing
│   │   ├── base.html           # Base template
│   │   ├── 404.html           # Custom 404 error page
│   │   └── 500.html           # Custom 500 error page
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Django forms
│   ├── urls.py                # URL patterns
│   └── admin.py               # Admin configuration
├── skillswap/                 # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── media/                    # User uploaded files
├── static/                   # Static files (CSS, JS, images)
├── manage.py                # Django management script
├── plan.md                  # Project roadmap and features
├── implementation.md        # Detailed implementation log
└── README.md               # This file
```

## 🎯 Current User Journey

1. **Visit Homepage**: Modern welcome page with SkillSwap branding
2. **Sign Up**: Create account with comprehensive form validation
3. **Login**: Secure authentication with password reveal functionality
4. **Profile Setup**: Complete profile with personal information and skills
5. **Profile Management**: View and edit profile with modern UI
6. **Navigation**: Use responsive header with conditional navigation
7. **Error Handling**: Experience custom error pages if issues occur

## 🔄 API Endpoints

### Authentication
- `GET/POST /login/` - User login
- `GET/POST /signup/` - User registration
- `POST /logout/` - User logout (POST for security)

### Profiles
- `GET /profile/` - View current user's profile
- `GET/POST /profile/edit/` - Edit current user's profile

### Navigation
- `GET /` - Homepage
- `GET /home/` - Home page (alias)
- `GET /index/` - Index page (alias)

### Development/Testing
- `GET /test-404/` - Preview 404 error page
- `GET /test-500/` - Preview 500 error page
- `GET /simulate-404/` - Trigger actual 404 error

## 📝 Development Notes

### Custom Features Implemented
- **Auto-Profile Creation**: User profiles are automatically created via Django signals
- **Modern Design System**: Consistent glassmorphism and gradient design throughout
- **Professional Error Handling**: Custom 404/500 pages with branded design
- **Enhanced UX**: Smooth animations, hover effects, and responsive design
- **Security Best Practices**: CSRF protection, secure forms, and proper HTTP methods

### Database Models
- **User**: Django's built-in User model (username, email, password)
- **Profile**: Extended user information (bio, city, country, gender, profile picture, skills)

### Design Philosophy
- **Modern & Professional**: Glassmorphism effects with professional color scheme
- **User-Friendly**: Clear navigation, helpful error messages, and intuitive flows
- **Responsive**: Mobile-first design that works on all device sizes
- **Accessible**: Proper contrast, clear typography, and semantic HTML

## 🚧 Upcoming Features

The project roadmap includes these planned features:

### Phase 1: Core Functionality
- [ ] **Skill Listings**: Create, edit, and browse skill offerings/requests
- [ ] **Search & Filter**: Find skills by category, location, or type
- [ ] **Messaging System**: Contact other users about skill exchanges

### Phase 2: Enhanced Features
- [ ] **Reviews & Ratings**: Rate and review skill exchanges
- [ ] **Categories & Tags**: Organize skills with categories and tags
- [ ] **Advanced Search**: Location-based and availability filtering

### Phase 3: Platform Features
- [ ] **Admin Dashboard**: Enhanced admin interface for platform management
- [ ] **Notifications**: Message and activity notifications
- [ ] **Mobile App**: Native mobile application

## 🤝 Contributing

This is currently a personal project, but suggestions and feedback are welcome! The project follows Django best practices and maintains comprehensive documentation.

## 📄 License

This project is for educational and portfolio purposes.

## 📞 Support

For questions or issues:
1. Check the `implementation.md` file for detailed technical documentation
2. Review the `plan.md` file for project roadmap and feature status
3. Use the test routes (e.g., `/test-404/`) to preview features during development

---

**SkillSwap** - *Building connections through skill sharing* 🌟
