#!/usr/bin/env python3
"""
Simple ATS Text Converter

This script creates a clean, ATS-friendly text version of the resume
by parsing the Markdown and generating structured text that ATS systems can parse.
"""

import re
from pathlib import Path

def parse_markdown_resume(markdown_file: str) -> str:
    """Parse Markdown resume and generate ATS-friendly text"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ats_lines = []
    
    # Extract name and title
    name_match = re.search(r'name:\s*(.+)', content)
    title_match = re.search(r'subtitle:\s*(.+)', content)
    
    if name_match:
        ats_lines.append(name_match.group(1).strip())
    if title_match:
        ats_lines.append(title_match.group(1).strip())
    
    ats_lines.append("")
    
    # Extract contact info
    email_match = re.search(r'email:\s*(.+)', content)
    phone_match = re.search(r'phone:\s*(.+)', content)
    location_match = re.search(r'location:\s*(.+)', content)
    linkedin_match = re.search(r'linkedin:\s*(.+)', content)
    
    contact_parts = []
    if email_match:
        contact_parts.append(email_match.group(1).strip())
    if phone_match:
        contact_parts.append(phone_match.group(1).strip())
    if location_match:
        contact_parts.append(location_match.group(1).strip())
    if linkedin_match:
        contact_parts.append(f"LinkedIn: {linkedin_match.group(1).strip()}")
    
    if contact_parts:
        ats_lines.append(" | ".join(contact_parts))
        ats_lines.append("")
    
    # Extract work experience
    ats_lines.append("WORK EXPERIENCE")
    
    # Find work experience section
    work_start = content.find("### Work Experience")
    edu_start = content.find("### Education")
    
    if work_start != -1 and edu_start != -1:
        work_section = content[work_start:edu_start]
        
        # Parse each job using Definition List format
        lines = work_section.split('\n')
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Job title (bold text)
            if line.startswith('**') and line.endswith('**') and not line.startswith('***'):
                if current_job:
                    # Format: Job Title: Company | Dates
                    ats_lines.append(f"{current_job['title']}: {current_job['company']} | {current_job['dates']}")
                    for achievement in current_job['achievements']:
                        ats_lines.append(f"* {achievement}")
                    ats_lines.append("")
                
                # Start new job
                job_title = line[2:-2]  # Remove ** markers
                current_job = {
                    'title': job_title,
                    'company': '',
                    'dates': '',
                    'achievements': []
                }
            
            # Company and dates (starts with :)
            elif line.startswith(': '):
                if current_job:
                    company_dates = line[2:]  # Remove ": "
                    if ' | ' in company_dates:
                        company, dates = company_dates.split(' | ', 1)
                        current_job['company'] = company.strip()
                        current_job['dates'] = dates.replace('_', '').strip()
                    else:
                        current_job['company'] = company_dates.strip()
            
            # Project subheading
            elif line.startswith('***') and line.endswith('***'):
                if current_job:
                    project_title = line[3:-3]  # Remove *** markers
                    current_job['achievements'].append(f"Project: {project_title}")
            
            # Achievement (starts with *)
            elif line.startswith('*   '):
                if current_job:
                    achievement = line[4:].strip()  # Remove "*   " prefix
                    current_job['achievements'].append(achievement)
        
        # Add the last job
        if current_job:
            ats_lines.append(f"{current_job['title']}: {current_job['company']} | {current_job['dates']}")
            for achievement in current_job['achievements']:
                ats_lines.append(f"* {achievement}")
            ats_lines.append("")
    
    # Extract education
    ats_lines.append("EDUCATION")
    
    edu_start = content.find("### Education")
    skills_start = content.find("### Skills")
    
    if edu_start != -1 and skills_start != -1:
        edu_section = content[edu_start:skills_start]
        
        # Look for education pattern: **Institution** | Location | _Dates_
        edu_match = re.search(r'\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*_([^_]+)_', edu_section)
        if edu_match:
            institution = edu_match.group(1).strip()
            location = edu_match.group(2).strip()
            dates = edu_match.group(3).strip()
            
            # Look for degree on next line
            degree_match = re.search(r'\*\s*([^*\n]+)', edu_section)
            if degree_match:
                degree = degree_match.group(1).strip()
                ats_lines.append(f"{degree}: {institution} | {dates}")
            else:
                ats_lines.append(f"{institution} | {dates}")
    
    ats_lines.append("")
    
    # Extract skills
    ats_lines.append("SKILLS")
    
    if skills_start != -1:
        skills_section = content[skills_start:]
        
        # Parse skill categories
        skill_categories = re.findall(r'\*\*([^*]+)\*\*\s*\n([^*\n]+)', skills_section)
        
        for category_name, skills_text in skill_categories:
            # Clean up skills text
            skills_text = skills_text.strip()
            # Replace bullet points with commas
            skills_text = re.sub(r'•', ',', skills_text)
            # Clean up extra spaces
            skills_text = re.sub(r'\s+', ' ', skills_text)
            
            ats_lines.append(f"{category_name.strip()}: {skills_text}")
    
    # Clean up ampersands for better ATS compatibility
    ats_text = '\n'.join(ats_lines)
    ats_text = ats_text.replace('&', 'and')
    
    return ats_text

def main():
    """Main function to convert Markdown to ATS text"""
    markdown_file = "my-resume/resume.md"
    output_file = "ats_data.txt"
    
    if not Path(markdown_file).exists():
        print(f"Error: {markdown_file} not found")
        return
    
    print("Converting Markdown to ATS-friendly text...")
    
    # Generate ATS text
    ats_text = parse_markdown_resume(markdown_file)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ats_text)
    
    print(f"ATS text generated: {output_file}")
    
    # Show sample
    print("\nGenerated ATS text:")
    print("-" * 50)
    lines = ats_text.split('\n')
    for line in lines[:30]:  # Show first 30 lines
        print(line)
    if len(lines) > 30:
        print("...")

if __name__ == "__main__":
    main()
