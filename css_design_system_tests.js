/**
 * Browser console test suite for comprehensive CSS validation including:
 * - Design system variables and consistency
 * - Utility class functionality and rendering
 * - Component styling and interactions
 * - Performance monitoring and optimization
 * - Interactive component showcase
 * 
 * Usage:
 * 1. Start Django server: python manage.py runserver
 * 2. Open browser to http://127.0.0.1:8000
 * 3. Open Developer Console (F12)
 * 4. Copy/paste this entire file
 * 5. Review test results and interactive showcase
  */

console.clear();
console.log("🧪 SkillSwap CSS Design System - Comprehensive Test Suite");
console.log("=".repeat(65));
console.log("Testing CSS variables, utility classes, components, and performance\n");

// ============================================================================
// DESIGN SYSTEM VARIABLES TEST
// ============================================================================

function testDesignSystemVariables() {
    console.log("1️⃣ Design System Variables");
    console.log("-".repeat(40));

    const coreVariables = [
        // Color System
        { name: '--color-primary', expected: '#6441a5', category: 'colors' },
        { name: '--color-primary-gradient', expectedContains: 'linear-gradient', category: 'colors' },
        { name: '--color-secondary', expected: '#667eea', category: 'colors' },
        { name: '--color-text-primary', expected: '#2c3e50', category: 'colors' },
        { name: '--color-background', expected: '#f8f9fa', category: 'colors' },

        // Spacing System
        { name: '--nav-link-padding', expected: '10px 20px', category: 'spacing' },
        { name: '--button-padding-small', expected: '8px 16px', category: 'spacing' },
        { name: '--nav-gap', expected: '15px', category: 'spacing' },

        // Typography
        { name: '--font-weight-medium', expected: '500', category: 'typography' },
        { name: '--font-size-sm', expected: '14px', category: 'typography' },

        // Layout
        { name: '--radius-card', expected: '15px', category: 'layout' },
        { name: '--transition-all', expectedContains: 'all', category: 'layout' },

        // Component Specific
        { name: '--profile-pic-size', expected: '60px', category: 'components' },
        { name: '--skill-description-min-height', expected: '3rem', category: 'components' }
    ];

    let passed = 0;
    const categoryResults = {};

    coreVariables.forEach(({ name, expected, expectedContains, category }) => {
        const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        let testPassed = false;

        if (expected) {
            testPassed = value === expected;
        } else if (expectedContains) {
            testPassed = value.toLowerCase().includes(expectedContains.toLowerCase());
        }

        const displayValue = value.length > 30 ? value.substring(0, 30) + '...' : value;
        const status = testPassed ? '✅' : '❌';
        const expectation = expected || `contains "${expectedContains}"`;

        console.log(`   ${status} ${name}: ${displayValue} ${testPassed ? '' : `(expected: ${expectation})`}`);

        if (testPassed) passed++;
        if (!categoryResults[category]) categoryResults[category] = { passed: 0, total: 0 };
        categoryResults[category].total++;
        if (testPassed) categoryResults[category].passed++;
    });

    console.log(`\n📊 Variables Summary: ${passed}/${coreVariables.length} passed`);
    Object.entries(categoryResults).forEach(([category, results]) => {
        const percentage = Math.round((results.passed / results.total) * 100);
        console.log(`   ${category}: ${results.passed}/${results.total} (${percentage}%)`);
    });

    return { passed, total: coreVariables.length, categoryResults };
}

// ============================================================================
// UTILITY CLASSES TEST
// ============================================================================

function testUtilityClasses() {
    console.log("\n2️⃣ Utility Classes Validation");
    console.log("-".repeat(40));

    // Create test container
    const testContainer = document.createElement('div');
    testContainer.style.cssText = 'position: fixed; top: -1000px; left: -1000px; opacity: 0;';
    document.body.appendChild(testContainer);

    testContainer.innerHTML = `
        <div class="btn-primary">Button Primary</div>
        <div class="btn-secondary">Button Secondary</div>
        <div class="btn-success">Button Success</div>
        <div class="glass-card">Glass Card</div>
        <div class="nav-link">Nav Link</div>
    `;

    const utilityTests = [
        {
            selector: '.btn-primary',
            tests: [
                { property: 'background', shouldContain: 'gradient', description: 'has gradient background' },
                { property: 'border-radius', expected: '8px', description: 'has proper border radius' },
                { property: 'padding', shouldContain: 'px', description: 'has padding defined' }
            ]
        },
        {
            selector: '.btn-secondary',
            tests: [
                { property: 'background-color', shouldNotBe: 'rgba(0, 0, 0, 0)', description: 'has background color' },
                { property: 'border-radius', expected: '8px', description: 'has proper border radius' }
            ]
        },
        {
            selector: '.glass-card',
            tests: [
                { property: 'background', shouldContain: 'rgba', description: 'has glassmorphism background' },
                { property: 'backdrop-filter', shouldContain: 'blur', description: 'has backdrop blur' }
            ]
        },
        {
            selector: '.nav-link',
            tests: [
                { property: 'padding', expected: '10px 20px', description: 'uses CSS variable padding' },
                { property: 'border-radius', expected: '15px', description: 'uses CSS variable radius' },
                { property: 'display', expected: 'flex', description: 'has flex display' }
            ]
        }
    ];

    let utilityPassed = 0;
    let utilityTotal = 0;

    utilityTests.forEach(({ selector, tests }) => {
        const element = testContainer.querySelector(selector);
        console.log(`\n   Testing ${selector}:`);

        if (!element) {
            console.log(`   ❌ Element ${selector} not found`);
            return;
        }

        tests.forEach(({ property, expected, shouldContain, shouldNotBe, description }) => {
            const value = getComputedStyle(element).getPropertyValue(property).trim();
            let testPassed = false;

            if (expected) {
                testPassed = value === expected;
            } else if (shouldContain) {
                testPassed = value.toLowerCase().includes(shouldContain.toLowerCase());
            } else if (shouldNotBe) {
                testPassed = value !== shouldNotBe;
            }

            const status = testPassed ? '✅' : '❌';
            const displayValue = value.length > 25 ? value.substring(0, 25) + '...' : value;

            console.log(`      ${status} ${description}: ${displayValue}`);

            utilityTotal++;
            if (testPassed) utilityPassed++;
        });
    });

    // Cleanup
    document.body.removeChild(testContainer);

    console.log(`\n📊 Utility Classes: ${utilityPassed}/${utilityTotal} tests passed`);
    return { passed: utilityPassed, total: utilityTotal };
}

// ============================================================================
// COMPONENT INTEGRATION TEST
// ============================================================================

function testComponentIntegration() {
    console.log("\n3️⃣ Component Integration");
    console.log("-".repeat(40));

    const componentSelectors = [
        { selector: '.skill-card', description: 'Skill cards' },
        { selector: '.skill-tile', description: 'Skill tiles' },
        { selector: '.filters-card', description: 'Filter components' },
        { selector: '.message-nav', description: 'Message navigation' },
        { selector: '.profile-completion', description: 'Profile completion UI' },
        { selector: '.nav-link.active', description: 'Active navigation links' }
    ];

    let componentsFound = 0;
    let componentsWorking = 0;

    componentSelectors.forEach(({ selector, description }) => {
        const elements = document.querySelectorAll(selector);

        if (elements.length > 0) {
            componentsFound++;

            // Test first element styling
            const element = elements[0];
            const styles = getComputedStyle(element);

            // Check if element has basic styling applied
            const hasBackground = styles.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
                styles.background !== 'rgba(0, 0, 0, 0)' ||
                styles.backgroundImage !== 'none';

            const hasLayout = styles.padding !== '0px' ||
                styles.margin !== '0px' ||
                styles.borderRadius !== '0px';

            const isWorking = hasBackground || hasLayout;

            const status = isWorking ? '✅' : '⚠️';
            console.log(`   ${status} ${description}: ${elements.length} found${isWorking ? ', styled' : ', basic styling'}`);

            if (isWorking) componentsWorking++;
        } else {
            console.log(`   ℹ️  ${description}: Not found on this page`);
        }
    });

    console.log(`\n📊 Components: ${componentsWorking}/${componentsFound} components properly styled`);
    return { found: componentsFound, working: componentsWorking };
}

// ============================================================================
// BUTTON CONSOLIDATION VALIDATION
// ============================================================================

function testButtonConsolidation() {
    console.log("\n3️⃣.5 Button Consolidation Validation");
    console.log("-".repeat(40));

    const tests = [];
    let passed = 0;

    // Test 1: Check if logout button uses .btn-muted class
    const logoutBtn = document.querySelector('.btn-muted');
    const hasLogoutIcon = logoutBtn ? logoutBtn.querySelector('.fa-sign-out-alt') !== null : false;

    tests.push({
        name: "Logout button uses .btn-muted utility class",
        result: logoutBtn !== null && hasLogoutIcon
    });

    if (logoutBtn) {
        const styles = getComputedStyle(logoutBtn);

        tests.push({
            name: "Button has proper styling (background, radius, padding)",
            result: styles.backgroundColor !== 'rgba(0, 0, 0, 0)' &&
                styles.borderRadius === '8px' &&
                styles.padding !== '0px'
        });

        tests.push({
            name: "Button has hover effects (transition)",
            result: (() => {
                const transition = styles.transition || '';
                const transitionDuration = styles.transitionDuration || '';

                // Check if there's a valid transition (either full property or just duration)
                const hasTransition = (transition &&
                    transition !== 'none' &&
                    transition !== 'all 0s ease 0s' &&
                    (transition.includes('all') ||
                        transition.includes('transform') ||
                        transition.includes('background') ||
                        transition.length > 10)) ||
                    (transitionDuration &&
                        transitionDuration !== '0s' &&
                        transitionDuration !== 'none');

                // Debug log for troubleshooting
                if (!hasTransition) {
                    console.log(`      🔍 Debug - Transition: "${transition}", Duration: "${transitionDuration}"`);
                }

                return hasTransition;
            })()
        });

        // Test icon spacing
        const icon = logoutBtn.querySelector('i');
        if (icon) {
            const iconStyles = getComputedStyle(icon);
            tests.push({
                name: "Icon has proper spacing",
                result: iconStyles.marginRight !== '0px'
            });
        }
    }

    // Test 2: Verify old .logout-btn class is not defined
    const testDiv = document.createElement('div');
    testDiv.className = 'logout-btn';
    testDiv.style.cssText = 'position: fixed; top: -1000px; left: -1000px; opacity: 0;';
    document.body.appendChild(testDiv);

    const testStyles = getComputedStyle(testDiv);
    tests.push({
        name: "Old .logout-btn class successfully removed",
        result: testStyles.backgroundColor === 'rgba(0, 0, 0, 0)' ||
            testStyles.backgroundColor === 'transparent'
    });

    document.body.removeChild(testDiv);

    // Test 3: Check logout functionality
    const form = logoutBtn?.closest('form');
    tests.push({
        name: "Logout functionality preserved (form + CSRF)",
        result: form !== null &&
            form.method.toLowerCase() === 'post' &&
            form.querySelector('[name="csrfmiddlewaretoken"]') !== null
    });

    // Display results
    tests.forEach((test, index) => {
        const status = test.result ? '✅' : '❌';
        const description = test.name;
        console.log(`   ${status} ${description}`);
        if (test.result) passed++;
    });

    console.log(`\n📊 Button Consolidation: ${passed}/${tests.length} validation tests passed`);

    if (passed === tests.length) {
        console.log("   🎉 Phase 4.5 consolidation successful!");
    } else {
        console.log("   ⚠️  Some consolidation issues detected");
    }

    return { passed, total: tests.length };
}

// ============================================================================
// PERFORMANCE MONITORING
// ============================================================================

function testPerformance() {
    console.log("\n4️⃣ CSS Performance Analysis");
    console.log("-".repeat(40));

    const cssFiles = Array.from(document.styleSheets)
        .filter(sheet => sheet.href && sheet.href.includes('/static/css/'))
        .map(sheet => {
            const url = new URL(sheet.href);
            return {
                name: url.pathname.split('/').pop(),
                href: sheet.href,
                rules: sheet.cssRules ? sheet.cssRules.length : 0
            };
        });

    console.log("   CSS Files Loaded:");
    cssFiles.forEach(file => {
        const sizeIndicator = file.rules > 100 ? '🔴' : file.rules > 50 ? '🟡' : '🟢';
        console.log(`   ${sizeIndicator} ${file.name}: ~${file.rules} rules`);
    });

    // Test CSS variable fallback performance
    const variableAccessTime = performance.now();
    const testDiv = document.createElement('div');
    testDiv.style.color = 'var(--color-primary)';
    document.body.appendChild(testDiv);
    getComputedStyle(testDiv).color;
    document.body.removeChild(testDiv);
    const accessTime = performance.now() - variableAccessTime;

    console.log(`   CSS Variable Access: ${accessTime.toFixed(2)}ms ${accessTime < 1 ? '✅' : '⚠️'}`);

    return {
        filesLoaded: cssFiles.length,
        totalRules: cssFiles.reduce((sum, f) => sum + f.rules, 0),
        variableAccessTime: accessTime
    };
}

// ============================================================================
// INTERACTIVE COMPONENT SHOWCASE
// ============================================================================

function createInteractiveShowcase() {
    console.log("\n5️⃣ Interactive Component Showcase");
    console.log("-".repeat(40));
    console.log("   Creating interactive design system showcase...");

    // Remove existing showcase
    const existingShowcase = document.getElementById('css-test-showcase');
    if (existingShowcase) {
        existingShowcase.remove();
    }

    const showcase = document.createElement('div');
    showcase.id = 'css-test-showcase';
    showcase.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        width: 350px;
        max-height: 80vh;
        overflow-y: auto;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 50px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;

    showcase.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; color: var(--color-primary, #6441a5);">🎨 Design System</h3>
            <button onclick="this.closest('#css-test-showcase').remove()" 
                    style="background: none; border: none; font-size: 18px; cursor: pointer; color: #999;">✕</button>
        </div>
        
        <div style="margin-bottom: 15px;">
            <h4 style="margin: 5px 0; color: #333;">Button Utilities</h4>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <button class="btn-primary" style="font-size: 12px; padding: 6px 12px;">Primary</button>
                <button class="btn-secondary" style="font-size: 12px; padding: 6px 12px;">Secondary</button>
                <button class="btn-success" style="font-size: 12px; padding: 6px 12px;">Success</button>
                <button class="btn-muted" style="font-size: 12px; padding: 6px 12px;"><i class="fas fa-sign-out-alt"></i>Logout</button>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <h4 style="margin: 5px 0; color: #333;">Navigation Elements</h4>
            <div style="display: flex; gap: 5px; flex-wrap: wrap;">
                <span class="nav-link" style="font-size: 12px; cursor: pointer;">Nav Link</span>
                <span class="nav-link" style="font-size: 12px; cursor: pointer; background: var(--color-primary-gradient, linear-gradient(135deg, #6441a5, #2a0845)); color: white;">Active</span>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <h4 style="margin: 5px 0; color: #333;">Glass Cards</h4>
            <div class="glass-card" style="padding: 10px; margin: 5px 0; font-size: 12px;">
                Glassmorphism Card Effect
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <h4 style="margin: 5px 0; color: #333;">CSS Variables</h4>
            <div style="font-size: 11px; color: #666;">
                <div>Primary: <span style="color: var(--color-primary, #6441a5);">■</span> var(--color-primary)</div>
                <div>Secondary: <span style="color: var(--color-secondary, #667eea);">■</span> var(--color-secondary)</div>
                <div>Radius: <span style="display: inline-block; width: 12px; height: 12px; background: #ddd; border-radius: var(--radius-card, 15px);"></span> var(--radius-card)</div>
            </div>
        </div>
        
        <div style="font-size: 11px; color: #999; text-align: center;">
            Interactive Design System Showcase<br>
            <em>Test results in console ↗️</em>
        </div>
    `;

    document.body.appendChild(showcase);
    console.log("   ✅ Interactive showcase created (top-right corner)");
    console.log("   ℹ️  Showcase demonstrates live CSS variables and utility classes");

    return true;
}

// ============================================================================
// MAIN TEST RUNNER
// ============================================================================

function runComprehensiveTests() {
    const startTime = performance.now();

    // Run all test suites
    const variableResults = testDesignSystemVariables();
    const utilityResults = testUtilityClasses();
    const componentResults = testComponentIntegration();
    const buttonConsolidationResults = testButtonConsolidation();
    const performanceResults = testPerformance();
    const showcaseCreated = createInteractiveShowcase();

    const totalTime = performance.now() - startTime;

    // Print comprehensive summary
    console.log("\n" + "=".repeat(65));
    console.log("📊 COMPREHENSIVE TEST SUMMARY");
    console.log("=".repeat(65));

    const totalPassed = variableResults.passed + utilityResults.passed + buttonConsolidationResults.passed;
    const totalTests = variableResults.total + utilityResults.total + buttonConsolidationResults.total;
    const overallPercentage = Math.round((totalPassed / totalTests) * 100);

    console.log(`🎯 Overall: ${totalPassed}/${totalTests} tests passed (${overallPercentage}%)`);
    console.log(`⚡ Performance: ${totalTime.toFixed(2)}ms test execution time`);
    console.log(`📁 CSS Files: ${performanceResults.filesLoaded} loaded, ~${performanceResults.totalRules} rules`);
    console.log(`🧩 Components: ${componentResults.working}/${componentResults.found} properly styled`);
    console.log(`🔧 Button Consolidation: ${buttonConsolidationResults.passed}/${buttonConsolidationResults.total} validation tests passed`);
    console.log(`✨ Showcase: ${showcaseCreated ? 'Created' : 'Failed'} (top-right corner)`);

    // Status indicator
    if (overallPercentage >= 90) {
        console.log("\n🎉 EXCELLENT: CSS design system working perfectly!");
    } else if (overallPercentage >= 75) {
        console.log("\n✨ GOOD: Most CSS features working, minor issues detected");
    } else if (overallPercentage >= 50) {
        console.log("\n⚠️  NEEDS WORK: Significant CSS issues need attention");
    } else {
        console.log("\n❌ CRITICAL: Major CSS design system problems detected");
    }

    console.log("\n💡 Next Steps:");
    if (variableResults.passed < variableResults.total) {
        console.log("   - Fix missing/incorrect CSS variables in variables.css");
    }
    if (utilityResults.passed < utilityResults.total) {
        console.log("   - Review utility class definitions in utilities.css");
    }
    if (componentResults.working < componentResults.found) {
        console.log("   - Check component CSS integration");
    }
    if (performanceResults.variableAccessTime > 1) {
        console.log("   - Consider CSS performance optimization");
    }

    console.log("\n🔄 Rerun: Copy/paste this script again to retest");
    console.log("📖 Documentation: Check README.md for test details");

    return {
        overallPercentage,
        totalPassed,
        totalTests,
        executionTime: totalTime,
        components: componentResults,
        buttonConsolidation: buttonConsolidationResults,
        performance: performanceResults
    };
}

// ============================================================================
// EXECUTE TESTS
// ============================================================================

// Run the comprehensive test suite - Use var to allow re-declaration
if (typeof testResults !== 'undefined') {
    delete window.testResults;
    delete window.skillswapTestResults;
}

var testResults = runComprehensiveTests();

// Store results globally for further inspection
window.skillswapTestResults = testResults;
