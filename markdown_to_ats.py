#!/usr/bin/env python3
"""
Markdown to ATS Text Converter

This script converts Markdown resume to ATS-friendly text format
by parsing the Definition List format and generating clean, structured text.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any

class ResumeData:
    def __init__(self):
        self.contact_info = {}
        self.work_experience = []
        self.education = []
        self.skills = []
        self.name = ""
        self.tagline = ""

class MarkdownToATSConverter:
    def __init__(self, markdown_file: str):
        self.markdown_file = markdown_file
        self.resume_data = ResumeData()
        
    def parse_markdown(self) -> ResumeData:
        """Parse Markdown file and extract structured data"""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        self._parse_frontmatter(content)
        
        # Parse work experience
        self._parse_work_experience(content)
        
        # Parse education
        self._parse_education(content)
        
        # Parse skills
        self._parse_skills(content)
        
        return self.resume_data
    
    def _parse_frontmatter(self, content: str):
        """Parse YAML frontmatter for contact info"""
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            lines = frontmatter.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'name':
                        self.resume_data.name = value
                    elif key == 'subtitle':
                        self.resume_data.tagline = value
                    else:
                        self.resume_data.contact_info[key] = value
    
    def _parse_work_experience(self, content: str):
        """Parse work experience section using Definition List format"""
        # Find work experience section
        work_section = self._extract_section(content, 'Work Experience', 'Education')
        if not work_section:
            return
        
        # Parse each job entry
        lines = work_section.split('\n')
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a job title (bold text)
            if line.startswith('**') and line.endswith('**'):
                # Save previous job if exists
                if current_job:
                    self.resume_data.work_experience.append(current_job)
                
                # Start new job
                job_title = line[2:-2]  # Remove ** markers
                current_job = {
                    'title': job_title,
                    'company': '',
                    'dates': '',
                    'achievements': []
                }
            
            # Check if this is a company/date line (starts with :)
            elif line.startswith(': '):
                if current_job:
                    # Parse "Company | _Date Range_" format
                    company_dates = line[2:]  # Remove ": "
                    if ' | ' in company_dates:
                        company, dates = company_dates.split(' | ', 1)
                        current_job['company'] = company.strip()
                        # Remove _ markers from dates
                        current_job['dates'] = dates.replace('_', '').strip()
                    else:
                        current_job['company'] = company_dates.strip()
            
            # Check if this is a project subheading
            elif line.startswith('***') and line.endswith('***'):
                if current_job:
                    project_title = line[3:-3]  # Remove *** markers
                    current_job['achievements'].append(f"Project: {project_title}")
            
            # Check if this is an achievement (starts with *)
            elif line.startswith('*   '):
                if current_job:
                    achievement = line[4:].strip()  # Remove "*   " prefix
                    current_job['achievements'].append(achievement)
            
            # Skip separator lines
            elif line.startswith('---'):
                continue
        
        # Add the last job
        if current_job:
            self.resume_data.work_experience.append(current_job)
    
    def _parse_education(self, content: str):
        """Parse education section"""
        edu_section = self._extract_section(content, 'Education', 'Skills')
        if not edu_section:
            return
        
        lines = edu_section.split('\n')
        current_edu = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse "Institution | Location | _Date Range_" format
            if ' | ' in line and not line.startswith('*'):
                parts = line.split(' | ')
                if len(parts) >= 3:
                    institution = parts[0].replace('**', '').strip()
                    location = parts[1].strip()
                    dates = parts[2].replace('_', '').strip()
                    
                    current_edu = {
                        'institution': institution,
                        'location': location,
                        'dates': dates,
                        'degree': ''
                    }
            
            # Check for degree on next line
            elif line.startswith('*   '):
                degree = line[4:].strip()
                if current_edu:
                    current_edu['degree'] = degree
                    self.resume_data.education.append(current_edu)
                    current_edu = None
    
    def _parse_skills(self, content: str):
        """Parse skills section"""
        skills_section = self._extract_section(content, 'Skills', '')
        if not skills_section:
            return
        
        lines = skills_section.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check if this is a skill category (bold text)
            if line.startswith('**') and line.endswith('**'):
                if current_category:
                    self.resume_data.skills.append(current_category)
                
                category_name = line[2:-2]  # Remove ** markers
                current_category = {
                    'name': category_name,
                    'skills': []
                }
            
            # Check if this is a skills list
            elif current_category and '•' in line:
                # Split by bullet points and clean up
                skill_items = line.split('•')
                for item in skill_items:
                    item = item.strip()
                    if item:
                        current_category['skills'].append(item)
        
        # Add the last category
        if current_category:
            self.resume_data.skills.append(current_category)
    
    def _extract_section(self, content: str, start_keyword: str, end_keyword: str) -> str:
        """Extract a specific section from the content"""
        lines = content.split('\n')
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
    
    def generate_ats_text(self) -> str:
        """Generate ATS-friendly text from parsed data"""
        ats_text = []
        
        # Header
        ats_text.append(f"NAME: {self.resume_data.name}")
        ats_text.append(f"TITLE: {self.resume_data.tagline}")
        ats_text.append("")
        
        # Contact Information
        ats_text.append("CONTACT INFORMATION:")
        for key, value in self.resume_data.contact_info.items():
            if value:
                ats_text.append(f"{key.upper()}: {value}")
        ats_text.append("")
        
        # Work Experience
        ats_text.append("WORK EXPERIENCE:")
        for job in self.resume_data.work_experience:
            ats_text.append(f"JOB TITLE: {job['title']}")
            ats_text.append(f"COMPANY: {job['company']}")
            ats_text.append(f"DATES: {job['dates']}")
            if job['achievements']:
                ats_text.append("ACHIEVEMENTS:")
                for achievement in job['achievements']:
                    ats_text.append(f"- {achievement}")
            ats_text.append("")
        
        # Education
        ats_text.append("EDUCATION:")
        for edu in self.resume_data.education:
            ats_text.append(f"DEGREE: {edu['degree']}")
            ats_text.append(f"INSTITUTION: {edu['institution']}")
            ats_text.append(f"LOCATION: {edu['location']}")
            ats_text.append(f"DATES: {edu['dates']}")
            ats_text.append("")
        
        # Skills
        ats_text.append("SKILLS:")
        for category in self.resume_data.skills:
            skills_list = ", ".join(category['skills'])
            ats_text.append(f"{category['name'].upper()}: {skills_list}")
        ats_text.append("")
        
        return '\n'.join(ats_text)
    
    def generate_ats_optimized_text(self) -> str:
        """Generate ATS-optimized text with better parsing format"""
        ats_text = []
        
        # Header
        ats_text.append(f"{self.resume_data.name}")
        ats_text.append(f"{self.resume_data.tagline}")
        ats_text.append("")
        
        # Contact Information
        contact_parts = []
        if self.resume_data.contact_info.get('email'):
            contact_parts.append(self.resume_data.contact_info['email'])
        if self.resume_data.contact_info.get('phone'):
            contact_parts.append(self.resume_data.contact_info['phone'])
        if self.resume_data.contact_info.get('location'):
            contact_parts.append(self.resume_data.contact_info['location'])
        if self.resume_data.contact_info.get('linkedin'):
            contact_parts.append(f"LinkedIn: {self.resume_data.contact_info['linkedin']}")
        
        ats_text.append(" | ".join(contact_parts))
        ats_text.append("")
        
        # Work Experience - ATS-friendly format
        ats_text.append("WORK EXPERIENCE")
        for job in self.resume_data.work_experience:
            # Format: Job Title: Company | Dates
            ats_text.append(f"{job['title']}: {job['company']} | {job['dates']}")
            
            # Add achievements as bullet points
            for achievement in job['achievements']:
                ats_text.append(f"* {achievement}")
            ats_text.append("")
        
        # Education - ATS-friendly format
        ats_text.append("EDUCATION")
        for edu in self.resume_data.education:
            # Format: Degree: Institution | Dates
            ats_text.append(f"{edu['degree']}: {edu['institution']} | {edu['dates']}")
        ats_text.append("")
        
        # Skills - ATS-friendly format
        ats_text.append("SKILLS")
        for category in self.resume_data.skills:
            # Format: Category: skill1, skill2, skill3
            skills_list = ", ".join(category['skills'])
            ats_text.append(f"{category['name']}: {skills_list}")
        
        return '\n'.join(ats_text)

def main():
    """Main function to convert Markdown to ATS text"""
    markdown_file = "my-resume/resume.md"
    output_file = "ats_data.txt"
    
    if not Path(markdown_file).exists():
        print(f"Error: {markdown_file} not found")
        return
    
    # Create converter
    converter = MarkdownToATSConverter(markdown_file)
    
    # Parse Markdown
    print("Parsing Markdown resume...")
    resume_data = converter.parse_markdown()
    
    # Generate ATS text
    print("Generating ATS-friendly text...")
    ats_text = converter.generate_ats_optimized_text()
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ats_text)
    
    print(f"ATS text generated: {output_file}")
    
    # Print summary
    print(f"\nParsed data summary:")
    print(f"- Name: {resume_data.name}")
    print(f"- Work Experience: {len(resume_data.work_experience)} jobs")
    print(f"- Education: {len(resume_data.education)} entries")
    print(f"- Skills: {len(resume_data.skills)} categories")
    
    # Show sample of generated text
    print(f"\nSample of generated ATS text:")
    print("-" * 50)
    lines = ats_text.split('\n')
    for line in lines[:20]:  # Show first 20 lines
        print(line)
    if len(lines) > 20:
        print("...")

if __name__ == "__main__":
    main()
