/**
 * SkillSwap CSS Design System - Comprehensive Test Suite
 * 
 * This file contains both Node.js tests (for file system analysis) and browser tests (for live validation).
 * 
 * USAGE OPTIONS:
 * 
 * 1. NODE.JS MODE (File System Analysis):
 *    Run: node css_design_system_tests.js
 *    Tests: Phase 5.1 consolidation, file structure, utility availability
 * 
 * 2. BROWSER MODE (Live Validation):
 *    - Start Django server: python manage.py runserver
 *    - Open browser to http://127.0.0.1:8000
 *    - Open Developer Console (F12)
 *    - Copy/paste this entire file
 *    - Review test results and interactive showcase
 */

// Detect environment
const isNode = typeof window === 'undefined';

if (isNode) {
    // ============================================================================
    // NODE.JS MODE: FILE SYSTEM ANALYSIS TESTS
    // ============================================================================

    const fs = require('fs');
    const path = require('path');

    // Colors for terminal output
    const COLORS = {
        GREEN: '\x1b[32m',
        RED: '\x1b[31m',
        YELLOW: '\x1b[33m',
        BLUE: '\x1b[34m',
        CYAN: '\x1b[36m',
        MAGENTA: '\x1b[35m',
        RESET: '\x1b[0m',
        BOLD: '\x1b[1m'
    };

    class SkillSwapCSSDesignSystemTests {
        constructor() {
            this.testResults = [];
            this.cssFiles = [
                'static/css/search-page.css',
                'static/css/home-pages.css',
                'static/css/auth-pages.css',
                'static/css/components.css',
                'static/css/utilities.css',
                'static/css/base.css'
            ];
            this.templateFiles = [
                'core/templates/core/search.html',
                'core/templates/core/home.html',
                'core/templates/core/components/user_card.html',
                'core/templates/core/components/user_info_sidebar.html'
            ];
        }

        log(message, color = COLORS.RESET) {
            console.log(`${color}${message}${COLORS.RESET}`);
        }

        readFile(filePath) {
            try {
                return fs.readFileSync(filePath, 'utf8');
            } catch (error) {
                this.log(`Error reading ${filePath}: ${error.message}`, COLORS.RED);
                return '';
            }
        }

        countLines(content) {
            return content.split('\n').length;
        }

        // ===== PHASE 5.1: SEARCH PAGE CONSOLIDATION TESTS =====

        testSearchPageConsolidation() {
            this.log('\n📊 Phase 5.1.1: Search Page Consolidation', COLORS.CYAN);

            const searchPageCSS = this.readFile('static/css/search-page.css');
            const currentLines = this.countLines(searchPageCSS);

            // Test 1: Line reduction
            this.testResults.push({
                category: 'Search Page',
                test: 'Line Count Reduction',
                status: currentLines <= 335 ? 'PASS' : 'FAIL',
                message: `${currentLines} lines (target: ≤335, 9+ lines eliminated)`
            });

            // Test 2: Glassmorphism consolidation - individual patterns
            const glassmorphismPatterns = [
                /backdrop-filter:\s*blur\(\d+px\)/g,
                /background:\s*rgba\(255,\s*255,\s*255,\s*0\.\d+\)/g,
                /border:\s*1px\s*solid\s*rgba\(255,\s*255,\s*255,\s*0\.\d+\)/g
            ];

            let totalHardcodedPatterns = 0;
            glassmorphismPatterns.forEach((pattern, index) => {
                const matches = searchPageCSS.match(pattern) || [];
                totalHardcodedPatterns += matches.length;

                const patternNames = ['backdrop-filter', 'glassmorphism background', 'glassmorphism border'];
                this.testResults.push({
                    category: 'Search Page',
                    test: `${patternNames[index]} Consolidation`,
                    status: matches.length === 0 ? 'PASS' : 'WARN',
                    message: `${matches.length} hardcoded ${patternNames[index]} patterns found`
                });
            });

            // Test 3: Overall glassmorphism removal
            this.testResults.push({
                category: 'Search Page',
                test: 'Total Glassmorphism Removal',
                status: totalHardcodedPatterns === 0 ? 'PASS' : totalHardcodedPatterns <= 3 ? 'WARN' : 'FAIL',
                message: `${totalHardcodedPatterns} total hardcoded glassmorphism patterns`
            });

            // Test 4: Template utility usage
            const searchTemplate = this.readFile('core/templates/core/search.html');
            const glassCardUsage = (searchTemplate.match(/glass-card/g) || []).length;
            const primaryGradientUsage = (searchTemplate.match(/primary-gradient/g) || []).length;

            this.testResults.push({
                category: 'Search Page',
                test: 'Glass Card Utility Usage',
                status: glassCardUsage >= 3 ? 'PASS' : glassCardUsage >= 1 ? 'WARN' : 'FAIL',
                message: `${glassCardUsage} glass-card utility usages (target: ≥3)`
            });

            this.testResults.push({
                category: 'Search Page',
                test: 'Primary Gradient Utility Usage',
                status: primaryGradientUsage >= 2 ? 'PASS' : primaryGradientUsage >= 1 ? 'WARN' : 'FAIL',
                message: `${primaryGradientUsage} primary-gradient utility usages (target: ≥2)`
            });

            // Test 5: CSS Variable usage
            const cssVariablePatterns = [
                /var\(--color-/g,
                /var\(--space-/g,
                /var\(--radius-/g,
                /var\(--shadow-/g
            ];

            let totalVariableUsage = 0;
            cssVariablePatterns.forEach(pattern => {
                const matches = searchPageCSS.match(pattern) || [];
                totalVariableUsage += matches.length;
            });

            this.testResults.push({
                category: 'Search Page',
                test: 'CSS Variable Usage',
                status: totalVariableUsage >= 10 ? 'PASS' : totalVariableUsage >= 5 ? 'WARN' : 'FAIL',
                message: `${totalVariableUsage} CSS variable usages found`
            });

            // Test 6: Button consolidation
            const buttonPatterns = [
                /\.btn-primary/g,
                /\.contact-btn/g,
                /\.search-button/g
            ];

            let buttonConsolidationScore = 0;
            buttonPatterns.forEach(pattern => {
                const matches = searchPageCSS.match(pattern) || [];
                if (matches.length > 0) buttonConsolidationScore++;
            });

            this.testResults.push({
                category: 'Search Page',
                test: 'Button Class Consolidation',
                status: buttonConsolidationScore >= 2 ? 'PASS' : buttonConsolidationScore >= 1 ? 'WARN' : 'FAIL',
                message: `${buttonConsolidationScore}/3 button utility classes found in search page`
            });

            // Test 7: Duplicate pattern removal
            const duplicatePatterns = [
                /box-shadow:\s*0\s*\d+px\s*\d+px\s*rgba\(0,\s*0,\s*0,\s*0\.\d+\)/g,
                /transition:\s*all\s*0\.\d+s\s*ease/g,
                /border-radius:\s*15px/g
            ];

            let duplicateCount = 0;
            duplicatePatterns.forEach(pattern => {
                const matches = searchPageCSS.match(pattern) || [];
                duplicateCount += Math.max(0, matches.length - 1); // Count extras beyond first usage
            });

            this.testResults.push({
                category: 'Search Page',
                test: 'Duplicate Pattern Removal',
                status: duplicateCount <= 2 ? 'PASS' : duplicateCount <= 5 ? 'WARN' : 'FAIL',
                message: `${duplicateCount} potential duplicate patterns detected`
            });
        }

        // ===== PHASE 5.1: USER CARD CONSOLIDATION TESTS =====

        testUserCardConsolidation() {
            this.log('\n📋 Phase 5.1.2: User Card Component Consolidation', COLORS.CYAN);

            const componentsCSS = this.readFile('static/css/components.css');
            const userCardPattern = /\.user-card\s*{[^}]*}/gs;
            const matches = componentsCSS.match(userCardPattern);

            if (!matches) {
                this.testResults.push({
                    category: 'User Card',
                    test: 'CSS Class Exists',
                    status: 'FAIL',
                    message: '.user-card class not found in components.css'
                });
                return;
            }

            const userCardBlock = matches[0];

            // Test 1: Check for CSS class existence and basic structure
            this.testResults.push({
                category: 'User Card',
                test: 'CSS Class Exists',
                status: 'PASS',
                message: '.user-card class found in components.css'
            });

            // Test 2: Individual glassmorphism pattern removal
            const glassmorphismPatterns = [
                { pattern: 'backdrop-filter:', name: 'backdrop-filter' },
                { pattern: 'background: rgba(255, 255, 255,', name: 'glassmorphism background' },
                { pattern: 'border: 1px solid rgba(255, 255, 255,', name: 'glassmorphism border' },
                { pattern: 'box-shadow: 0 8px 32px rgba(0, 0, 0,', name: 'glassmorphism shadow' }
            ];

            let hasAnyHardcodedGlass = false;
            glassmorphismPatterns.forEach(({ pattern, name }) => {
                const hasPattern = userCardBlock.includes(pattern);
                if (hasPattern) hasAnyHardcodedGlass = true;

                this.testResults.push({
                    category: 'User Card',
                    test: `${name} Removal`,
                    status: !hasPattern ? 'PASS' : 'FAIL',
                    message: hasPattern ? `Still contains hardcoded ${name}` : `${name} properly removed`
                });
            });

            // Test 3: Overall glassmorphism consolidation
            this.testResults.push({
                category: 'User Card',
                test: 'Overall Glassmorphism Removal',
                status: !hasAnyHardcodedGlass ? 'PASS' : 'FAIL',
                message: hasAnyHardcodedGlass ? 'Contains hardcoded glassmorphism patterns' : 'All glassmorphism patterns removed'
            });

            // Test 4: Template utility usage analysis
            const templateFiles = [
                'core/templates/core/components/user_card.html',
                'core/templates/core/search.html',
                'core/templates/core/components/user_info_sidebar.html'
            ];

            let totalGlassCardUsage = 0;
            let totalPrimaryGradientUsage = 0;
            let templatesWithUtilities = 0;

            templateFiles.forEach(templateFile => {
                const content = this.readFile(templateFile);
                if (content) {
                    const glassCardCount = (content.match(/glass-card/g) || []).length;
                    const primaryGradientCount = (content.match(/primary-gradient/g) || []).length;

                    totalGlassCardUsage += glassCardCount;
                    totalPrimaryGradientUsage += primaryGradientCount;

                    if (glassCardCount > 0 || primaryGradientCount > 0) {
                        templatesWithUtilities++;
                    }

                    this.testResults.push({
                        category: 'User Card',
                        test: `${templateFile.split('/').pop()} Utility Usage`,
                        status: (glassCardCount > 0 || primaryGradientCount > 0) ? 'PASS' : 'WARN',
                        message: `glass-card: ${glassCardCount}, primary-gradient: ${primaryGradientCount}`
                    });
                }
            });

            // Test 5: Overall template utility adoption
            this.testResults.push({
                category: 'User Card',
                test: 'Template Utility Adoption',
                status: templatesWithUtilities >= 2 ? 'PASS' : templatesWithUtilities >= 1 ? 'WARN' : 'FAIL',
                message: `${templatesWithUtilities}/${templateFiles.length} templates using utilities`
            });

            // Test 6: Primary gradient usage in templates
            this.testResults.push({
                category: 'User Card',
                test: 'Primary Gradient Usage',
                status: totalPrimaryGradientUsage >= 2 ? 'PASS' : totalPrimaryGradientUsage >= 1 ? 'WARN' : 'FAIL',
                message: `${totalPrimaryGradientUsage} primary-gradient usages across templates`
            });

            // Test 7: Utility class availability
            const utilitiesCSS = this.readFile('static/css/utilities.css');
            const baseCSS = this.readFile('static/css/base.css');

            const requiredUtilities = [
                { class: '.glass-card', file: 'utilities.css', content: utilitiesCSS },
                { class: '.primary-gradient', file: 'base.css', content: baseCSS },
                { class: '.user-name', file: 'utilities.css', content: utilitiesCSS },
                { class: '.user-bio', file: 'utilities.css', content: utilitiesCSS },
                { class: '.profile-pic', file: 'utilities.css', content: utilitiesCSS },
                { class: '.contact-btn', file: 'utilities.css', content: utilitiesCSS }
            ];

            let availableUtilities = 0;
            requiredUtilities.forEach(({ class: utility, file, content }) => {
                const hasUtility = content.includes(utility + ' {') ||
                    content.includes(utility + '{') ||
                    content.includes(utility + ',');

                if (hasUtility) availableUtilities++;

                this.testResults.push({
                    category: 'User Card',
                    test: `${utility} Utility Available`,
                    status: hasUtility ? 'PASS' : 'FAIL',
                    message: hasUtility ? `Available in ${file}` : `Missing from ${file}`
                });
            });

            // Test 8: Overall utility availability
            this.testResults.push({
                category: 'User Card',
                test: 'Utility System Coverage',
                status: availableUtilities >= 5 ? 'PASS' : availableUtilities >= 3 ? 'WARN' : 'FAIL',
                message: `${availableUtilities}/${requiredUtilities.length} required utilities available`
            });

            // Test 9: Remaining hardcoded patterns check
            const hardcodedPatterns = [
                /color:\s*#[0-9a-fA-F]{3,6}/g,
                /font-size:\s*\d+px/g,
                /padding:\s*\d+px/g,
                /margin:\s*\d+px/g
            ];

            let hardcodedCount = 0;
            hardcodedPatterns.forEach(pattern => {
                const matches = userCardBlock.match(pattern) || [];
                hardcodedCount += matches.length;
            });

            this.testResults.push({
                category: 'User Card',
                test: 'Hardcoded Values Reduction',
                status: hardcodedCount <= 5 ? 'PASS' : hardcodedCount <= 10 ? 'WARN' : 'FAIL',
                message: `${hardcodedCount} hardcoded values found (colors, sizes, spacing)`
            });
        }

        // ===== PHASE 5.1: COMPREHENSIVE CONSOLIDATION ANALYSIS =====

        testPhase51ComprehensiveAnalysis() {
            this.log('\n🔬 Phase 5.1: Comprehensive Consolidation Analysis', COLORS.CYAN);

            // Cross-file pattern analysis
            const allCSSFiles = [
                'static/css/search-page.css',
                'static/css/components.css',
                'static/css/utilities.css',
                'static/css/base.css'
            ];

            let totalGlassmorphismPatterns = 0;
            let totalHardcodedGradients = 0;
            let totalCSSVariableUsage = 0;

            allCSSFiles.forEach(filePath => {
                const content = this.readFile(filePath);

                // Count glassmorphism patterns
                const glassPatterns = content.match(/backdrop-filter:\s*blur\(\d+px\)/g) || [];
                totalGlassmorphismPatterns += glassPatterns.length;

                // Count hardcoded gradients
                const gradientPatterns = content.match(/linear-gradient\([^)]+\)/g) || [];
                totalHardcodedGradients += gradientPatterns.length;

                // Count CSS variable usage
                const variablePatterns = content.match(/var\(--[^)]+\)/g) || [];
                totalCSSVariableUsage += variablePatterns.length;
            });

            // Test 1: Overall glassmorphism consolidation across all files
            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'Cross-File Glassmorphism Consolidation',
                status: totalGlassmorphismPatterns <= 3 ? 'PASS' : totalGlassmorphismPatterns <= 8 ? 'WARN' : 'FAIL',
                message: `${totalGlassmorphismPatterns} glassmorphism patterns across all CSS files`
            });

            // Test 2: Gradient consolidation analysis
            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'Gradient Consolidation',
                status: totalHardcodedGradients <= 10 ? 'PASS' : totalHardcodedGradients <= 20 ? 'WARN' : 'FAIL',
                message: `${totalHardcodedGradients} hardcoded gradients found (target: use .primary-gradient utility)`
            });

            // Test 3: CSS variable adoption rate
            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'CSS Variable Adoption',
                status: totalCSSVariableUsage >= 50 ? 'PASS' : totalCSSVariableUsage >= 25 ? 'WARN' : 'FAIL',
                message: `${totalCSSVariableUsage} CSS variable usages across all files`
            });

            // Test 4: Template consistency check
            const templateFiles = [
                'core/templates/core/search.html',
                'core/templates/core/components/user_card.html',
                'core/templates/core/components/user_info_sidebar.html'
            ];

            let templatesUsingUtilities = 0;
            let totalUtilityUsage = 0;

            templateFiles.forEach(templateFile => {
                const content = this.readFile(templateFile);
                if (content) {
                    const utilityClasses = [
                        'glass-card', 'primary-gradient', 'btn-primary',
                        'user-name', 'user-bio', 'profile-pic', 'contact-btn', 'skill-tag'
                    ];

                    let fileUtilityCount = 0;
                    utilityClasses.forEach(utility => {
                        const matches = content.match(new RegExp(utility, 'g')) || [];
                        fileUtilityCount += matches.length;
                    });

                    totalUtilityUsage += fileUtilityCount;
                    if (fileUtilityCount > 0) templatesUsingUtilities++;
                }
            });

            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'Template Utility Consistency',
                status: templatesUsingUtilities >= 2 ? 'PASS' : templatesUsingUtilities >= 1 ? 'WARN' : 'FAIL',
                message: `${templatesUsingUtilities}/${templateFiles.length} templates using utility classes`
            });

            // Test 5: Overall utility density
            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'Utility Usage Density',
                status: totalUtilityUsage >= 15 ? 'PASS' : totalUtilityUsage >= 8 ? 'WARN' : 'FAIL',
                message: `${totalUtilityUsage} total utility class usages in templates`
            });

            // Test 6: Component modernization score
            const modernizationFactors = [
                { condition: totalGlassmorphismPatterns <= 3, weight: 25 },
                { condition: totalUtilityUsage >= 15, weight: 25 },
                { condition: templatesUsingUtilities >= 2, weight: 25 },
                { condition: totalCSSVariableUsage >= 50, weight: 25 }
            ];

            let modernizationScore = 0;
            modernizationFactors.forEach(factor => {
                if (factor.condition) modernizationScore += factor.weight;
            });

            this.testResults.push({
                category: 'Phase 5.1 Analysis',
                test: 'Component Modernization Score',
                status: modernizationScore >= 75 ? 'PASS' : modernizationScore >= 50 ? 'WARN' : 'FAIL',
                message: `${modernizationScore}/100 modernization score (glassmorphism + utilities + variables + templates)`
            });
        }

        // ===== UTILITY SYSTEM TESTS =====

        testUtilitySystem() {
            this.log('\n🔧 Utility System Analysis', COLORS.CYAN);

            const utilitiesCSS = this.readFile('static/css/utilities.css');
            const baseCSS = this.readFile('static/css/base.css');

            const coreUtilities = [
                { class: '.glass-card', file: 'utilities.css', content: utilitiesCSS },
                { class: '.primary-gradient', file: 'base.css', content: baseCSS },
                { class: '.btn-primary', file: 'utilities.css', content: utilitiesCSS },
                { class: '.user-name', file: 'utilities.css', content: utilitiesCSS },
                { class: '.user-bio', file: 'utilities.css', content: utilitiesCSS },
                { class: '.profile-pic', file: 'utilities.css', content: utilitiesCSS },
                { class: '.contact-btn', file: 'utilities.css', content: utilitiesCSS },
                { class: '.skill-tag', file: 'utilities.css', content: utilitiesCSS }
            ];

            let utilityCount = 0;
            coreUtilities.forEach(({ class: utility, file, content }) => {
                const hasUtility = content.includes(utility + ' {') ||
                    content.includes(utility + '{') ||
                    content.includes(utility + ',');

                if (hasUtility) utilityCount++;

                this.testResults.push({
                    category: 'Utilities',
                    test: `${utility} Availability`,
                    status: hasUtility ? 'PASS' : 'FAIL',
                    message: hasUtility ? `Available in ${file}` : `Missing from ${file}`
                });
            });

            // Overall utility coverage
            const utilityDensity = (utilitiesCSS.match(/\.[a-z-]+\s*{/g) || []).length;
            this.testResults.push({
                category: 'Utilities',
                test: 'Utility System Coverage',
                status: utilityDensity >= 200 ? 'PASS' : 'WARN',
                message: `${utilityDensity} utility classes found`
            });
        }

        // ===== DESIGN SYSTEM CONSISTENCY TESTS =====

        testDesignSystemConsistency() {
            this.log('\n🎛️ Design System Consistency', COLORS.CYAN);

            const allCSS = this.cssFiles.map(file => this.readFile(file)).join('\n');

            // CSS Variable Usage
            const variablePatterns = [
                'var\\(--color-primary',
                'var\\(--space-',
                'var\\(--font-size-',
                'var\\(--border-radius-',
                'var\\(--shadow-',
                'var\\(--transition-'
            ];

            let totalVariableUsage = 0;
            variablePatterns.forEach(pattern => {
                const matches = (allCSS.match(new RegExp(pattern, 'g')) || []).length;
                totalVariableUsage += matches;
            });

            this.testResults.push({
                category: 'Design System',
                test: 'CSS Variable Usage',
                status: totalVariableUsage >= 100 ? 'PASS' : 'WARN',
                message: `${totalVariableUsage} CSS variable usages found`
            });

            // Color Consistency
            const hardcodedColors = allCSS.match(/#[0-9a-fA-F]{3,6}/g) || [];
            const uniqueHardcodedColors = [...new Set(hardcodedColors)];

            this.testResults.push({
                category: 'Design System',
                test: 'Color System Consistency',
                status: uniqueHardcodedColors.length <= 20 ? 'PASS' : 'WARN',
                message: `${uniqueHardcodedColors.length} unique hardcoded colors (target: ≤20)`
            });
        }

        // ===== CODE QUALITY ANALYSIS =====

        testCodeQuality() {
            this.log('\n🔍 Code Quality Analysis', COLORS.CYAN);

            let totalLines = 0;
            let duplicatePatternCount = 0;

            this.cssFiles.forEach(filePath => {
                const content = this.readFile(filePath);
                const lines = this.countLines(content);
                totalLines += lines;

                // Check for common duplicate patterns
                const duplicatePatterns = [
                    /backdrop-filter:\s*blur\(\d+px\)/g,
                    /border:\s*1px\s*solid\s*rgba\(255,\s*255,\s*255,\s*0\.\d+\)/g,
                    /box-shadow:\s*0\s*\d+px\s*\d+px\s*rgba\(0,\s*0,\s*0,\s*0\.\d+\)/g
                ];

                duplicatePatterns.forEach(pattern => {
                    const matches = content.match(pattern) || [];
                    duplicatePatternCount += matches.length;
                });
            });

            this.testResults.push({
                category: 'Code Quality',
                test: 'Total CSS Size',
                status: totalLines <= 6500 ? 'PASS' : 'WARN',
                message: `${totalLines} total lines across ${this.cssFiles.length} files`
            });

            this.testResults.push({
                category: 'Code Quality',
                test: 'Duplicate Pattern Analysis',
                status: duplicatePatternCount <= 10 ? 'PASS' : 'WARN',
                message: `${duplicatePatternCount} potential duplicate patterns found`
            });
        }

        // ===== PHASE 5 PROGRESS ASSESSMENT =====

        testPhase5Progress() {
            this.log('\n📈 Phase 5 Progress Assessment', COLORS.CYAN);

            // Calculate completion based on test results
            const phase51Tests = this.testResults.filter(r =>
                r.category === 'Search Page' || r.category === 'User Card'
            );
            const phase51Passed = phase51Tests.filter(r => r.status === 'PASS').length;
            const phase51Progress = phase51Tests.length > 0 ? (phase51Passed / phase51Tests.length) * 100 : 0;

            this.testResults.push({
                category: 'Phase 5',
                test: 'Phase 5.1 Completion',
                status: phase51Progress >= 80 ? 'PASS' : phase51Progress >= 60 ? 'WARN' : 'FAIL',
                message: `${phase51Progress.toFixed(1)}% complete (search page + user card consolidation)`
            });

            // Check readiness for Phase 5.2
            const systemTests = this.testResults.filter(r =>
                r.category === 'Utilities' || r.category === 'Design System'
            );
            const systemPassed = systemTests.filter(r => r.status === 'PASS').length;
            const systemHealth = systemTests.length > 0 ? (systemPassed / systemTests.length) * 100 : 0;

            this.testResults.push({
                category: 'Phase 5',
                test: 'Phase 5.2 Readiness',
                status: systemHealth >= 75 ? 'PASS' : 'WARN',
                message: `${systemHealth.toFixed(1)}% system health (ready for home-pages.css consolidation)`
            });
        }

        // ===== RESULTS DISPLAY =====

        generateSummary() {
            const passed = this.testResults.filter(r => r.status === 'PASS').length;
            const failed = this.testResults.filter(r => r.status === 'FAIL').length;
            const warnings = this.testResults.filter(r => r.status === 'WARN').length;
            const total = this.testResults.length;

            return { passed, failed, warnings, total };
        }

        displayResults() {
            this.log('\n' + '='.repeat(100), COLORS.BOLD);
            this.log('SKILLSWAP CSS DESIGN SYSTEM - COMPREHENSIVE TEST RESULTS', COLORS.BOLD);
            this.log('='.repeat(100), COLORS.BOLD);

            // Group results by category
            const categories = {};
            this.testResults.forEach(result => {
                if (!categories[result.category]) {
                    categories[result.category] = [];
                }
                categories[result.category].push(result);
            });

            Object.entries(categories).forEach(([category, results]) => {
                this.log(`\n${COLORS.BOLD}${COLORS.MAGENTA}📁 ${category}${COLORS.RESET}`);
                this.log('-'.repeat(60), COLORS.CYAN);

                results.forEach(result => {
                    const color = result.status === 'PASS' ? COLORS.GREEN :
                        result.status === 'FAIL' ? COLORS.RED : COLORS.YELLOW;
                    const icon = result.status === 'PASS' ? '✅' :
                        result.status === 'FAIL' ? '❌' : '⚠️';

                    this.log(`${icon} [${result.status}] ${result.test}`, color);
                    this.log(`   ${result.message}`, COLORS.RESET);
                });
            });

            const summary = this.generateSummary();

            this.log('\n' + '='.repeat(100), COLORS.BOLD);
            this.log('OVERALL SUMMARY', COLORS.BOLD);
            this.log('='.repeat(100), COLORS.BOLD);
            this.log(`Total Tests: ${summary.total}`, COLORS.CYAN);
            this.log(`✅ Passed: ${summary.passed}`, COLORS.GREEN);
            this.log(`❌ Failed: ${summary.failed}`, COLORS.RED);
            this.log(`⚠️  Warnings: ${summary.warnings}`, COLORS.YELLOW);

            const successRate = ((summary.passed / summary.total) * 100).toFixed(1);
            this.log(`\nSuccess Rate: ${successRate}%`,
                successRate >= 85 ? COLORS.GREEN :
                    successRate >= 70 ? COLORS.YELLOW : COLORS.RED);

            // Recommendations
            this.log('\n' + '='.repeat(100), COLORS.BOLD);
            this.log('RECOMMENDATIONS', COLORS.BOLD);
            this.log('='.repeat(100), COLORS.BOLD);

            if (summary.failed === 0 && summary.warnings <= 8) {
                this.log('🎉 CSS Design System is in excellent condition!', COLORS.GREEN);
                this.log('✨ Ready to proceed with Phase 5.2: home-pages.css consolidation', COLORS.CYAN);
            } else if (summary.failed > 0) {
                this.log('❌ Critical issues detected - fix failed tests first', COLORS.RED);
                this.log('🔧 Focus on utility system and consolidation issues', COLORS.YELLOW);
            } else {
                this.log('⚠️  Good progress with minor improvements needed', COLORS.YELLOW);
                this.log('✅ Safe to proceed with caution', COLORS.CYAN);
            }

            this.log('\n📋 Run browser tests for live component validation:', COLORS.CYAN);
            this.log('   1. Start server: python manage.py runserver', COLORS.RESET);
            this.log('   2. Open browser and console', COLORS.RESET);
            this.log('   3. Copy/paste this file for interactive tests', COLORS.RESET);
        }

        // ===== MAIN TEST RUNNER =====

        runAllTests() {
            this.log(`${COLORS.BOLD}${COLORS.BLUE}🧪 SKILLSWAP CSS DESIGN SYSTEM TEST SUITE${COLORS.RESET}`);
            this.log(`${COLORS.CYAN}Comprehensive analysis of CSS consolidation, utilities, and design system...${COLORS.RESET}\n`);

            this.testSearchPageConsolidation();
            this.testUserCardConsolidation();
            this.testPhase51ComprehensiveAnalysis();
            this.testUtilitySystem();
            this.testDesignSystemConsistency();
            this.testCodeQuality();
            this.testPhase5Progress();

            this.displayResults();

            return this.generateSummary();
        }
    }

    // Execute Node.js tests
    const tester = new SkillSwapCSSDesignSystemTests();
    const results = tester.runAllTests();

    // Export for potential module usage
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { SkillSwapCSSDesignSystemTests, results };
    }

} else {
    // ============================================================================
    // BROWSER MODE: LIVE VALIDATION TESTS
    // ============================================================================

    console.clear();
    console.log("🧪 SkillSwap CSS Design System - Live Browser Test Suite");
    console.log("=".repeat(75));
    console.log("Testing live CSS variables, utility classes, components, and performance\n");

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

            // Shadows and Effects
            { name: '--shadow-card', expectedContains: 'rgba', category: 'effects' },
            { name: '--blur-glass', expected: '10px', category: 'effects' }
        ];

        const results = { passed: 0, total: coreVariables.length, categories: {} };
        const computedStyle = getComputedStyle(document.documentElement);

        coreVariables.forEach(variable => {
            const value = computedStyle.getPropertyValue(variable.name).trim();
            let passed = false;

            if (variable.expected) {
                passed = value === variable.expected;
            } else if (variable.expectedContains) {
                passed = value.includes(variable.expectedContains);
            }

            if (!results.categories[variable.category]) {
                results.categories[variable.category] = { passed: 0, total: 0 };
            }
            results.categories[variable.category].total++;

            if (passed) {
                results.passed++;
                results.categories[variable.category].passed++;
                console.log(`✅ ${variable.name}: ${value}`);
            } else {
                console.log(`❌ ${variable.name}: ${value || 'MISSING'} (expected: ${variable.expected || 'contains ' + variable.expectedContains})`);
            }
        });

        // Category summary
        console.log("\n📊 Variable Categories:");
        Object.entries(results.categories).forEach(([category, stats]) => {
            const percentage = ((stats.passed / stats.total) * 100).toFixed(1);
            const icon = stats.passed === stats.total ? '✅' : stats.passed > 0 ? '⚠️' : '❌';
            console.log(`${icon} ${category}: ${stats.passed}/${stats.total} (${percentage}%)`);
        });

        return results;
    }

    // ============================================================================
    // UTILITY CLASSES TEST
    // ============================================================================

    function testUtilityClasses() {
        console.log("\n2️⃣ Utility Classes");
        console.log("-".repeat(40));

        const utilityTests = [
            // Layout utilities
            { class: 'glass-card', property: 'backdrop-filter', expectedContains: 'blur' },
            { class: 'primary-gradient', property: 'background-image', expectedContains: 'gradient' },
            { class: 'btn-primary', property: 'background', expectedContains: 'gradient' },

            // Typography utilities  
            { class: 'user-name', property: 'font-weight', expected: '500' },
            { class: 'user-bio', property: 'color', expectedContains: '#' },

            // Component utilities
            { class: 'profile-pic', property: 'border-radius', expected: '50%' },
            { class: 'contact-btn', property: 'padding', expectedContains: 'px' },
            { class: 'skill-tag', property: 'border-radius', expectedContains: 'px' },

            // Interactive utilities
            { class: 'hover-lift', property: 'transition', expectedContains: 'transform' },
            { class: 'fade-in', property: 'animation', expectedContains: 'fade' }
        ];

        const results = { passed: 0, total: utilityTests.length, details: [] };

        utilityTests.forEach(test => {
            // Create test element
            const testElement = document.createElement('div');
            testElement.className = test.class;
            testElement.style.visibility = 'hidden';
            testElement.style.position = 'absolute';
            document.body.appendChild(testElement);

            const computedStyle = getComputedStyle(testElement);
            const value = computedStyle.getPropertyValue(test.property);
            let passed = false;

            if (test.expected) {
                passed = value === test.expected;
            } else if (test.expectedContains) {
                passed = value.includes(test.expectedContains);
            }

            if (passed) {
                results.passed++;
                console.log(`✅ .${test.class} → ${test.property}: ${value}`);
            } else {
                console.log(`❌ .${test.class} → ${test.property}: ${value || 'MISSING'}`);
            }

            results.details.push({
                class: test.class,
                property: test.property,
                value: value,
                passed: passed
            });

            // Cleanup
            document.body.removeChild(testElement);
        });

        return results;
    }

    // ============================================================================
    // COMPONENT INTEGRATION TEST
    // ============================================================================

    function testComponentIntegration() {
        console.log("\n3️⃣ Component Integration");
        console.log("-".repeat(40));

        const components = [
            { selector: '.user-card', name: 'User Card' },
            { selector: '.search-header', name: 'Search Header' },
            { selector: '.glass-card', name: 'Glass Card' },
            { selector: '.btn-primary', name: 'Primary Button' },
            { selector: '.skill-tag', name: 'Skill Tag' },
            { selector: '.profile-pic', name: 'Profile Picture' },
            { selector: '.nav-link', name: 'Navigation Link' }
        ];

        const results = { found: 0, working: 0, total: components.length, details: [] };

        components.forEach(component => {
            const elements = document.querySelectorAll(component.selector);
            const found = elements.length > 0;
            let working = false;

            if (found) {
                results.found++;
                const firstElement = elements[0];
                const computedStyle = getComputedStyle(firstElement);

                // Basic styling check
                const hasBackground = computedStyle.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
                    computedStyle.backgroundImage !== 'none';
                const hasSizing = computedStyle.width !== 'auto' || computedStyle.height !== 'auto' ||
                    computedStyle.padding !== '0px' || computedStyle.margin !== '0px';

                working = hasBackground || hasSizing;
                if (working) results.working++;
            }

            const status = found ? (working ? '✅' : '⚠️') : '❌';
            console.log(`${status} ${component.name}: ${elements.length} element(s) found${working ? ' (styled)' : found ? ' (unstyled)' : ''}`);

            results.details.push({
                name: component.name,
                selector: component.selector,
                count: elements.length,
                found: found,
                working: working
            });
        });

        return results;
    }

    // ============================================================================
    // BUTTON CONSOLIDATION TEST
    // ============================================================================

    function testButtonConsolidation() {
        console.log("\n4️⃣ Button Consolidation");
        console.log("-".repeat(40));

        const buttonTests = [
            { selector: '.btn-primary', name: 'Primary Button' },
            { selector: '.btn-secondary', name: 'Secondary Button' },
            { selector: '.contact-btn', name: 'Contact Button' },
            { selector: '.user-card-action-button', name: 'User Card Action Button' },
            { selector: '.search-button', name: 'Search Button' }
        ];

        const results = { consolidated: 0, total: buttonTests.length, details: [] };

        buttonTests.forEach(test => {
            const elements = document.querySelectorAll(test.selector);
            let isConsolidated = false;

            if (elements.length > 0) {
                const firstElement = elements[0];
                const computedStyle = getComputedStyle(firstElement);

                // Check if using consolidated patterns
                const hasGradient = computedStyle.backgroundImage.includes('gradient');
                const hasProperTransition = computedStyle.transition.includes('all') ||
                    computedStyle.transition.includes('transform');
                const hasConsistentPadding = computedStyle.padding !== '0px';

                isConsolidated = hasGradient && hasProperTransition && hasConsistentPadding;
                if (isConsolidated) results.consolidated++;
            }

            const status = elements.length === 0 ? '⚪' : isConsolidated ? '✅' : '❌';
            console.log(`${status} ${test.name}: ${elements.length} element(s)${isConsolidated ? ' (consolidated)' : elements.length > 0 ? ' (needs consolidation)' : ''}`);

            results.details.push({
                name: test.name,
                selector: test.selector,
                count: elements.length,
                consolidated: isConsolidated
            });
        });

        return results;
    }

    // ============================================================================
    // PERFORMANCE ANALYSIS
    // ============================================================================

    function testPerformance() {
        console.log("\n5️⃣ Performance Analysis");
        console.log("-".repeat(40));

        const performanceResults = {
            variableAccessTime: 0,
            renderTime: 0,
            cssFileCount: 0,
            totalRules: 0
        };

        // Test CSS variable access speed
        const startTime = performance.now();
        const testElement = document.createElement('div');
        document.body.appendChild(testElement);

        for (let i = 0; i < 1000; i++) {
            getComputedStyle(testElement).getPropertyValue('--color-primary');
        }

        const endTime = performance.now();
        performanceResults.variableAccessTime = endTime - startTime;
        document.body.removeChild(testElement);

        // Count CSS rules
        let totalRules = 0;
        for (let i = 0; i < document.styleSheets.length; i++) {
            try {
                const stylesheet = document.styleSheets[i];
                if (stylesheet.cssRules) {
                    totalRules += stylesheet.cssRules.length;
                }
            } catch (e) {
                // Cross-origin or other access issues
            }
        }
        performanceResults.totalRules = totalRules;
        performanceResults.cssFileCount = document.styleSheets.length;

        console.log(`📊 CSS Variable Access: ${performanceResults.variableAccessTime.toFixed(2)}ms (1000 calls)`);
        console.log(`📄 CSS Files Loaded: ${performanceResults.cssFileCount}`);
        console.log(`📏 Total CSS Rules: ${performanceResults.totalRules}`);

        // Performance recommendations
        if (performanceResults.variableAccessTime > 5) {
            console.log('⚠️  CSS variable access is slow - consider optimization');
        } else {
            console.log('✅ CSS variable access performance is good');
        }

        if (performanceResults.totalRules > 5000) {
            console.log('⚠️  High CSS rule count - consider consolidation');
        } else {
            console.log('✅ CSS rule count is reasonable');
        }

        return performanceResults;
    }

    // ============================================================================
    // INTERACTIVE COMPONENT SHOWCASE
    // ============================================================================

    function createInteractiveShowcase() {
        console.log("\n6️⃣ Interactive Component Showcase");
        console.log("-".repeat(40));

        // Create showcase container
        const showcase = document.createElement('div');
        showcase.id = 'css-test-showcase';
        showcase.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 300px;
            max-height: 80vh;
            overflow-y: auto;
            background: var(--color-background, #f8f9fa);
            border: 2px solid var(--color-primary, #6441a5);
            border-radius: var(--radius-card, 15px);
            padding: 20px;
            z-index: 10000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: var(--shadow-card, 0 8px 32px rgba(0,0,0,0.1));
            backdrop-filter: blur(10px);
        `;

        showcase.innerHTML = `
            <h3 style="margin: 0 0 15px 0; color: var(--color-primary, #6441a5);">🧪 CSS Test Showcase</h3>
            <button class="btn-primary" style="width: 100%; margin-bottom: 10px;">Primary Button</button>
            <div class="glass-card" style="padding: 15px; margin-bottom: 10px;">
                <h4 style="margin: 0 0 10px 0;">Glass Card</h4>
                <p style="margin: 0; font-size: 14px;">Testing glassmorphism effect</p>
            </div>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                <span class="skill-tag">JavaScript</span>
                <span class="skill-tag">Python</span>
            </div>
            <div class="user-header" style="margin-bottom: 10px;">
                <div class="profile-pic" style="width: 40px; height: 40px; background: var(--color-primary-gradient, linear-gradient(135deg, #6441a5, #667eea));"></div>
                <div class="user-info" style="margin-left: 10px;">
                    <h4 class="user-name" style="margin: 0;">Test User</h4>
                    <p style="margin: 0; font-size: 12px; color: #666;">Test Location</p>
                </div>
            </div>
            <button onclick="document.getElementById('css-test-showcase').remove()" 
                    style="width: 100%; padding: 8px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Close Showcase
            </button>
        `;

        // Remove existing showcase if present
        const existing = document.getElementById('css-test-showcase');
        if (existing) existing.remove();

        document.body.appendChild(showcase);
        console.log('✅ Interactive showcase created (top-right corner)');

        return showcase;
    }

    // ============================================================================
    // COMPREHENSIVE TEST RUNNER
    // ============================================================================

    function runComprehensiveTests() {
        const startTime = performance.now();

        console.log("🚀 Starting comprehensive CSS design system tests...\n");

        const variableResults = testDesignSystemVariables();
        const utilityResults = testUtilityClasses();
        const componentResults = testComponentIntegration();
        const buttonConsolidationResults = testButtonConsolidation();
        const performanceResults = testPerformance();

        // Create interactive showcase
        const showcase = createInteractiveShowcase();

        const endTime = performance.now();
        const totalTime = endTime - startTime;

        // Calculate overall results
        const totalTests = variableResults.total + utilityResults.total + componentResults.total + buttonConsolidationResults.total;
        const totalPassed = variableResults.passed + utilityResults.passed + componentResults.working + buttonConsolidationResults.consolidated;
        const overallPercentage = ((totalPassed / totalTests) * 100).toFixed(1);

        console.log("\n" + "=".repeat(75));
        console.log("📊 COMPREHENSIVE TEST RESULTS");
        console.log("=".repeat(75));
        console.log(`⏱️  Total execution time: ${totalTime.toFixed(2)}ms`);
        console.log(`📊 Overall success rate: ${overallPercentage}% (${totalPassed}/${totalTests})`);
        console.log(`📦 Design variables: ${variableResults.passed}/${variableResults.total} working`);
        console.log(`🛠️  Utility classes: ${utilityResults.passed}/${utilityResults.total} working`);
        console.log(`🧩 Components: ${componentResults.working}/${componentResults.found} styled`);
        console.log(`🔘 Button consolidation: ${buttonConsolidationResults.consolidated}/${buttonConsolidationResults.total} consolidated`);

        // Final assessment
        console.log("\n" + "=".repeat(75));
        console.log("🎯 DESIGN SYSTEM HEALTH ASSESSMENT");
        console.log("=".repeat(75));

        if (overallPercentage >= 90) {
            console.log("\n🎉 EXCELLENT: CSS design system is in outstanding condition!");
        } else if (overallPercentage >= 75) {
            console.log("\n✨ GOOD: Most CSS features working, minor issues detected");
        } else if (overallPercentage >= 50) {
            console.log("\n⚠️  NEEDS WORK: Significant CSS issues need attention");
        } else {
            console.log("\n❌ CRITICAL: Major CSS design system problems detected");
        }

        console.log("\n💡 Next Steps:");
        if (variableResults.passed < variableResults.total) {
            console.log("   - Fix missing/incorrect CSS variables");
        }
        if (utilityResults.passed < utilityResults.total) {
            console.log("   - Review utility class definitions");
        }
        if (componentResults.working < componentResults.found) {
            console.log("   - Check component CSS integration");
        }
        if (performanceResults.variableAccessTime > 1) {
            console.log("   - Consider CSS performance optimization");
        }

        console.log("\n🔄 Rerun: Copy/paste this script again to retest");
        console.log("📊 Node.js mode: Run 'node css_design_system_tests.js' for file analysis");

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
    // EXECUTE BROWSER TESTS
    // ============================================================================

    // Run the comprehensive test suite - Use var to allow re-declaration
    if (typeof testResults !== 'undefined') {
        delete window.testResults;
        delete window.skillswapTestResults;
    }

    var testResults = runComprehensiveTests();

    // Store results globally for further inspection
    window.skillswapTestResults = testResults;
}
