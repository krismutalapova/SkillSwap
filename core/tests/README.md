# SkillSwap Test Suite

Comprehensive testing framework for the SkillSwap platform with organized structure and multiple test runners.

## 📁 Test Structure

```
core/tests/
├── README.md                            
├── django_tests/                          # 🔧 Backend functionality tests
│   ├── test_models.py                     # Profile, Skill, Message, Rating models
│   ├── test_views.py                      # Authentication, CRUD, permissions
│   ├── test_forms.py                      # Form validation and processing
│   ├── test_templates.py                  # Template rendering and context
│   └── test_integration.py                # End-to-end workflows
├── frontend_tests/                        # 🎨 Frontend and CSS tests
│   ├── utils/                             # 🔧 Shared test utilities and base classes
│   │   ├── __init__.py                    # Package initialization
│   │   ├── base_test_classes.py           # CSSTestCase, CSSLiveTestCase base classes
│   │   ├── css_test_helpers.py            # CSS parsing and analysis utilities
│   │   └── file_test_helpers.py           # File operations and project navigation
│   ├── test_css_variables.py              # CSS variable usage and definition tests
│   ├── test_button_consolidation.py       # Button pattern consolidation validation
│   ├── test_hardcoded_values.py           # Hardcoded value detection and analysis
│   ├── test_css_architecture.py           # CSS file organization and naming conventions
│   ├── test_responsive_design.py          # Responsive design and mobile-first validation
│   ├── test_template_css_integration.py   # Template-CSS integration and class usage
│   ├── test_css_performance.py            # Performance analysis and optimization
│   ├── test_css_integrity.py              # File existence, syntax, and basic validation
│   ├── test_css_duplicate_classes.py      # Cross-file duplicate detection
│   ├── test_css_integration.py            # Django integration validation
│   ├── test_visual_regression.py          # Visual regression testing
│   ├── test_css_refactoring_suite.py      # Monolithic suite 
│   └── css_tests.js                       # JavaScript design system tests
└── test_runners/                          # 🚀 Test execution utilities
    ├── comprehensive_runner.py            # Full-featured runner
    ├── simple_runner.py                   # Quick test execution
    ├── django_only_runner.py              # Backend tests only
    └── frontend_runner.py                 # Frontend tests only
```

## 🚀 Quick Start

### Run All Tests
```bash
# Basic test run
python manage.py test core.tests

# With detailed output
python manage.py test core.tests --verbosity=2

# With coverage analysis
python core/tests/test_runners/comprehensive_runner.py --coverage
```

### Run Specific Categories
```bash
# Django tests only
python manage.py test core.tests.django_tests

# Frontend tests only  
python manage.py test core.tests.frontend_tests

# Individual test modules
python manage.py test core.tests.django_tests.test_models
python manage.py test core.tests.django_tests.test_views
```

## Test Runners

### **`comprehensive_runner.py`** - Primary Runner
Complete testing solution with advanced features:
- ✅ Coverage analysis and HTML reports
- ✅ Environment validation 
- ✅ Performance metrics and timing
- ✅ All Django + Frontend tests

```bash
python core/tests/test_runners/comprehensive_runner.py --coverage
python core/tests/test_runners/comprehensive_runner.py --check-env
python core/tests/test_runners/comprehensive_runner.py --specific models
```

### **`simple_runner.py`** - Quick Runner
Lightweight execution with colored output:
- ✅ Fast execution
- ✅ Django-only or Frontend-only modes
- ✅ Individual test categories

```bash
python core/tests/test_runners/simple_runner.py
python core/tests/test_runners/simple_runner.py --django
python core/tests/test_runners/simple_runner.py --frontend
```

### **`django_only_runner.py`** - Backend Only
Django tests without frontend overhead:
```bash
python core/tests/test_runners/django_only_runner.py
python core/tests/test_runners/django_only_runner.py models
```

### **`frontend_runner.py`** - Frontend Specialist
CSS and visual testing with browser automation:
```bash
python core/tests/test_runners/frontend_runner.py
python core/tests/test_runners/frontend_runner.py --visual
```

## JavaScript CSS Tests

Dual-mode CSS design system validation:
```bash
# Node.js file system analysis
node core/tests/frontend_tests/css_tests.js

# Browser live validation (copy/paste into browser console)
# Visit http://127.0.0.1:8000 and paste css_tests.js content
```

## Test Categories

### Django Tests (`django_tests/`)
- **Models**: Profile completion, skill sync, ratings, signals
- **Views**: Authentication, CRUD operations, permissions, error handling  
- **Forms**: Validation, field processing, user input handling
- **Templates**: Rendering, context, template tags, inheritance
- **Integration**: Complete user workflows, messaging, skill discovery

### Frontend Tests (`frontend_tests/`)
- **CSS Variables**: Variable definition, usage, and integration testing
- **Button Consolidation**: Button pattern consolidation and utility adoption
- **Hardcoded Values**: Detection and analysis of hardcoded CSS values
- **CSS Architecture**: File organization, naming conventions, and structure
- **Responsive Design**: Mobile-first approach and breakpoint validation
- **Template Integration**: Template-CSS integration and class usage validation
- **Performance**: File size analysis, optimization opportunities, load times
- **Integrity**: File existence, syntax validation, and basic quality checks
- **Duplicate Detection**: Cross-file duplicate class analysis
- **CSS Integration**: Django staticfiles integration
- **Visual Regression**: Selenium browser automation testing

## Development Workflow

### Adding New Tests
1. **Choose category**: Django (`django_tests/`) or Frontend (`frontend_tests/`)
2. **Follow naming**: `test_<component>.py` and `test_<specific_behavior>`
3. **Use setUp()**: Prepare test data in setUp() method
4. **Test thoroughly**: Positive, negative, and edge cases

### Testing Best Practices
- Each test should be independent and isolated
- Use Django's TestCase for database tests
- Include descriptive assertion messages
- Test both success and failure scenarios

### Example Test Pattern
```python
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
        
        profile.city = 'Stockholm'
        profile.save()
        self.assertTrue(profile.is_profile_complete)
```

## Continuous Integration

### Recommended CI Pipeline
```bash
# 1. Environment validation
python core/tests/test_runners/comprehensive_runner.py --check-env

# 2. Full test suite with coverage
python core/tests/test_runners/comprehensive_runner.py --coverage

# 3. Frontend validation
python core/tests/test_runners/frontend_runner.py
```

### Pre-commit Checklist
- [ ] All tests pass locally
- [ ] New tests added for new functionality  
- [ ] Test coverage maintained or improved
- [ ] No hardcoded values in tests

---

This comprehensive test suite ensures the SkillSwap platform maintains high quality and reliability across all components.
