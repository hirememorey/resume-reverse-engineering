#!/usr/bin/env python3
"""
Test ATS Text File

This script tests the generated ATS text file using the same logic
as the existing ATS test scripts but without PDF extraction.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any

class ATSTextTester:
    def __init__(self, text_file: str):
        self.text_file = text_file
        self.text = ""
        self.results = {
            'contact_info': {},
            'work_experience': {},
            'education': {},
            'skills': {},
            'ats_issues': [],
            'optimization_score': 0
        }
    
    def load_text(self):
        """Load text from file"""
        with open(self.text_file, 'r', encoding='utf-8') as f:
            self.text = f.read()
    
    def test_contact_info(self) -> Dict[str, Any]:
        """Test contact information parsing"""
        contact = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'complete': False
        }
        
        # Extract name (first line)
        lines = self.text.split('\n')
        if lines:
            contact['name'] = lines[0].strip()
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, self.text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Extract phone
        phone_pattern = r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        phone_match = re.search(phone_pattern, self.text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # Extract location
        location_pattern = r'([A-Z][a-z]+,\s*[A-Z]{2})'
        location_match = re.search(location_pattern, self.text)
        if location_match:
            contact['location'] = location_match.group(1)
        
        # Extract LinkedIn
        linkedin_pattern = r'LinkedIn:\s*([a-zA-Z0-9-]+)'
        linkedin_match = re.search(linkedin_pattern, self.text)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(1)
        
        # Check if complete
        contact['complete'] = all([
            contact['name'], contact['email'], contact['phone'], contact['location']
        ])
        
        self.results['contact_info'] = contact
        return contact
    
    def test_work_experience(self) -> Dict[str, Any]:
        """Test work experience parsing"""
        experience = {
            'jobs': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Find work experience section
        work_section = self._extract_section('WORK EXPERIENCE', 'EDUCATION')
        if not work_section:
            experience['issues'].append("Work experience section not found")
            return experience
        
        # Parse jobs using the ATS-friendly format
        lines = work_section.split('\n')
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a job entry (format: Job Title: Company | Dates)
            if ':' in line and '|' in line and not line.startswith('*'):
                if current_job:
                    experience['jobs'].append(current_job)
                
                # Parse job title, company, dates
                parts = line.split(':')
                if len(parts) >= 2:
                    job_title = parts[0].strip()
                    company_dates = parts[1].strip()
                    
                    if '|' in company_dates:
                        company, dates = company_dates.split('|', 1)
                        current_job = {
                            'title': job_title,
                            'company': company.strip(),
                            'dates': dates.strip(),
                            'achievements': []
                        }
                    else:
                        current_job = {
                            'title': job_title,
                            'company': company_dates.strip(),
                            'dates': '',
                            'achievements': []
                        }
            
            # Check if this is an achievement (starts with *)
            elif line.startswith('*') and current_job:
                achievement = line[1:].strip()  # Remove "*" prefix
                if achievement:
                    current_job['achievements'].append(achievement)
        
        # Add the last job
        if current_job:
            experience['jobs'].append(current_job)
        
        # Check if parsing was successful
        experience['parsed_well'] = len(experience['jobs']) > 0 and all(
            job['title'] and job['company'] for job in experience['jobs']
        )
        
        if not experience['parsed_well']:
            experience['issues'].append("Work experience not parsed correctly")
        
        self.results['work_experience'] = experience
        return experience
    
    def test_education(self) -> Dict[str, Any]:
        """Test education parsing"""
        education = {
            'institutions': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Find education section
        edu_section = self._extract_section('EDUCATION', 'SKILLS')
        if not edu_section:
            education['issues'].append("Education section not found")
            return education
        
        # Parse education entries
        lines = edu_section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for education pattern: Degree: Institution | Dates
            if ':' in line and '|' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    degree = parts[0].strip()
                    institution_dates = parts[1].strip()
                    
                    if '|' in institution_dates:
                        institution, dates = institution_dates.split('|', 1)
                        education['institutions'].append({
                            'degree': degree,
                            'institution': institution.strip(),
                            'dates': dates.strip()
                        })
                    else:
                        education['institutions'].append({
                            'degree': degree,
                            'institution': institution_dates.strip(),
                            'dates': ''
                        })
        
        # Check if parsing was successful
        education['parsed_well'] = len(education['institutions']) > 0
        
        if not education['parsed_well']:
            education['issues'].append("Education not parsed correctly")
        
        self.results['education'] = education
        return education
    
    def test_skills(self) -> Dict[str, Any]:
        """Test skills parsing"""
        skills = {
            'skill_categories': [],
            'parsed_well': False,
            'issues': []
        }
        
        # Find skills section
        skills_section = self._extract_section('SKILLS', '')
        if not skills_section:
            skills['issues'].append("Skills section not found")
            return skills
        
        # Parse skill categories
        lines = skills_section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for skill category pattern: Category: skill1, skill2, skill3
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    category_name = parts[0].strip()
                    skills_text = parts[1].strip()
                    
                    # Split skills by comma
                    skill_items = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
                    
                    skills['skill_categories'].append({
                        'name': category_name,
                        'skills': skill_items
                    })
        
        # Check if parsing was successful
        skills['parsed_well'] = len(skills['skill_categories']) > 0 and any(
            len(cat['skills']) > 0 for cat in skills['skill_categories']
        )
        
        if not skills['parsed_well']:
            skills['issues'].append("Skills not parsed correctly")
        
        self.results['skills'] = skills
        return skills
    
    def _extract_section(self, start_keyword: str, end_keyword: str) -> str:
        """Extract a specific section from the text"""
        lines = self.text.split('\n')
        start_idx = -1
        end_idx = len(lines)
        
        # Find start of section
        for i, line in enumerate(lines):
            if start_keyword.upper() in line.upper():
                start_idx = i
                break
        
        if start_idx == -1:
            return ""
        
        # Find end of section
        if end_keyword:
            for i in range(start_idx + 1, len(lines)):
                if end_keyword.upper() in lines[i].upper():
                    end_idx = i
                    break
        
        # Extract section
        section_lines = lines[start_idx:end_idx]
        return '\n'.join(section_lines)
    
    def identify_ats_issues(self) -> List[str]:
        """Identify ATS parsing issues"""
        issues = []
        
        # Check for problematic characters
        if '&' in self.text:
            issues.append("Ampersands (&) should be written as 'and' for better ATS compatibility")
        
        if '•' in self.text or '◦' in self.text:
            issues.append("Special bullet points may not parse well in some ATS systems")
        
        if re.search(r'[^\x00-\x7F]', self.text):
            issues.append("Non-ASCII characters may cause ATS parsing issues")
        
        # Check for missing contact info
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text):
            issues.append("Email address not found - critical for ATS")
        
        if not re.search(r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', self.text):
            issues.append("Phone number not found - important for ATS")
        
        return issues
    
    def calculate_optimization_score(self) -> int:
        """Calculate ATS optimization score"""
        score = 0
        
        # Contact info (25 points)
        if self.results['contact_info']['complete']:
            score += 25
        
        # Work experience (30 points)
        if self.results['work_experience']['parsed_well']:
            score += 30
        
        # Education (20 points)
        if self.results['education']['parsed_well']:
            score += 20
        
        # Skills (15 points)
        if self.results['skills']['parsed_well']:
            score += 15
        
        # No ATS issues (10 points)
        if len(self.results['ats_issues']) == 0:
            score += 10
        
        return score
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all ATS tests"""
        print("Testing ATS text file...")
        print("=" * 50)
        
        # Load text
        self.load_text()
        
        # Run tests
        self.test_contact_info()
        self.test_work_experience()
        self.test_education()
        self.test_skills()
        
        # Identify issues
        self.results['ats_issues'] = self.identify_ats_issues()
        
        # Calculate score
        self.results['optimization_score'] = self.calculate_optimization_score()
        
        return self.results
    
    def print_results(self):
        """Print test results"""
        print("\n" + "=" * 60)
        print("ATS TEXT TEST RESULTS")
        print("=" * 60)
        
        # Contact Information
        print("\n📞 CONTACT INFORMATION:")
        contact = self.results['contact_info']
        print(f"  Name: {'✅' if contact['name'] else '❌'} {contact['name'] or 'Not found'}")
        print(f"  Email: {'✅' if contact['email'] else '❌'} {contact['email'] or 'Not found'}")
        print(f"  Phone: {'✅' if contact['phone'] else '❌'} {contact['phone'] or 'Not found'}")
        print(f"  Location: {'✅' if contact['location'] else '❌'} {contact['location'] or 'Not found'}")
        print(f"  LinkedIn: {'✅' if contact['linkedin'] else '❌'} {contact['linkedin'] or 'Not found'}")
        print(f"  Complete: {'✅' if contact['complete'] else '❌'}")
        
        # Work Experience
        print("\n💼 WORK EXPERIENCE:")
        work = self.results['work_experience']
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
        education = self.results['education']
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
        skills = self.results['skills']
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
        issues = self.results['ats_issues']
        if issues:
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("  ✅ No ATS issues detected!")
        
        # Optimization Score
        print(f"\n📊 ATS OPTIMIZATION SCORE: {self.results['optimization_score']}/100")
        if self.results['optimization_score'] >= 80:
            print("  ✅ Excellent ATS compatibility!")
        elif self.results['optimization_score'] >= 60:
            print("  ⚠️ Good ATS compatibility, some improvements needed")
        else:
            print("  ❌ Poor ATS compatibility, significant improvements needed")

def main():
    """Main function to test ATS text file"""
    text_file = "ats_data.txt"
    
    if not Path(text_file).exists():
        print(f"Error: {text_file} not found")
        print("Run simple_ats_converter.py first to generate the ATS text file")
        return
    
    tester = ATSTextTester(text_file)
    results = tester.run_all_tests()
    tester.print_results()
    
    # Save results
    with open('ats_text_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: ats_text_test_results.json")

if __name__ == "__main__":
    main()
