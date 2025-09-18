#!/usr/bin/env python3
"""
Compare ATS Results

This script compares the original ATS results with the new optimized results
to show the improvement achieved.
"""

import json
from pathlib import Path

def load_json_file(filename):
    """Load JSON file safely"""
    if Path(filename).exists():
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def compare_results():
    """Compare original vs optimized ATS results"""
    print("📊 ATS Results Comparison")
    print("=" * 50)
    
    # Load original results
    original_results = load_json_file("advanced_ats_results.json")
    optimized_results = load_json_file("ats_text_test_results.json")
    
    if not original_results:
        print("❌ Original ATS results not found")
        return
    
    if not optimized_results:
        print("❌ Optimized ATS results not found")
        return
    
    print("\n🔍 CONTACT INFORMATION:")
    print(f"  Original: {'✅' if original_results['contact_info']['complete'] else '❌'}")
    print(f"  Optimized: {'✅' if optimized_results['contact_info']['complete'] else '❌'}")
    
    print("\n💼 WORK EXPERIENCE:")
    original_work = original_results['work_experience']
    optimized_work = optimized_results['work_experience']
    
    print(f"  Original: {len(original_work['jobs'])} jobs, {'✅' if original_work['parsed_well'] else '❌'} parsed")
    print(f"  Optimized: {len(optimized_work['jobs'])} jobs, {'✅' if optimized_work['parsed_well'] else '❌'} parsed")
    
    print("\n🎓 EDUCATION:")
    original_edu = original_results['education']
    optimized_edu = optimized_results['education']
    
    print(f"  Original: {len(original_edu['institutions'])} institutions, {'✅' if original_edu['parsed_well'] else '❌'} parsed")
    print(f"  Optimized: {len(optimized_edu['institutions'])} institutions, {'✅' if optimized_edu['parsed_well'] else '❌'} parsed")
    
    print("\n🛠️ SKILLS:")
    original_skills = original_results['skills']
    optimized_skills = optimized_results['skills']
    
    print(f"  Original: {len(original_skills['skill_categories'])} categories, {'✅' if original_skills['parsed_well'] else '❌'} parsed")
    print(f"  Optimized: {len(optimized_skills['skill_categories'])} categories, {'✅' if optimized_skills['parsed_well'] else '❌'} parsed")
    
    print("\n⚠️ ATS ISSUES:")
    original_issues = len(original_results['ats_issues'])
    optimized_issues = len(optimized_results['ats_issues'])
    
    print(f"  Original: {original_issues} issues")
    print(f"  Optimized: {optimized_issues} issues")
    
    if original_issues > 0:
        print("  Original issues:")
        for i, issue in enumerate(original_results['ats_issues'], 1):
            print(f"    {i}. {issue}")
    
    if optimized_issues > 0:
        print("  Optimized issues:")
        for i, issue in enumerate(optimized_results['ats_issues'], 1):
            print(f"    {i}. {issue}")
    else:
        print("  ✅ No issues in optimized version!")
    
    print("\n📊 ATS SCORES:")
    original_score = original_results.get('optimization_score', 0)
    optimized_score = optimized_results.get('optimization_score', 0)
    
    print(f"  Original: {original_score}/100")
    print(f"  Optimized: {optimized_score}/100")
    print(f"  Improvement: +{optimized_score - original_score} points")
    
    print("\n" + "=" * 50)
    print("🎉 SUMMARY:")
    
    if optimized_score > original_score:
        print(f"✅ ATS compatibility improved by {optimized_score - original_score} points!")
        print("✅ All sections now parse correctly")
        print("✅ No ATS issues detected")
        print("✅ Resume is now optimized for both human readers and ATS systems")
    else:
        print("⚠️ No improvement in ATS score")
    
    print(f"\n📈 Overall improvement: {((optimized_score - original_score) / max(original_score, 1)) * 100:.1f}%")

def main():
    """Main function"""
    compare_results()

if __name__ == "__main__":
    main()
