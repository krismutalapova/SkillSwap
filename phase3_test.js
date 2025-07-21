/**
 * Phase 3 Component Validation Test
 * 
 * Test specifically for the components.css refactoring
 * Run in browser console after Phase 3 changes
 */

console.log("🔧 Phase 3 Component Testing...\n");

// Test the new variables we added
const phase3Variables = [
    { name: '--radius-pill', expected: '20px' },
    { name: '--color-offer-gradient', expected: 'linear-gradient(135deg, #3a7bd5bd 0%, #3a6073 100%)' },
    { name: '--color-request-gradient', expected: 'linear-gradient(135deg, #fd746ce0 0%, #ff9068d6 100%)' },
    { name: '--profile-pic-size', expected: '60px' },
    { name: '--skill-description-min-height', expected: '3rem' },
    { name: '--transform-card-hover', expected: 'translateY(-5px)' }
];

console.log("Testing Phase 3 Variables:");
let phase3Passed = 0;
phase3Variables.forEach(({ name, expected }) => {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    const passed = value === expected || value.includes(expected.substring(0, 20));
    console.log(`   ${passed ? '✅' : '❌'} ${name}: ${value.substring(0, 50)}${value.length > 50 ? '...' : ''}`);
    if (passed) phase3Passed++;
});

console.log(`Phase 3 Variables: ${phase3Passed}/${phase3Variables.length} passed\n`);

// Test component styles are working
console.log("Testing Component CSS Application:");

// Create test elements to verify component styles
const testContainer = document.createElement('div');
testContainer.innerHTML = `
  <div class="filters-card" style="width: 300px; margin: 20px;">
    <div class="filter-group">
      <label>Test Filter</label>
      <input type="text" placeholder="Test input">
    </div>
    <button class="search-btn btn-base btn-primary">Test Button</button>
  </div>
  
  <div class="skill-card" style="width: 300px; margin: 20px;">
    <div class="skill-header">
      <h3 class="skill-title">Test Skill</h3>
      <span class="skill-type skill-type-offer">OFFER</span>
    </div>
    <div class="skill-content">
      <p class="skill-description">Test description for skill card</p>
      <div class="skill-meta">
        <span class="category">Technology</span>
      </div>
    </div>
  </div>
  
  <div class="user-card" style="width: 300px; margin: 20px;">
    <div class="user-header">
      <div class="profile-pic-placeholder" style="background: #ddd;"></div>
      <div>
        <h4>Test User</h4>
        <p>Test user description</p>
      </div>
    </div>
  </div>
`;

testContainer.style.position = 'fixed';
testContainer.style.top = '10px';
testContainer.style.left = '10px';
testContainer.style.zIndex = '10000';
testContainer.style.background = 'white';
testContainer.style.padding = '20px';
testContainer.style.borderRadius = '15px';
testContainer.style.boxShadow = '0 10px 50px rgba(0,0,0,0.3)';
testContainer.style.maxHeight = '80vh';
testContainer.style.overflow = 'auto';

document.body.appendChild(testContainer);

// Test computed styles
setTimeout(() => {
    console.log("Component Style Tests:");

    // Test filters card
    const filtersCard = testContainer.querySelector('.filters-card');
    const filtersBg = getComputedStyle(filtersCard).background;
    console.log(`   ${filtersBg.includes('rgba') ? '✅' : '❌'} Filters card glassmorphism: ${filtersBg.includes('rgba') ? 'Applied' : 'Missing'}`);

    // Test skill card hover
    const skillCard = testContainer.querySelector('.skill-card');
    const skillBg = getComputedStyle(skillCard).background;
    console.log(`   ${skillBg.includes('rgba') ? '✅' : '❌'} Skill card glassmorphism: ${skillBg.includes('rgba') ? 'Applied' : 'Missing'}`);

    // Test skill type gradient
    const skillType = testContainer.querySelector('.skill-type-offer');
    const skillTypeBg = getComputedStyle(skillType).background;
    console.log(`   ${skillTypeBg.includes('gradient') ? '✅' : '❌'} Skill type gradient: ${skillTypeBg.includes('gradient') ? 'Applied' : 'Missing'}`);

    // Test profile pic size
    const profilePic = testContainer.querySelector('.profile-pic-placeholder');
    const profileWidth = getComputedStyle(profilePic).width;
    console.log(`   ${profileWidth === '60px' ? '✅' : '❌'} Profile pic size: ${profileWidth} (expected: 60px)`);

    // Test form input styling
    const input = testContainer.querySelector('input');
    const inputBorder = getComputedStyle(input).border;
    console.log(`   ${inputBorder.includes('2px') ? '✅' : '❌'} Input border: ${inputBorder.includes('2px') ? 'Applied' : 'Missing'}`);

    console.log("\n✅ Phase 3 Component Testing Complete!");
    console.log("💡 Visual test components added to top-left corner");
    console.log("🎯 Hover over elements to test hover effects");

    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.textContent = '× Close Test Panel';
    closeBtn.style.position = 'sticky';
    closeBtn.style.top = '0';
    closeBtn.style.background = '#dc3545';
    closeBtn.style.color = 'white';
    closeBtn.style.border = 'none';
    closeBtn.style.padding = '10px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.borderRadius = '5px';
    closeBtn.style.marginBottom = '10px';
    closeBtn.onclick = () => testContainer.remove();

    testContainer.insertBefore(closeBtn, testContainer.firstChild);
}, 100);
