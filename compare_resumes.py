#!/usr/bin/env python3
"""
Compare Original and ATS-Optimized Resumes

This script compares the original resume with the ATS-optimized version
to show the differences and improvements.
"""

import PyPDF2
import pdfplumber
import re
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
            return full_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def analyze_text(text, name):
    """Analyze text for ATS compatibility metrics"""
    print(f"\n{'='*60}")
    print(f"ANALYSIS: {name}")
    print(f"{'='*60}")
    
    # Basic metrics
    print(f"Text Length: {len(text)} characters")
    print(f"Word Count: {len(text.split())} words")
    print(f"Line Count: {len(text.split('\\n'))} lines")
    
    # Character analysis
    special_chars = len(re.findall(r'[^\w\s@.-]', text))
    print(f"Special Characters: {special_chars}")
    
    # ATS-specific checks
    has_ampersands = '&' in text
    has_special_bullets = any(char in text for char in ['•', '◦', '·'])
    has_non_ascii = bool(re.search(r'[^\x00-\x7F]', text))
    
    print(f"\\nATS Compatibility Checks:")
    print(f"  Ampersands (&): {'❌ Found' if has_ampersands else '✅ None'}")
    print(f"  Special Bullets: {'❌ Found' if has_special_bullets else '✅ None'}")
    print(f"  Non-ASCII Chars: {'❌ Found' if has_non_ascii else '✅ None'}")
    
    # Contact information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
    
    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))
    
    print(f"\\nContact Information:")
    print(f"  Email: {'✅ Found' if has_email else '❌ Missing'}")
    print(f"  Phone: {'✅ Found' if has_phone else '❌ Missing'}")
    
    # Section analysis
    sections = ['work experience', 'education', 'skills']
    found_sections = []
    
    for section in sections:
        if section.lower() in text.lower():
            found_sections.append(section)
    
    print(f"\\nSections Found: {', '.join(found_sections) if found_sections else 'None'}")
    
    # Calculate ATS score
    score = 0
    if has_email: score += 25
    if has_phone: score += 25
    if len(found_sections) >= 3: score += 25
    if not has_ampersands: score += 10
    if not has_special_bullets: score += 10
    if not has_non_ascii: score += 5
    
    print(f"\\nATS Score: {score}/100")
    
    return {
        'text_length': len(text),
        'word_count': len(text.split()),
        'special_chars': special_chars,
        'has_ampersands': has_ampersands,
        'has_special_bullets': has_special_bullets,
        'has_non_ascii': has_non_ascii,
        'has_email': has_email,
        'has_phone': has_phone,
        'sections_found': len(found_sections),
        'ats_score': score
    }

def compare_resumes(original_path, optimized_path):
    """Compare original and optimized resumes"""
    print("RESUME COMPARISON ANALYSIS")
    print("="*60)
    
    # Extract text from both PDFs
    original_text = extract_text_from_pdf(original_path)
    optimized_text = extract_text_from_pdf(optimized_path)
    
    if not original_text:
        print(f"Error: Could not extract text from {original_path}")
        return
    
    if not optimized_text:
        print(f"Error: Could not extract text from {optimized_path}")
        return
    
    # Analyze both versions
    original_analysis = analyze_text(original_text, "ORIGINAL RESUME")
    optimized_analysis = analyze_text(optimized_text, "ATS-OPTIMIZED RESUME")
    
    # Compare results
    print(f"\\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    
    print(f"\\nText Length:")
    print(f"  Original: {original_analysis['text_length']} characters")
    print(f"  Optimized: {optimized_analysis['text_length']} characters")
    print(f"  Difference: {optimized_analysis['text_length'] - original_analysis['text_length']:+d}")
    
    print(f"\\nATS Score:")
    print(f"  Original: {original_analysis['ats_score']}/100")
    print(f"  Optimized: {optimized_analysis['ats_score']}/100")
    print(f"  Improvement: {optimized_analysis['ats_score'] - original_analysis['ats_score']:+d} points")
    
    print(f"\\nSpecial Characters:")
    print(f"  Original: {original_analysis['special_chars']}")
    print(f"  Optimized: {optimized_analysis['special_chars']}")
    print(f"  Reduction: {original_analysis['special_chars'] - optimized_analysis['special_chars']:+d}")
    
    print(f"\\nAmpersands:")
    print(f"  Original: {'❌ Found' if original_analysis['has_ampersands'] else '✅ None'}")
    print(f"  Optimized: {'❌ Found' if optimized_analysis['has_ampersands'] else '✅ None'}")
    
    print(f"\\nSpecial Bullets:")
    print(f"  Original: {'❌ Found' if original_analysis['has_special_bullets'] else '✅ None'}")
    print(f"  Optimized: {'❌ Found' if optimized_analysis['has_special_bullets'] else '✅ None'}")
    
    print(f"\\nNon-ASCII Characters:")
    print(f"  Original: {'❌ Found' if original_analysis['has_non_ascii'] else '✅ None'}")
    print(f"  Optimized: {'❌ Found' if optimized_analysis['has_non_ascii'] else '✅ None'}")
    
    # Overall assessment
    print(f"\\n{'='*60}")
    print("OVERALL ASSESSMENT")
    print(f"{'='*60}")
    
    if optimized_analysis['ats_score'] > original_analysis['ats_score']:
        print("✅ ATS optimization was successful!")
        print(f"   Score improved by {optimized_analysis['ats_score'] - original_analysis['ats_score']} points")
    elif optimized_analysis['ats_score'] == original_analysis['ats_score']:
        print("⚠️  ATS optimization had no effect on score")
    else:
        print("❌ ATS optimization made the resume worse")
        print(f"   Score decreased by {original_analysis['ats_score'] - optimized_analysis['ats_score']} points")
    
    # Recommendations
    print(f"\\nRECOMMENDATIONS:")
    
    if optimized_analysis['ats_score'] < 70:
        print("• Consider further optimization for better ATS compatibility")
        print("• Focus on work experience formatting")
        print("• Ensure consistent section headers")
        print("• Add more industry-specific keywords")
    
    if optimized_analysis['has_ampersands']:
        print("• Replace remaining ampersands with 'and'")
    
    if optimized_analysis['has_special_bullets']:
        print("• Replace special bullet points with standard asterisks")
    
    if optimized_analysis['has_non_ascii']:
        print("• Remove or replace non-ASCII characters")
    
    if optimized_analysis['sections_found'] < 3:
        print("• Ensure all required sections are present and clearly marked")
    
    print(f"\\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")

def main():
    original_path = "harris_resume.pdf"
    optimized_path = "harris_resume_ats_optimized.pdf"
    
    if not Path(original_path).exists():
        print(f"Error: {original_path} not found")
        return
    
    if not Path(optimized_path).exists():
        print(f"Error: {optimized_path} not found")
        return
    
    compare_resumes(original_path, optimized_path)

if __name__ == "__main__":
    main()
