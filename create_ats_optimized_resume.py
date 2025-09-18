#!/usr/bin/env python3
"""
Create ATS-Optimized Resume

This script creates an ATS-optimized version of the resume
that maintains human readability while improving ATS compatibility.
"""

import re
from pathlib import Path

def create_ats_optimized_resume(input_file: str, output_file: str):
    """Create an ATS-optimized version of the resume"""
    
    # Read the original LaTeX file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply ATS optimizations
    optimized_content = content
    
    # 1. Replace ampersands with 'and'
    optimized_content = optimized_content.replace('\\&', 'and')
    optimized_content = optimized_content.replace('&', 'and')
    
    # 2. Replace special characters that might cause ATS issues
    optimized_content = optimized_content.replace('•', '*')
    optimized_content = optimized_content.replace('◦', '*')
    optimized_content = optimized_content.replace('·', '*')
    
    # 3. Remove or replace non-ASCII characters
    optimized_content = optimized_content.replace('–', '-')
    optimized_content = optimized_content.replace('—', '-')
    optimized_content = optimized_content.replace('"', '"')
    optimized_content = optimized_content.replace('"', '"')
    optimized_content = optimized_content.replace(''', "'")
    optimized_content = optimized_content.replace(''', "'")
    
    # 4. Ensure consistent formatting for work experience
    # This is more complex and would require parsing the LaTeX structure
    
    # 5. Add ATS-friendly section headers
    # Replace cvsection with more ATS-friendly formatting
    
    # Write the optimized version
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print(f"ATS-optimized resume created: {output_file}")
    return optimized_content

def create_ats_optimized_markdown(input_file: str, output_file: str):
    """Create an ATS-optimized Markdown version"""
    
    # Read the original Markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply ATS optimizations
    optimized_content = content
    
    # 1. Replace ampersands with 'and'
    optimized_content = optimized_content.replace('&', 'and')
    
    # 2. Replace special bullet points
    optimized_content = optimized_content.replace('•', '*')
    optimized_content = optimized_content.replace('◦', '*')
    optimized_content = optimized_content.replace('·', '*')
    
    # 3. Remove or replace non-ASCII characters
    optimized_content = optimized_content.replace('–', '-')
    optimized_content = optimized_content.replace('—', '-')
    optimized_content = optimized_content.replace('"', '"')
    optimized_content = optimized_content.replace('"', '"')
    optimized_content = optimized_content.replace(''', "'")
    optimized_content = optimized_content.replace(''', "'")
    
    # 4. Ensure consistent formatting
    # Remove extra spaces and normalize whitespace
    optimized_content = re.sub(r'\s+', ' ', optimized_content)
    optimized_content = re.sub(r'\n\s*\n', '\n\n', optimized_content)
    
    # 5. Add ATS-friendly keywords
    # This could be expanded to add industry-specific keywords
    
    # Write the optimized version
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print(f"ATS-optimized Markdown created: {output_file}")
    return optimized_content

def main():
    # Create ATS-optimized versions
    print("Creating ATS-optimized resume versions...")
    
    # Optimize LaTeX file
    create_ats_optimized_resume('harris_resume.tex', 'harris_resume_ats_optimized.tex')
    
    # Optimize Markdown file
    create_ats_optimized_markdown('my-resume/resume.md', 'my-resume/resume_ats_optimized.md')
    
    print("\nATS optimization complete!")
    print("Files created:")
    print("  - harris_resume_ats_optimized.tex")
    print("  - my-resume/resume_ats_optimized.md")
    print("\nNext steps:")
    print("  1. Compile the optimized LaTeX file: xelatex harris_resume_ats_optimized.tex")
    print("  2. Test the optimized PDF with the ATS testing scripts")
    print("  3. Compare results with the original resume")

if __name__ == "__main__":
    main()
