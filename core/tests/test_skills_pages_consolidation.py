#!/usr/bin/env python3
"""
Test suite for skills-pages.css to skill-pages.css merge
Verifies that the orphaned file removal and merge was successful
"""

import os
import sys
from pathlib import Path

class TestSkillPagesConsolidation:
    """Test suite for skill pages CSS consolidation"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.skill_pages_css = self.base_dir / "static/css/skill-pages.css"
        self.skills_pages_css = self.base_dir / "static/css/skills-pages.css"
        self.test_results = []
        
    def read_file_content(self, file_path):
        """Helper to read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def test_orphaned_file_removed(self):
        """Test that skills-pages.css file was removed"""
        if not self.skills_pages_css.exists():
            self.test_results.append("✅ Orphaned skills-pages.css file successfully removed")
        else:
            self.test_results.append("❌ skills-pages.css file still exists")
    
    def test_main_file_exists(self):
        """Test that skill-pages.css still exists and is loaded"""
        if self.skill_pages_css.exists():
            self.test_results.append("✅ Main skill-pages.css file preserved")
        else:
            self.test_results.append("❌ Main skill-pages.css file missing")
    
    def test_required_classes_present(self):
        """Test that required classes from skills-pages.css are now in skill-pages.css"""
        if not self.skill_pages_css.exists():
            self.test_results.append("❌ Cannot test - main file missing")
            return
            
        content = self.read_file_content(self.skill_pages_css)
        
        # Classes that were actually used in templates
        required_classes = [
            '.stat-icon {',  # Used in my_skills.html
            '.filter-label {', # Used in skill_filters.html
        ]
        
        failures = []
        for class_def in required_classes:
            if class_def not in content:
                failures.append(f"❌ Missing required class: {class_def}")
        
        if not failures:
            self.test_results.append("✅ All required classes preserved in skill-pages.css")
        else:
            for failure in failures:
                self.test_results.append(failure)
    
    def test_no_duplicates_created(self):
        """Test that we didn't create duplicate class definitions"""
        if not self.skill_pages_css.exists():
            return
            
        content = self.read_file_content(self.skill_pages_css)
        
        # Count base class definitions (not scoped variants)
        import re
        # Look for exact pattern: .class { (not .parent .class {)
        stat_icon_pattern = r'^\.stat-icon\s*{'
        filter_label_pattern = r'^\.filter-label\s*{'
        
        stat_icon_count = len(re.findall(stat_icon_pattern, content, re.MULTILINE))
        filter_label_count = len(re.findall(filter_label_pattern, content, re.MULTILINE))
        
        issues = []
        if stat_icon_count > 1:
            issues.append(f"❌ Duplicate .stat-icon base definitions: {stat_icon_count}")
        if filter_label_count > 1:
            issues.append(f"❌ Duplicate .filter-label definitions: {filter_label_count}")
        
        if not issues:
            self.test_results.append("✅ No duplicate class definitions created")
        else:
            for issue in issues:
                self.test_results.append(issue)
    
    def test_css_syntax_valid(self):
        """Test that CSS syntax is still valid after merge"""
        if not self.skill_pages_css.exists():
            return
            
        content = self.read_file_content(self.skill_pages_css)
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_braces == close_braces:
            self.test_results.append("✅ CSS syntax valid (balanced braces)")
        else:
            self.test_results.append(f"❌ CSS syntax issue: {open_braces} {{ vs {close_braces} }}")
    
    def test_merge_documentation(self):
        """Test that merge was properly documented"""
        if not self.skill_pages_css.exists():
            return
            
        content = self.read_file_content(self.skill_pages_css)
        
        if "MERGED FROM skills-pages.css" in content:
            self.test_results.append("✅ Merge properly documented with comments")
        else:
            self.test_results.append("⚠️  Merge not documented in comments")
    
    def run_all_tests(self):
        """Run all test methods and report results"""
        print("🧪 Skills Pages CSS Consolidation Test Suite")
        print("=" * 60)
        
        test_methods = [
            self.test_orphaned_file_removed,
            self.test_main_file_exists,
            self.test_required_classes_present,
            self.test_no_duplicates_created,
            self.test_css_syntax_valid,
            self.test_merge_documentation
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.test_results.append(f"❌ Test {test_method.__name__} failed: {e}")
        
        # Print results
        print(f"\n📋 Test Results ({len(self.test_results)} checks):")
        print("-" * 40)
        
        passed = failed = warnings = 0
        for result in self.test_results:
            print(result)
            if result.startswith("✅"):
                passed += 1
            elif result.startswith("❌"):
                failed += 1
            elif result.startswith("⚠️"):
                warnings += 1
        
        print(f"\n📊 Summary: {passed} passed, {failed} failed, {warnings} warnings")
        
        if failed == 0:
            print("🎉 Skills Pages CSS Consolidation: ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  Some tests failed - review the changes")
            return False

if __name__ == "__main__":
    tester = TestSkillPagesConsolidation()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
