#!/usr/bin/env python3
"""
ATS (Applicant Tracking System) Testing Script for Resume PDFs

This script tests PDF resumes for ATS compatibility and human readability
by analyzing text extraction, structure, and formatting.
"""

import PyPDF2
import pdfplumber
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse
import sys

class ATSResumeTester:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.results = {
            'file_info': {},
            'text_extraction': {},
            'ats_compatibility': {},
            'human_readability': {},
            'recommendations': []
        }
    
    def test_basic_file_info(self) -> Dict[str, Any]:
        """Test basic PDF file information"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'pages': len(pdf_reader.pages),
                    'encrypted': pdf_reader.is_encrypted,
                    'metadata': pdf_reader.metadata,
                    'file_size_mb': Path(self.pdf_path).stat().st_size / (1024 * 1024)
                }
                
                self.results['file_info'] = info
                return info
        except Exception as e:
            return {'error': str(e)}
    
    def test_text_extraction(self) -> Dict[str, Any]:
        """Test text extraction quality using multiple methods"""
        results = {
            'pdfplumber_text': '',
            'pyPDF2_text': '',
            'extraction_quality': {},
            'text_structure': {}
        }
        
        try:
            # Method 1: pdfplumber (better for complex layouts)
            with pdfplumber.open(self.pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                results['pdfplumber_text'] = full_text
            
            # Method 2: PyPDF2 (standard method)
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                full_text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                results['pyPDF2_text'] = full_text
            
            # Analyze extraction quality
            results['extraction_quality'] = self._analyze_extraction_quality(results)
            results['text_structure'] = self._analyze_text_structure(results['pdfplumber_text'])
            
            self.results['text_extraction'] = results
            return results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_extraction_quality(self, results: Dict) -> Dict[str, Any]:
        """Analyze the quality of text extraction"""
        pdfplumber_text = results['pdfplumber_text']
        pyPDF2_text = results['pyPDF2_text']
        
        return {
            'pdfplumber_length': len(pdfplumber_text),
            'pyPDF2_length': len(pyPDF2_text),
            'text_difference': abs(len(pdfplumber_text) - len(pyPDF2_text)),
            'extraction_consistency': len(pdfplumber_text) > 0 and len(pyPDF2_text) > 0,
            'has_meaningful_content': len(pdfplumber_text.strip()) > 100
        }
    
    def _analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """Analyze the structure of extracted text"""
        lines = text.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'average_line_length': sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1),
            'has_contact_info': self._detect_contact_info(text),
            'has_work_experience': self._detect_work_experience(text),
            'has_education': self._detect_education(text),
            'has_skills': self._detect_skills(text)
        }
    
    def _detect_contact_info(self, text: str) -> bool:
        """Detect if contact information is present"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        return bool(re.search(email_pattern, text) or re.search(phone_pattern, text))
    
    def _detect_work_experience(self, text: str) -> bool:
        """Detect if work experience section is present"""
        work_keywords = ['experience', 'employment', 'work history', 'professional', 'career']
        return any(keyword in text.lower() for keyword in work_keywords)
    
    def _detect_education(self, text: str) -> bool:
        """Detect if education section is present"""
        edu_keywords = ['education', 'university', 'college', 'degree', 'bachelor', 'master', 'phd']
        return any(keyword in text.lower() for keyword in edu_keywords)
    
    def _detect_skills(self, text: str) -> bool:
        """Detect if skills section is present"""
        skills_keywords = ['skills', 'technical', 'proficiencies', 'competencies']
        return any(keyword in text.lower() for keyword in skills_keywords)
    
    def test_ats_compatibility(self) -> Dict[str, Any]:
        """Test ATS compatibility metrics"""
        text = self.results['text_extraction'].get('pdfplumber_text', '')
        
        if not text:
            return {'error': 'No text extracted for ATS analysis'}
        
        results = {
            'text_readability': self._test_text_readability(text),
            'keyword_density': self._analyze_keyword_density(text),
            'formatting_issues': self._detect_formatting_issues(text),
            'ats_friendly_score': 0
        }
        
        # Calculate ATS-friendly score (0-100)
        score = 0
        
        # Text extraction quality (30 points)
        if self.results['text_extraction']['extraction_quality']['has_meaningful_content']:
            score += 30
        
        # Contact info present (20 points)
        if self.results['text_extraction']['text_structure']['has_contact_info']:
            score += 20
        
        # Work experience present (20 points)
        if self.results['text_extraction']['text_structure']['has_work_experience']:
            score += 20
        
        # Education present (15 points)
        if self.results['text_extraction']['text_structure']['has_education']:
            score += 15
        
        # Skills present (15 points)
        if self.results['text_extraction']['text_structure']['has_skills']:
            score += 15
        
        results['ats_friendly_score'] = score
        self.results['ats_compatibility'] = results
        return results
    
    def _test_text_readability(self, text: str) -> Dict[str, Any]:
        """Test text readability for ATS parsing"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return {
            'total_words': len(text.split()),
            'average_words_per_line': sum(len(line.split()) for line in lines) / max(len(lines), 1),
            'has_consistent_formatting': self._check_consistent_formatting(lines),
            'special_characters': self._count_special_characters(text),
            'unicode_issues': self._check_unicode_issues(text)
        }
    
    def _check_consistent_formatting(self, lines: List[str]) -> bool:
        """Check if formatting is consistent"""
        # Look for consistent patterns in job titles, dates, etc.
        date_pattern = r'\d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}'
        date_lines = [line for line in lines if re.search(date_pattern, line)]
        
        # Check if dates are consistently formatted
        return len(date_lines) > 0
    
    def _count_special_characters(self, text: str) -> int:
        """Count special characters that might cause ATS issues"""
        special_chars = r'[^\w\s@.-]'
        return len(re.findall(special_chars, text))
    
    def _check_unicode_issues(self, text: str) -> bool:
        """Check for Unicode issues that might cause ATS problems"""
        try:
            text.encode('ascii')
            return False
        except UnicodeEncodeError:
            return True
    
    def _analyze_keyword_density(self, text: str) -> Dict[str, Any]:
        """Analyze keyword density for ATS optimization"""
        # Common resume keywords
        keywords = [
            'management', 'leadership', 'strategy', 'analysis', 'development',
            'project', 'team', 'client', 'business', 'technical', 'software',
            'data', 'marketing', 'sales', 'operations', 'finance', 'design'
        ]
        
        text_lower = text.lower()
        keyword_counts = {keyword: text_lower.count(keyword) for keyword in keywords}
        total_words = len(text.split())
        
        return {
            'keyword_counts': keyword_counts,
            'total_keywords': sum(keyword_counts.values()),
            'keyword_density': sum(keyword_counts.values()) / max(total_words, 1) * 100
        }
    
    def _detect_formatting_issues(self, text: str) -> List[str]:
        """Detect potential formatting issues for ATS"""
        issues = []
        
        # Check for common ATS problems
        if '•' in text or '◦' in text:
            issues.append("Bullet points may not parse well in some ATS systems")
        
        if '&' in text:
            issues.append("Ampersands should be written as 'and' for better ATS compatibility")
        
        if re.search(r'[^\x00-\x7F]', text):
            issues.append("Non-ASCII characters may cause ATS parsing issues")
        
        if text.count('\n') > 100:
            issues.append("Too many line breaks may confuse ATS parsing")
        
        return issues
    
    def test_human_readability(self) -> Dict[str, Any]:
        """Test human readability aspects"""
        text = self.results['text_extraction'].get('pdfplumber_text', '')
        
        if not text:
            return {'error': 'No text extracted for readability analysis'}
        
        results = {
            'visual_structure': self._analyze_visual_structure(text),
            'content_organization': self._analyze_content_organization(text),
            'professional_presentation': self._analyze_professional_presentation(text)
        }
        
        self.results['human_readability'] = results
        return results
    
    def _analyze_visual_structure(self, text: str) -> Dict[str, Any]:
        """Analyze visual structure for human readability"""
        lines = text.split('\n')
        
        return {
            'section_breaks': text.count('---') + text.count('***'),
            'bullet_points': text.count('•') + text.count('*'),
            'bold_sections': len(re.findall(r'\*\*.*?\*\*', text)),
            'consistent_spacing': self._check_consistent_spacing(lines)
        }
    
    def _check_consistent_spacing(self, lines: List[str]) -> bool:
        """Check if spacing is consistent"""
        non_empty_lines = [line for line in lines if line.strip()]
        if len(non_empty_lines) < 2:
            return True
        
        # Check for consistent indentation patterns
        indentations = [len(line) - len(line.lstrip()) for line in non_empty_lines if line.strip()]
        return len(set(indentations)) <= 3  # Allow for 3 different indentation levels
    
    def _analyze_content_organization(self, text: str) -> Dict[str, Any]:
        """Analyze content organization"""
        sections = text.split('\n\n')
        
        return {
            'total_sections': len(sections),
            'section_lengths': [len(section) for section in sections],
            'has_clear_headings': bool(re.search(r'^[A-Z][A-Z\s]+$', text, re.MULTILINE)),
            'chronological_order': self._check_chronological_order(text)
        }
    
    def _check_chronological_order(self, text: str) -> bool:
        """Check if work experience is in chronological order"""
        # Look for date patterns and check if they're in reverse chronological order
        date_pattern = r'(\d{4})'
        dates = re.findall(date_pattern, text)
        
        if len(dates) < 2:
            return True
        
        # Convert to integers and check if they're in descending order
        years = [int(date) for date in dates if date.isdigit()]
        return years == sorted(years, reverse=True)
    
    def _analyze_professional_presentation(self, text: str) -> Dict[str, Any]:
        """Analyze professional presentation"""
        return {
            'has_contact_info': self._detect_contact_info(text),
            'has_quantified_achievements': bool(re.search(r'\$[\d,]+|\d+%|\d+x|\d+\+', text)),
            'action_verbs': len(re.findall(r'\b(led|managed|developed|created|built|launched|increased|improved|saved|unlocked)\b', text.lower())),
            'professional_tone': self._check_professional_tone(text)
        }
    
    def _check_professional_tone(self, text: str) -> bool:
        """Check if the tone is professional"""
        unprofessional_words = ['awesome', 'cool', 'amazing', 'fantastic', 'incredible']
        text_lower = text.lower()
        return not any(word in text_lower for word in unprofessional_words)
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # ATS compatibility recommendations
        ats_score = self.results['ats_compatibility'].get('ats_friendly_score', 0)
        if ats_score < 70:
            recommendations.append("Consider improving ATS compatibility - current score is below 70")
        
        formatting_issues = self.results['ats_compatibility'].get('formatting_issues', [])
        for issue in formatting_issues:
            recommendations.append(f"ATS Issue: {issue}")
        
        # Human readability recommendations
        visual_structure = self.results['human_readability'].get('visual_structure', {})
        if visual_structure.get('bullet_points', 0) < 5:
            recommendations.append("Consider adding more bullet points for better readability")
        
        if visual_structure.get('section_breaks', 0) < 3:
            recommendations.append("Consider adding more section breaks for better organization")
        
        # Content recommendations
        text_structure = self.results['text_extraction'].get('text_structure', {})
        if not text_structure.get('has_quantified_achievements', False):
            recommendations.append("Add more quantified achievements (numbers, percentages, dollar amounts)")
        
        self.results['recommendations'] = recommendations
        return recommendations
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("Running ATS and Human Readability Tests...")
        print("=" * 50)
        
        # Run all test categories
        self.test_basic_file_info()
        self.test_text_extraction()
        self.test_ats_compatibility()
        self.test_human_readability()
        self.generate_recommendations()
        
        return self.results
    
    def print_results(self):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("RESUME ATS & READABILITY TEST RESULTS")
        print("=" * 60)
        
        # File Information
        print("\n📄 FILE INFORMATION:")
        file_info = self.results['file_info']
        print(f"  Pages: {file_info.get('pages', 'N/A')}")
        print(f"  File Size: {file_info.get('file_size_mb', 0):.2f} MB")
        print(f"  Encrypted: {file_info.get('encrypted', 'N/A')}")
        
        # Text Extraction
        print("\n📝 TEXT EXTRACTION:")
        extraction = self.results['text_extraction']
        if 'error' not in extraction:
            quality = extraction['extraction_quality']
            structure = extraction['text_structure']
            print(f"  Text Length: {quality.get('pdfplumber_length', 0)} characters")
            print(f"  Extraction Quality: {'✅ Good' if quality.get('has_meaningful_content') else '❌ Poor'}")
            print(f"  Contact Info: {'✅ Present' if structure.get('has_contact_info') else '❌ Missing'}")
            print(f"  Work Experience: {'✅ Present' if structure.get('has_work_experience') else '❌ Missing'}")
            print(f"  Education: {'✅ Present' if structure.get('has_education') else '❌ Missing'}")
            print(f"  Skills: {'✅ Present' if structure.get('has_skills') else '❌ Missing'}")
        
        # ATS Compatibility
        print("\n🤖 ATS COMPATIBILITY:")
        ats = self.results['ats_compatibility']
        if 'error' not in ats:
            score = ats.get('ats_friendly_score', 0)
            print(f"  ATS Score: {score}/100 {'✅' if score >= 70 else '❌'}")
            
            readability = ats.get('text_readability', {})
            print(f"  Total Words: {readability.get('total_words', 0)}")
            print(f"  Special Characters: {readability.get('special_characters', 0)}")
            
            issues = ats.get('formatting_issues', [])
            if issues:
                print("  Issues Found:")
                for issue in issues:
                    print(f"    ⚠️  {issue}")
            else:
                print("  ✅ No formatting issues detected")
        
        # Human Readability
        print("\n👁️ HUMAN READABILITY:")
        human = self.results['human_readability']
        if 'error' not in human:
            visual = human.get('visual_structure', {})
            content = human.get('content_organization', {})
            professional = human.get('professional_presentation', {})
            
            print(f"  Section Breaks: {visual.get('section_breaks', 0)}")
            print(f"  Bullet Points: {visual.get('bullet_points', 0)}")
            print(f"  Bold Sections: {visual.get('bold_sections', 0)}")
            print(f"  Quantified Achievements: {'✅ Present' if professional.get('has_quantified_achievements') else '❌ Missing'}")
            print(f"  Action Verbs: {professional.get('action_verbs', 0)}")
            print(f"  Professional Tone: {'✅ Good' if professional.get('professional_tone') else '❌ Needs Improvement'}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        recommendations = self.results.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ No specific recommendations - resume looks good!")

def main():
    parser = argparse.ArgumentParser(description='Test PDF resume for ATS compatibility and human readability')
    parser.add_argument('pdf_path', help='Path to the PDF resume file')
    parser.add_argument('--output', '-o', help='Output file for JSON results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"Error: File {args.pdf_path} not found")
        sys.exit(1)
    
    tester = ATSResumeTester(args.pdf_path)
    results = tester.run_all_tests()
    tester.print_results()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: {args.output}")

if __name__ == "__main__":
    main()
