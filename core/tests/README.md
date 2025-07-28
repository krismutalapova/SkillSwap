# SkillSwap Test Suite

This directory contains comprehensive tests for t### 🎨 Frontend Tests (`frontend_tests/`)
User interface and styling tests:

#### **JavaScript CSS Design System Tests** (`css_tests.js`)
- **Dual-mode testing**: Node.js file system analysis + Browser live validation
- **Node.js mode**: `node core/tests/frontend_tests/css_tests.js`
- **Browser mode**: Copy/paste into browser console on running Django server
- **Coverage**: Design system validation, CSS consolidation verification, performance analysis

#### **CSS Refactoring Suite** (`test_css_refactoring_suite.py`)killSwap platform, organized into logical categories for better maintainability and clarity.

## 📁 Directory Structure

```
core/tests/
├── __init__.py                             # Main test package entry point  
├── README.md                              # This comprehensive test guide
├── django_tests/                          # 🔧 Core Django functionality tests
│   ├── __init__.py
│   ├── test_models.py                     # Model tests (Profile, Skill, Message, Rating)
│   ├── test_views.py                      # View tests (authentication, CRUD, permissions)
│   ├── test_forms.py                      # Form validation and processing tests
│   ├── test_templates.py                  # Template rendering and context tests
│   └── test_integration.py                # End-to-end workflow tests
├── frontend_tests/                        # 🎨 Frontend and CSS tests
│   ├── __init__.py
│   ├── css_tests.js                       # JavaScript CSS design system tests (Node.js + Browser)
│   ├── test_css_duplicate_classes.py      # CSS duplication detection
│   ├── test_css_integration.py            # CSS integration tests
│   ├── test_css_refactoring.py            # CSS refactoring tests  
│   ├── test_css_refactoring_suite.py      # CSS refactoring suite
│   ├── test_profile_pages_optimization.py # Profile page optimization
│   └── test_visual_regression.py          # Visual regression tests
├── test_runners/                          # 🚀 Test execution utilities
│   ├── __init__.py
│   ├── run_organized_tests.py             # Organized test runner with colors
│   ├── run_all_tests.py                   # Comprehensive test runner with coverage
│   ├── run_django_tests.py                # Simple Django test runner
│   └── run_all_css_tests.py               # CSS-specific test runner
└── reports/                               # 📊 Generated reports and coverage data
    └── (generated files)
```

## Test Categories

### Django Tests (`django_tests/`)
Core Django application functionality testing:

#### **Model Tests** (`test_models.py`)
- **Profile Model**: Profile completion logic, skill synchronization, properties
- **Skill Model**: CRUD operations, ratings, category handling  
- **Message Model**: Communication system functionality
- **Rating Model**: Rating calculations and constraints
- **Signal Testing**: Profile auto-creation, skill synchronization

#### **View Tests** (`test_views.py`)
- **Authentication Views**: Signup, login, profile completion
- **Profile Views**: Profile viewing, editing, permission handling
- **Skill Views**: Skill CRUD, filtering, search functionality
- **Message Views**: Messaging system, inbox, sent messages
- **Error Handling**: 404/500 custom error pages

#### **Form Tests** (`test_forms.py`)
- **User Forms**: Signup form, name completion form
- **Profile Forms**: Profile editing, validation
- **Skill Forms**: Skill creation/editing, field validation
- **Message Forms**: Message sending, form validation

#### **Template Tests** (`test_templates.py`)
- **Template Rendering**: Template context and rendering
- **Template Tags**: Custom template tags functionality
- **Form Rendering**: Form display and validation errors
- **Navigation**: Template inheritance and navigation

#### **Integration Tests** (`test_integration.py`)
- **User Workflow**: Complete user registration → profile setup → skill creation
- **Skill Discovery**: Search and filtering functionality
- **Message System**: End-to-end messaging workflow
- **Rating System**: Rating creation and calculation

### Frontend Tests (`frontend_tests/`)
User interface and styling tests:

#### **CSS Refactoring Suite** (`test_css_refactoring_suite.py`)
- CSS variable usage validation
- Button pattern consolidation verification
- Hardcoded value replacement checks
- File integrity and syntax validation

#### **CSS Integration Tests** (`test_css_integration.py`)
- Template rendering with new CSS classes
- Static file serving and CSS loading
- Form styling integration
- Django-specific CSS functionality

#### **CSS Duplicate Detection** (`test_css_duplicate_classes.py`)
- Cross-file duplicate class detection
- Within-file duplicate class validation
- CSS architecture and separation of concerns analysis
- Comprehensive duplicate elimination verification

#### **Profile Pages Optimization** (`test_profile_pages_optimization.py`)
- Detailed profile-pages.css optimization analysis
- 100% variable usage validation
- Font size and border width optimization checks
- Section organization validation
- Profile-specific optimizations tracking

#### **Visual Regression Tests** (`test_visual_regression.py`)
- Selenium-based browser automation
- Visual rendering verification
- Responsive design testing
- Cross-browser compatibility checks

### Test Runners (`test_runners/`)
Test execution and automation tools:

#### **Organized Test Runner** (`run_organized_tests.py`)
- Color-coded output for different test categories
- Selective test execution by category
- Status summary with pass/fail counts

#### **Comprehensive Runner** (`run_all_tests.py`)
- All tests with coverage reporting
- Detailed execution logging
- Performance metrics

#### **Specialized Runners**
- **Django Runner** (`run_django_tests.py`): Backend tests only
- **CSS Runner** (`run_all_css_tests.py`): Frontend tests only

## 🚀 Running Tests

### Quick Start Commands

```bash
# Run all tests
python manage.py test core.tests

# Run specific categories
python manage.py test core.tests.django_tests      # All Django tests
python manage.py test core.tests.frontend_tests    # All frontend tests

# Run specific test modules
python manage.py test core.tests.django_tests.test_models     # Model tests only
python manage.py test core.tests.django_tests.test_views      # View tests only  
python manage.py test core.tests.django_tests.test_forms      # Form tests only
python manage.py test core.tests.django_tests.test_templates  # Template tests only
python manage.py test core.tests.django_tests.test_integration # Integration tests only

# Run JavaScript CSS tests
node core/tests/frontend_tests/css_tests.js        # Node.js file system analysis
# OR open browser console on http://127.0.0.1:8000 and paste css_tests.js content
```

### Using Test Runners

```bash
# Organized test runner with colored output
python core/tests/test_runners/run_organized_tests.py                    # All tests
python core/tests/test_runners/run_organized_tests.py --django           # Django tests only
python core/tests/test_runners/run_organized_tests.py --frontend         # Frontend tests only
python core/tests/test_runners/run_organized_tests.py --models           # Model tests only
python core/tests/test_runners/run_organized_tests.py --views            # View tests only

# Comprehensive test runner with coverage
python core/tests/test_runners/run_all_tests.py --coverage

# Django tests only
python core/tests/test_runners/run_django_tests.py

# CSS tests only
python core/tests/test_runners/run_all_css_tests.py

# JavaScript CSS design system tests
node core/tests/frontend_tests/css_tests.js                              # File system analysis
```

### Advanced Test Options

```bash
# Verbose output
python manage.py test core.tests --verbosity=2

# Specific test methods
python manage.py test core.tests.django_tests.test_models.ProfileModelTest.test_profile_completion

# With coverage reporting
coverage run --source='.' manage.py test core.tests
coverage report
coverage html
```

## 🛠️ Test Development Guidelines

### File Organization
- Place tests in the appropriate category directory (`django_tests/` or `frontend_tests/`)
- Use descriptive test class and method names
- Keep related tests together in the same file

### Naming Conventions
- **Test files**: `test_<component>.py`
- **Test classes**: `<Component>Test` or `<Component><Type>Test`
- **Test methods**: `test_<specific_behavior>`

### Best Practices
- Each test should be independent and isolated
- Use Django's TestCase for database tests
- Use setUp() and tearDown() for test data preparation
- Test both positive and negative scenarios
- Include edge cases and error conditions
- Use descriptive assertion messages

### Testing Patterns

```python
# Model testing example
class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_profile_completion_status(self):
        """Test profile completion logic"""
        profile = self.user.profile
        self.assertFalse(profile.is_profile_complete)
        
        # Add required fields
        profile.city = 'Stockholm'
        profile.save()
        self.assertTrue(profile.is_profile_complete)

# View testing example
class ProfileViewTest(TestCase):
    def test_profile_edit_requires_login(self):
        """Test that profile editing requires authentication"""
        response = self.client.get('/profile/edit/')
        self.assertRedirects(response, '/login/?next=/profile/edit/')
```

## 📈 Adding New Tests

### For Django Functionality
1. **Determine the category**: Models, Views, Forms, Templates, or Integration
2. **Add to appropriate file**: `django_tests/test_<category>.py`
3. **Follow naming conventions**: Clear, descriptive test names
4. **Include test data setup**: Use setUp() method or fixtures
5. **Test thoroughly**: Include positive, negative, and edge cases

### For Frontend Features
1. **Choose appropriate test type**: CSS, visual regression, or performance
2. **Add to `frontend_tests/`**: Place in relevant test file
3. **Consider test dependencies**: Browser automation, static files, etc.
4. **Document test requirements**: Any special setup or dependencies

### Test Coverage Goals
- **Models**: 100% method and property coverage
- **Views**: All HTTP methods and permission scenarios
- **Forms**: All validation rules and edge cases
- **Templates**: All template tags and context variables
- **Integration**: Complete user workflows

## 🔍 Debugging Test Failures

### Common Issues
1. **Database State**: Ensure tests don't depend on each other
2. **Static Files**: Verify CSS/JS files are properly configured
3. **Authentication**: Check login requirements for protected views
4. **URL Patterns**: Ensure correct URL names in tests

### Debugging Tools
```bash
# Run single failing test with verbose output
python manage.py test core.tests.django_tests.test_views.SearchViewTest.test_search_with_filters --verbosity=2

# Use Django's test database inspection
python manage.py test --debug-mode --verbosity=2

# Generate coverage report to identify untested code
coverage run --source='.' manage.py test core.tests
coverage html
```

## 🚀 Continuous Integration

### Pre-commit Checklist
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Test coverage maintained or improved
- [ ] Documentation updated for new test categories

### Performance Guidelines
- Keep test execution time under 30 seconds for the full suite
- Use Django's `TransactionTestCase` only when necessary
- Mock external services and APIs
- Use test-specific settings when needed

---

This comprehensive test suite ensures the SkillSwap platform maintains high quality and reliability.
