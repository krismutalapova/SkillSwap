# Tests

This directory contains all test files for the SkillSwap project.

## Test Files:

### Python Tests (Django)
- `test_popup_messages.py` - Comprehensive tests for all profile popup scenarios (completion and update)
- `test_css_system.py` - CSS variables, design system consistency, and file structure tests
- `test_css_visual.py` - Browser-based visual regression tests (requires Selenium)

### JavaScript Tests (Browser)
- `../test_utilities.js` - Browser console tests for CSS variables and utility classes

## Running Tests:

### Python Tests
To run all Django tests:
```bash
python manage.py test
```

To run specific test categories:
```bash
# CSS system tests
python manage.py test core.tests.test_css_system

# Visual tests (requires Selenium setup)  
python manage.py test core.tests.test_css_visual

# Profile tests
python manage.py test core.tests.test_popup_messages
```

### JavaScript CSS Tests
1. Open browser to your local development server
2. Open Developer Console (F12)
3. Copy and paste contents of `test_utilities.js`
4. Review test results and visual test panel

## Test Categories:

### 1. CSS System Tests (`test_css_system.py`)
- ✅ **File Existence**: Verify CSS files exist
- ✅ **Variable Definitions**: Check all required CSS variables are defined
- ✅ **Utility Classes**: Verify utility classes are present
- ✅ **File Sizes**: Ensure CSS files stay within reasonable size limits
- ✅ **Loading Order**: Test CSS files load in correct sequence
- ✅ **Design Consistency**: Check for hardcoded values that should use variables

### 2. Visual Regression Tests (`test_css_visual.py`) 
- 🔧 **Browser Tests**: Selenium-based visual verification (optional)
- 🔧 **Responsive Tests**: Cross-device layout verification
- ✅ **Performance Tests**: CSS payload size monitoring
- ✅ **Syntax Tests**: Basic CSS validation

### 3. Interactive Tests (`test_utilities.js`)
- ✅ **Variable Access**: Test CSS variables in browser environment
- ✅ **Utility Rendering**: Verify utility classes produce expected visual results
- ✅ **Interactive Panel**: Live examples of design system components
- ✅ **Performance Monitoring**: Real-time CSS file size tracking

## When to Run Tests:

### During Refactoring (Current)
- Run `test_css_system.py` after every phase
- Use `test_utilities.js` for quick visual verification
- Monitor file sizes to track refactoring progress

### After Refactoring (Ongoing)
- Include CSS tests in CI/CD pipeline  
- Run before major releases
- Use for design system documentation
- Performance regression monitoring

## Benefits:

1. **Regression Prevention**: Catch visual breaks during refactoring
2. **Performance Monitoring**: Track CSS bloat over time
3. **Design System Validation**: Ensure consistency across components
4. **Documentation**: Tests serve as living examples
5. **Confidence**: Refactor fearlessly with automated validation

## Future Enhancements:

- Screenshot comparison tests
- Automated cross-browser testing
- CSS coverage reporting
- Design token validation
- Performance budgets

## Test Categories:

### Profile Tests
- Profile completion logic
- Profile update notifications
- User feedback popups

### Future Tests
- User authentication tests
- Search functionality tests
- Skills matching tests
- Messaging system tests (when implemented)
