/**
 * Enhanced CSS Conflict Resolution Test
 * 
 * Test to verify duplicate styles were removed and variables are active
 * Run in browser console after refreshing the page
 */

console.log("🧹 Enhanced CSS Conflict Resolution Test...\n");

// Test that our refactored variables are now the only ones active
const testElements = [
    { selector: '.filters-card', property: 'padding', expected: '25px' },
    { selector: '.filters-card', property: 'margin-bottom', expected: '30px' },
    { selector: '.filter-group', property: 'min-width', expected: '200px' },
    { selector: '.skill-card', property: 'background', shouldContain: 'rgba(255, 255, 255, 0.95)' },
    { selector: '.skill-type-offer', property: 'background', shouldContain: 'linear-gradient' },
    { selector: '.skill-type-request', property: 'background', shouldContain: 'linear-gradient' }
];

console.log("Testing CSS Variables Application:");
let conflictsResolved = 0;

testElements.forEach(({ selector, property, expected, shouldContain }) => {
    const element = document.querySelector(selector);
    if (element) {
        const computedValue = getComputedStyle(element).getPropertyValue(property);
        let passed = false;

        if (expected) {
            passed = computedValue.trim() === expected;
        } else if (shouldContain) {
            passed = computedValue.includes(shouldContain.substring(0, 20));
        }

        console.log(`   ${passed ? '✅' : '❌'} ${selector} ${property}: ${computedValue.substring(0, 50)}${computedValue.length > 50 ? '...' : ''}`);
        if (passed) conflictsResolved++;
    } else {
        console.log(`   ⚠️  ${selector} not found on this page`);
    }
});

console.log(`\nVariable Application: ${conflictsResolved}/${testElements.length} tests passed\n`);

// Enhanced CSS rule conflict detection
console.log("Detailed CSS Rule Analysis:");
const stylesheets = Array.from(document.styleSheets);
const ruleChecks = [
    { selector: '.filters-card', maxExpected: 2, description: 'Filter card styling' },
    { selector: '.skill-card', maxExpected: 25, description: 'Skill card (base + mini variants + hovers + page-specific)' },
    { selector: '.skill-meta', maxExpected: 3, description: 'Skill metadata (base + responsive + mini)' },
    { selector: '.filter-group', maxExpected: 6, description: 'Filter group (base + label + select + responsive)' },
    { selector: '.active-filters', maxExpected: 2, description: 'Active filters display' }
];

ruleChecks.forEach(({ selector, maxExpected, description }) => {
    let ruleCount = 0;
    let sourceFiles = new Set();
    let specificRules = [];

    stylesheets.forEach(sheet => {
        try {
            const sheetHref = sheet.href || 'inline';
            const fileName = sheetHref.split('/').pop();
            Array.from(sheet.cssRules || []).forEach(rule => {
                if (rule.selectorText && rule.selectorText.includes(selector)) {
                    ruleCount++;
                    sourceFiles.add(fileName);
                    // Store specific selector for debugging
                    if (selector === '.skill-card' || selector === '.filter-group') {
                        specificRules.push(`${fileName}: ${rule.selectorText}`);
                    }
                }
            });
        } catch (e) {
            // Handle cross-origin stylesheets
        }
    });

    const status = ruleCount <= maxExpected ? '✅' : '❌';
    console.log(`   ${status} ${selector}: ${ruleCount} rules (expected ≤${maxExpected}) - ${description}`);
    if (sourceFiles.size > 0) {
        console.log(`      Sources: ${Array.from(sourceFiles).join(', ')}`);
    }

    // Show specific rules for debugging problem selectors
    if ((selector === '.skill-card' && ruleCount > 25) || (selector === '.filter-group' && ruleCount > 6)) {
        console.log(`      Specific rules: ${specificRules.slice(0, 10).join(', ')}`);
        if (specificRules.length > 10) console.log(`      ... and ${specificRules.length - 10} more`);
    }
});

// Test specific CSS variables
console.log("\nCSS Variables Verification:");
const cssVariables = [
    { name: '--space-lg', expected: '20px' },  // Updated to match fixed variable
    { name: '--space-xl', expected: '25px' },
    { name: '--space-xxl', expected: '30px' },
    { name: '--filter-group-min-width', expected: '200px' },
    { name: '--color-background-glass', shouldContain: 'rgba(255, 255, 255, 0.95)' }
];

cssVariables.forEach(({ name, expected, shouldContain }) => {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    let passed = false;

    if (expected) {
        passed = value === expected;
    } else if (shouldContain) {
        passed = value.includes(shouldContain);
    }

    console.log(`   ${passed ? '✅' : '❌'} ${name}: ${value || 'not defined'}`);
});

console.log("\n✅ Enhanced CSS Conflict Resolution Test Complete!");
console.log("💡 Refresh the page and run this test again to see improvements");
console.log("🎯 Check browser inspector - crossed-out styles should be minimal");
console.log("📊 Rule counts should be within expected ranges now");
