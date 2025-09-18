#!/usr/bin/env python3
"""
Advanced ATS Testing Script

This script simulates how different ATS systems parse resumes
and provides specific recommendations for optimization.
"""

import PyPDF2
import pdfplumber
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse

class AdvancedATSTester:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.parsed_sections = {}
        
    def extract_text(self):
        """Extract text using the best available method"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                self.text = full_text
                return True
        except Exception as e:
            print(f"Error extracting text: {e}")
            return False
    
    def simulate_ats_parsing(self) -> Dict[str, Any]:
        """Simulate how different ATS systems parse the resume"""
        results = {
            'contact_info': self._parse_contact_info(),
            'work_experience': self._parse_work_experience(),
            'education': self._parse_education(),
            'skills': self._parse_skills(),
            'ats_issues': self._identify_ats_issues(),
            'optimization_score': 0
        }
        
        # Calculate optimization score
        score = 0
        if results['contact_info']['complete']:
            score += 25
        if results['work_experience']['parsed_well']:
            score += 30
        if results['education']['parsed_well']:
            score += 20
        if results['skills']['parsed_well']:
            score += 15
        if len(results['ats_issues']) == 0:
            score += 10
        
        results['optimization_score'] = score
        return results
    
    def _parse_contact_info(self) -> Dict[str, Any]:
        """Parse contact information as ATS would"""
        contact = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'complete': False
        }
        
        # Extract name (usually first line or after "Name:")
        name_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',
            r'Name:\s*([A-Z][a-z]+ [A-Z][a-z]+)',
            r'^([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, self.text, re.MULTILINE)
            if match:
                contact['name'] = match.group(1)
                break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, self.text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Extract phone
        phone_patterns = [
            r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'(\+?1[-.\s]?)?([0-9]{3})[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, self.text)
            if phone_match:
                contact['phone'] = phone_match.group(0)
                break
        
        # Extract location
        location_patterns = [
            r'([A-Z][a-z]+,\s*[A-Z]{2})',
            r'([A-Z][a-z]+,\s*[A-Z][a-z]+)',
            r'Location:\s*([A-Z][a-z]+,\s*[A-Z]{2})'
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, self.text)
            if location_match:
                contact['location'] = location_match.group(1)
                break
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/([a-zA-Z0-9-]+)'
        linkedin_match = re.search(linkedin_pattern, self.text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(1)
        
        # Check if contact info is complete
        contact['complete'] = all([
            contact['name'], contact['email'], contact['phone'], contact['location']
        ])
        
        return contact
    
    def _parse_work_experience(self) -> Dict[str, Any]:
        """Parse work experience as ATS would"""
        experience = {
            'jobs': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Look for work experience section
        work_section = self._extract_section('work experience', 'education')
        if not work_section:
            experience['issues'].append("Work experience section not found")
            return experience
        
        # Parse individual jobs
        job_patterns = [
            r'([A-Z][^:]+)\s*:\s*([^|]+)\|\s*([^|]+)',
            r'([A-Z][^:]+)\s*:\s*([^|]+)\|\s*([^|]+)',
            r'([A-Z][^:]+)\s*:\s*([^|]+)\|\s*([^|]+)'
        ]
        
        lines = work_section.split('\n')
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this looks like a job title
            if re.match(r'^[A-Z][^:]+:', line):
                if current_job:
                    experience['jobs'].append(current_job)
                
                # Parse job title, company, dates
                parts = line.split('|')
                if len(parts) >= 2:
                    title_company = parts[0].split(':')
                    if len(title_company) >= 2:
                        current_job = {
                            'title': title_company[0].strip(),
                            'company': title_company[1].strip(),
                            'dates': parts[1].strip() if len(parts) > 1 else '',
                            'achievements': []
                        }
                    else:
                        current_job = {
                            'title': title_company[0].strip(),
                            'company': '',
                            'dates': parts[1].strip() if len(parts) > 1 else '',
                            'achievements': []
                        }
                else:
                    current_job = {
                        'title': line,
                        'company': '',
                        'dates': '',
                        'achievements': []
                    }
            
            # Check if this looks like an achievement
            elif current_job and (line.startswith('•') or line.startswith('*') or line.startswith('-') or line.startswith('·')):
                achievement = line.lstrip('•*-·').strip()
                if achievement:
                    current_job['achievements'].append(achievement)
        
        if current_job:
            experience['jobs'].append(current_job)
        
        # Check if parsing was successful
        experience['parsed_well'] = len(experience['jobs']) > 0 and all(
            job['title'] and job['company'] for job in experience['jobs']
        )
        
        if not experience['parsed_well']:
            experience['issues'].append("Work experience not parsed correctly")
        
        return experience
    
    def _parse_education(self) -> Dict[str, Any]:
        """Parse education as ATS would"""
        education = {
            'institutions': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Look for education section
        edu_section = self._extract_section('education', 'skills')
        if not edu_section:
            education['issues'].append("Education section not found")
            return education
        
        # Parse education entries
        lines = edu_section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree and institution patterns
            degree_patterns = [
                r'([A-Z][^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)',
                r'([A-Z][^|]+)\s*\|\s*([^|]+)',
                r'([A-Z][^|]+)'
            ]
            
            for pattern in degree_patterns:
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    institution = {
                        'degree': groups[0].strip(),
                        'institution': groups[1].strip() if len(groups) > 1 else '',
                        'dates': groups[2].strip() if len(groups) > 2 else ''
                    }
                    education['institutions'].append(institution)
                    break
        
        # Check if parsing was successful
        education['parsed_well'] = len(education['institutions']) > 0
        
        if not education['parsed_well']:
            education['issues'].append("Education not parsed correctly")
        
        return education
    
    def _parse_skills(self) -> Dict[str, Any]:
        """Parse skills as ATS would"""
        skills = {
            'skill_categories': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Look for skills section
        skills_section = self._extract_section('skills', '')
        if not skills_section:
            skills['issues'].append("Skills section not found")
            return skills
        
        # Parse skill categories
        lines = skills_section.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this looks like a skill category header
            if re.match(r'^[A-Z][^:]+:', line):
                if current_category:
                    skills['skill_categories'].append(current_category)
                
                category_name = line.rstrip(':')
                current_category = {
                    'name': category_name,
                    'skills': []
                }
            
            # Check if this looks like skills list
            elif current_category and ('•' in line or '·' in line or '|' in line):
                # Split by common separators
                skill_items = re.split(r'[•·|]', line)
                for item in skill_items:
                    item = item.strip()
                    if item:
                        current_category['skills'].append(item)
        
        if current_category:
            skills['skill_categories'].append(current_category)
        
        # Check if parsing was successful
        skills['parsed_well'] = len(skills['skill_categories']) > 0 and any(
            len(cat['skills']) > 0 for cat in skills['skill_categories']
        )
        
        if not skills['parsed_well']:
            skills['issues'].append("Skills not parsed correctly")
        
        return skills
    
    def _extract_section(self, start_keyword: str, end_keyword: str) -> str:
        """Extract a specific section from the resume text"""
        lines = self.text.split('\n')
        start_idx = -1
        end_idx = len(lines)
        
        # Find start of section
        for i, line in enumerate(lines):
            if start_keyword.lower() in line.lower():
                start_idx = i
                break
        
        if start_idx == -1:
            return ""
        
        # Find end of section
        if end_keyword:
            for i in range(start_idx + 1, len(lines)):
                if end_keyword.lower() in lines[i].lower():
                    end_idx = i
                    break
        
        # Extract section
        section_lines = lines[start_idx:end_idx]
        return '\n'.join(section_lines)
    
    def _identify_ats_issues(self) -> List[str]:
        """Identify specific ATS parsing issues"""
        issues = []
        
        # Check for problematic characters
        if '&' in self.text:
            issues.append("Ampersands (&) should be written as 'and' for better ATS compatibility")
        
        if '•' in self.text or '◦' in self.text:
            issues.append("Special bullet points may not parse well in some ATS systems")
        
        if re.search(r'[^\x00-\x7F]', self.text):
            issues.append("Non-ASCII characters may cause ATS parsing issues")
        
        # Check for formatting issues
        if self.text.count('\n') > 100:
            issues.append("Too many line breaks may confuse ATS parsing")
        
        # Check for missing contact info
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text):
            issues.append("Email address not found - critical for ATS")
        
        if not re.search(r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', self.text):
            issues.append("Phone number not found - important for ATS")
        
        # Check for consistent formatting
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        if len(set(len(line) for line in lines)) > 10:
            issues.append("Inconsistent line lengths may confuse ATS parsing")
        
        return issues
    
    def generate_ats_optimized_version(self) -> str:
        """Generate an ATS-optimized version of the resume"""
        optimized_text = self.text
        
        # Replace ampersands
        optimized_text = optimized_text.replace('&', 'and')
        
        # Replace special bullet points
        optimized_text = optimized_text.replace('•', '*')
        optimized_text = optimized_text.replace('◦', '*')
        optimized_text = optimized_text.replace('·', '*')
        
        # Remove non-ASCII characters
        optimized_text = ''.join(char if ord(char) < 128 else ' ' for char in optimized_text)
        
        # Normalize whitespace
        optimized_text = re.sub(r'\s+', ' ', optimized_text)
        optimized_text = re.sub(r'\n\s*\n', '\n\n', optimized_text)
        
        return optimized_text
    
    def run_advanced_test(self) -> Dict[str, Any]:
        """Run the advanced ATS test"""
        if not self.extract_text():
            return {'error': 'Failed to extract text from PDF'}
        
        results = self.simulate_ats_parsing()
        results['optimized_text'] = self.generate_ats_optimized_version()
        
        return results
    
    def print_advanced_results(self, results: Dict[str, Any]):
        """Print advanced test results"""
        print("\n" + "=" * 60)
        print("ADVANCED ATS COMPATIBILITY TEST RESULTS")
        print("=" * 60)
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        # Contact Information
        print("\n📞 CONTACT INFORMATION:")
        contact = results['contact_info']
        print(f"  Name: {'✅' if contact['name'] else '❌'} {contact['name'] or 'Not found'}")
        print(f"  Email: {'✅' if contact['email'] else '❌'} {contact['email'] or 'Not found'}")
        print(f"  Phone: {'✅' if contact['phone'] else '❌'} {contact['phone'] or 'Not found'}")
        print(f"  Location: {'✅' if contact['location'] else '❌'} {contact['location'] or 'Not found'}")
        print(f"  LinkedIn: {'✅' if contact['linkedin'] else '❌'} {contact['linkedin'] or 'Not found'}")
        print(f"  Complete: {'✅' if contact['complete'] else '❌'}")
        
        # Work Experience
        print("\n💼 WORK EXPERIENCE:")
        work = results['work_experience']
        print(f"  Jobs Found: {len(work['jobs'])}")
        print(f"  Parsed Well: {'✅' if work['parsed_well'] else '❌'}")
        
        for i, job in enumerate(work['jobs'][:3], 1):  # Show first 3 jobs
            print(f"    {i}. {job['title']} at {job['company']}")
            print(f"       Dates: {job['dates']}")
            print(f"       Achievements: {len(job['achievements'])}")
        
        if work['issues']:
            print("  Issues:")
            for issue in work['issues']:
                print(f"    ⚠️  {issue}")
        
        # Education
        print("\n🎓 EDUCATION:")
        education = results['education']
        print(f"  Institutions Found: {len(education['institutions'])}")
        print(f"  Parsed Well: {'✅' if education['parsed_well'] else '❌'}")
        
        for inst in education['institutions']:
            print(f"    • {inst['degree']} from {inst['institution']}")
        
        if education['issues']:
            print("  Issues:")
            for issue in education['issues']:
                print(f"    ⚠️  {issue}")
        
        # Skills
        print("\n🛠️ SKILLS:")
        skills = results['skills']
        print(f"  Categories Found: {len(skills['skill_categories'])}")
        print(f"  Parsed Well: {'✅' if skills['parsed_well'] else '❌'}")
        
        for category in skills['skill_categories']:
            print(f"    • {category['name']}: {len(category['skills'])} skills")
        
        if skills['issues']:
            print("  Issues:")
            for issue in skills['issues']:
                print(f"    ⚠️  {issue}")
        
        # ATS Issues
        print("\n⚠️ ATS ISSUES:")
        issues = results['ats_issues']
        if issues:
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("  ✅ No ATS issues detected!")
        
        # Optimization Score
        print(f"\n📊 ATS OPTIMIZATION SCORE: {results['optimization_score']}/100")
        if results['optimization_score'] >= 80:
            print("  ✅ Excellent ATS compatibility!")
        elif results['optimization_score'] >= 60:
            print("  ⚠️ Good ATS compatibility, some improvements needed")
        else:
            print("  ❌ Poor ATS compatibility, significant improvements needed")

def main():
    parser = argparse.ArgumentParser(description='Advanced ATS testing for PDF resumes')
    parser.add_argument('pdf_path', help='Path to the PDF resume file')
    parser.add_argument('--output', '-o', help='Output file for JSON results')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"Error: File {args.pdf_path} not found")
        return
    
    tester = AdvancedATSTester(args.pdf_path)
    results = tester.run_advanced_test()
    tester.print_advanced_results(results)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: {args.output}")

if __name__ == "__main__":
    main()
