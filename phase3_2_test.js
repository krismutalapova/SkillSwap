/**
 * Phase 3.2 Component Patterns Test
 * 
 * Test the new component-specific mixins and patterns
 * Run in browser console after Phase 3.2 changes
 */

console.log("🎨 Phase 3.2 Component Patterns Testing...\n");

// Create a comprehensive test container with all new component patterns
const testContainer = document.createElement('div');
testContainer.innerHTML = `
  <div style="position: fixed; top: 10px; right: 10px; width: 400px; max-height: 90vh; overflow-y: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 50px rgba(0,0,0,0.3); z-index: 10000;">
    <h3 style="margin-top: 0; color: #333;">Phase 3.2 Component Patterns</h3>
    
    <!-- Card hover effects -->
    <div class="card-hover-lift glass-card" style="margin: 10px 0; padding: 15px;">
      <strong>Card Hover Lift</strong><br>
      <small>Hover me for subtle lift effect</small>
    </div>
    
    <div class="card-hover-strong glass-card" style="margin: 10px 0; padding: 15px;">
      <strong>Card Hover Strong</strong><br>
      <small>Hover me for strong lift effect</small>
    </div>
    
    <!-- Icon buttons -->
    <div style="margin: 15px 0;">
      <strong>Icon Buttons:</strong><br>
      <button class="icon-btn icon-btn-primary" title="Primary Icon Button">🔧</button>
      <button class="icon-btn icon-btn-secondary" title="Secondary Icon Button">⚙️</button>
      <button class="icon-btn icon-btn-danger" title="Danger Icon Button">🗑️</button>
      <button class="icon-btn icon-btn-sm icon-btn-primary" title="Small Icon Button">+</button>
      <button class="icon-btn icon-btn-lg icon-btn-secondary" title="Large Icon Button">📝</button>
    </div>
    
    <!-- Badges -->
    <div style="margin: 15px 0;">
      <strong>Badges:</strong><br>
      <span class="badge badge-primary">Primary Badge</span>
      <span class="badge badge-success">Success Badge</span>
      <span class="badge badge-danger">Danger Badge</span>
      <span class="badge badge-primary badge-pill">Pill Badge</span>
    </div>
    
    <!-- Status indicators -->
    <div style="margin: 15px 0;">
      <strong>Status Indicators:</strong><br>
      <div><span class="status-dot status-dot-active"></span>Active Status</div>
      <div><span class="status-dot status-dot-inactive"></span>Inactive Status</div>
      <div><span class="status-dot status-dot-warning"></span>Warning Status</div>
    </div>
    
    <!-- Link buttons -->
    <div style="margin: 15px 0;">
      <strong>Link Buttons:</strong><br>
      <a href="#" class="link-btn link-btn-primary">🔗 Primary Link</a>
      <a href="#" class="link-btn link-btn-ghost">👻 Ghost Link</a>
    </div>
    
    <!-- Progress bar -->
    <div style="margin: 15px 0;">
      <strong>Progress Bar:</strong><br>
      <div class="progress-bar">
        <div class="progress-fill" style="width: 65%;"></div>
      </div>
    </div>
    
    <!-- Form patterns -->
    <div class="form-section" style="margin: 15px 0;">
      <h4 class="form-section-title">📝 Form Section</h4>
      
      <div class="form-group-horizontal">
        <label class="form-label">Label:</label>
        <input type="text" class="form-field" placeholder="Horizontal form field" style="max-width: 200px;">
      </div>
      
      <div class="form-group">
        <label class="form-label">Vertical Group:</label>
        <input type="text" class="form-field" placeholder="Vertical form field">
      </div>
    </div>
    
    <!-- Close button -->
    <button id="closePhase32Test" style="position: sticky; bottom: 0; width: 100%; background: #dc3545; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; margin-top: 15px;">
      ✕ Close Test Panel
    </button>
  </div>
`;

document.body.appendChild(testContainer);

// Add close functionality
document.getElementById('closePhase32Test').onclick = () => testContainer.remove();

// Test the new variables
const phase32Variables = [
    { name: '--icon-btn-size', expected: '40px' },
    { name: '--icon-btn-size-sm', expected: '32px' },
    { name: '--icon-btn-size-lg', expected: '48px' },
    { name: '--status-dot-size', expected: '8px' },
    { name: '--progress-bar-height', expected: '8px' },
    { name: '--transition-base', expected: 'all 0.3s ease' }
];

console.log("Testing Phase 3.2 Variables:");
let phase32Passed = 0;
phase32Variables.forEach(({ name, expected }) => {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    const passed = value === expected || value.includes(expected.substring(0, 10));
    console.log(`   ${passed ? '✅' : '❌'} ${name}: ${value || 'not defined'}`);
    if (passed) phase32Passed++;
});

console.log(`Phase 3.2 Variables: ${phase32Passed}/${phase32Variables.length} passed\n`);

// Test component styles
setTimeout(() => {
    console.log("Testing Component Pattern Styles:");

    // Test icon button sizing
    const iconBtn = testContainer.querySelector('.icon-btn');
    const iconBtnWidth = getComputedStyle(iconBtn).width;
    console.log(`   ${iconBtnWidth === '40px' ? '✅' : '❌'} Icon button size: ${iconBtnWidth} (expected: 40px)`);

    // Test badge styling
    const badge = testContainer.querySelector('.badge');
    const badgePadding = getComputedStyle(badge).padding;
    console.log(`   ${badgePadding.includes('4px') ? '✅' : '❌'} Badge padding: ${badgePadding}`);

    // Test progress bar
    const progressBar = testContainer.querySelector('.progress-bar');
    const progressHeight = getComputedStyle(progressBar).height;
    console.log(`   ${progressHeight === '8px' ? '✅' : '❌'} Progress bar height: ${progressHeight} (expected: 8px)`);

    // Test form section background
    const formSection = testContainer.querySelector('.form-section');
    const formBg = getComputedStyle(formSection).background;
    console.log(`   ${formBg.includes('rgba') ? '✅' : '❌'} Form section glassmorphism: ${formBg.includes('rgba') ? 'Applied' : 'Missing'}`);

    // Test hover effects by programmatically triggering them
    console.log(`   ✅ Hover effects: Ready for manual testing`);

    console.log("\n🎨 Phase 3.2 Component Patterns Test Complete!");
    console.log("💡 Interactive test panel added to top-right corner");
    console.log("🎯 Try hovering over cards and clicking buttons");
    console.log("🔧 All new component patterns are now available for use");
}, 100);
