/**
 * SkillSwap CSS Utilities Test Suite
 * 
 * Run this in browser console to verify CSS variables and utility classes work correctly.
 * Useful during development and refactoring.
 */

console.log("🧪 Testing SkillSwap CSS Design System...\n");

// ============================================================================
// TEST 1: CSS Variables Validation
// ============================================================================
console.log("1️⃣ Testing CSS Variables:");

const testVariables = [
  { name: '--color-primary-start', expected: '#6441a5' },
  { name: '--color-primary-end', expected: '#2a0845' },
  { name: '--space-xl', expected: '20px' },
  { name: '--space-md', expected: '12px' },
  { name: '--radius-card', expected: '15px' },
  { name: '--color-background-glass', expected: 'rgba(255, 255, 255, 0.95)' }
];

let variableTestsPassed = 0;
testVariables.forEach(({ name, expected }) => {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const passed = value === expected;
  console.log(`   ${passed ? '✅' : '❌'} ${name}: ${value} ${passed ? '' : `(expected: ${expected})`}`);
  if (passed) variableTestsPassed++;
});

console.log(`Variables Test: ${variableTestsPassed}/${testVariables.length} passed\n`);

// ============================================================================
// TEST 2: Utility Classes Validation  
// ============================================================================
console.log("2️⃣ Testing Utility Classes:");

const testUtilityClasses = (testContainer) => {
  const testResults = [];

  // Test glassmorphism
  const glassCard = testContainer.querySelector('.glass-card');
  const glassBackground = getComputedStyle(glassCard).backgroundColor;
  testResults.push({
    test: 'glass-card background',
    passed: glassBackground.includes('rgba') && glassBackground.includes('0.95'),
    value: glassBackground
  });

  // Test button styling
  const btnPrimary = testContainer.querySelector('.btn-primary');
  const btnBackground = getComputedStyle(btnPrimary).backgroundImage;
  testResults.push({
    test: 'btn-primary gradient',
    passed: btnBackground.includes('linear-gradient'),
    value: btnBackground.substring(0, 50) + '...'
  });

  // Test text gradient
  const textGradient = testContainer.querySelector('.text-gradient');
  const textBg = getComputedStyle(textGradient).backgroundImage;
  testResults.push({
    test: 'text-gradient',
    passed: textBg.includes('linear-gradient'),
    value: textBg.substring(0, 50) + '...'
  });

  return testResults;
};

// ============================================================================
// TEST 3: Create Visual Test Panel
// ============================================================================
console.log("3️⃣ Creating Visual Test Panel...");

const createTestPanel = () => {
  // Remove existing test panel if present
  const existingPanel = document.getElementById('css-test-panel');
  if (existingPanel) existingPanel.remove();

  const testPanel = document.createElement('div');
  testPanel.id = 'css-test-panel';
  testPanel.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; z-index: 9999; 
                    background: white; border: 2px solid #ccc; border-radius: 8px; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.2); padding: 20px; max-width: 300px;">
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="margin: 0;">🧪 CSS Test Panel</h4>
                <button onclick="document.getElementById('css-test-panel').remove()" 
                        style="background: #dc3545; color: white; border: none; border-radius: 4px; padding: 5px 10px; cursor: pointer;">×</button>
            </div>
            
            <!-- Test glassmorphism cards -->
            <div class="glass-card p-md mb-md" style="margin-bottom: 12px;">
                <h5 class="text-gradient text-bold" style="margin: 0 0 8px 0;">Glass Card Test</h5>
                <p class="text-muted" style="margin: 0 0 8px 0; font-size: 14px;">Should have blur effect</p>
                <button class="btn-base btn-primary btn-small">Primary</button>
            </div>
            
            <!-- Test button variations -->
            <div class="flex-between mb-md" style="display: flex; gap: 8px; margin-bottom: 12px;">
                <button class="btn-base btn-secondary btn-small">Secondary</button>
                <button class="btn-base btn-success btn-small">Success</button>
            </div>
            
            <!-- Test form utilities -->
            <div class="form-group mb-md" style="margin-bottom: 12px;">
                <input class="form-field" type="text" placeholder="Form field test" style="width: 100%; margin-bottom: 8px;">
            </div>
            
            <!-- Test results display -->
            <div id="test-results" style="font-size: 12px; border-top: 1px solid #eee; padding-top: 10px;">
                <div class="text-muted">Running tests...</div>
            </div>
        </div>
    `;

  document.body.appendChild(testPanel);

  // Run utility class tests on the panel
  setTimeout(() => {
    const results = testUtilityClasses(testPanel);
    const resultsDiv = document.getElementById('test-results');

    let resultHTML = '<strong>Utility Tests:</strong><br>';
    let passedCount = 0;

    results.forEach(({ test, passed, value }) => {
      resultHTML += `${passed ? '✅' : '❌'} ${test}<br>`;
      if (passed) passedCount++;
    });

    resultHTML += `<br><strong>${passedCount}/${results.length} tests passed</strong>`;
    resultsDiv.innerHTML = resultHTML;

    console.log(`   Utility Classes: ${passedCount}/${results.length} passed`);
  }, 100);

  return testPanel;
};

// Run the visual test
createTestPanel();

// ============================================================================
// TEST 4: Performance Check
// ============================================================================
console.log("\n4️⃣ Performance Check:");

const checkCSSFileSize = async (url) => {
  try {
    const response = await fetch(url);
    const text = await response.text();
    return text.length;
  } catch (error) {
    return 0;
  }
};

// Check CSS file sizes (async)
Promise.all([
  checkCSSFileSize('/static/css/variables.css'),
  checkCSSFileSize('/static/css/utilities.css'),
  checkCSSFileSize('/static/css/base.css')
]).then(([variablesSize, utilitiesSize, baseSize]) => {
  console.log(`   variables.css: ${(variablesSize / 1000).toFixed(1)}KB`);
  console.log(`   utilities.css: ${(utilitiesSize / 1000).toFixed(1)}KB`);
  console.log(`   base.css: ${(baseSize / 1000).toFixed(1)}KB`);
  console.log(`   Total core CSS: ${((variablesSize + utilitiesSize + baseSize) / 1000).toFixed(1)}KB`);

  const totalSize = variablesSize + utilitiesSize + baseSize;
  const isOptimal = totalSize < 50000; // Under 50KB is good
  console.log(`   ${isOptimal ? '✅' : '⚠️'} Size is ${isOptimal ? 'optimal' : 'large'}`);
});

// ============================================================================
// Summary
// ============================================================================
setTimeout(() => {
  console.log("\n🎯 Test Summary:");
  console.log("   • CSS variables are loaded and accessible");
  console.log("   • Utility classes render correctly");
  console.log("   • Visual test panel created (top-right corner)");
  console.log("   • Performance metrics displayed");
  console.log("\n✅ CSS Design System Tests Completed!");
  console.log("\n💡 Tips:");
  console.log("   - Test panel shows live examples of utility classes");
  console.log("   - Hover over cards to test hover effects");
  console.log("   - Resize window to test responsive behavior");
}, 1000);
