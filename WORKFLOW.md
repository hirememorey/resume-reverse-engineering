# Resume Generation Workflow

## Overview

This document describes the complete workflow for generating a professional PDF resume from Markdown source using the AltaCV LaTeX template.

## Workflow Steps

### 1. Edit Source Markdown
**File**: `my-resume/resume.md`

**Requirements**:
- Use Definition List format for work experience
- Include colons before company names
- Maintain consistent formatting

**Example**:
```markdown
**Job Title**
: Company Name | _Date Range_
*   Achievement 1
*   Achievement 2
```

### 2. Update LaTeX File
**File**: `harris_resume.tex`

**Manual Updates Required**:
- Copy content from Markdown to LaTeX
- Convert Definition Lists to `\cvevent` commands
- Ensure company names are in second parameter

**Example Conversion**:
```markdown
**Co-Founder & CEO, Scalpel**
: Scalpel | _October 2022 - January 2025_
```

Becomes:
```latex
\cvevent{Co-Founder \& CEO, Scalpel}{Scalpel}{October 2022 - January 2025}{}
```

### 3. Compile LaTeX
**Command**: `xelatex harris_resume.tex`

**Critical Requirements**:
- Must use XeLaTeX (not pdfLaTeX)
- Run twice to resolve cross-references
- Check for compilation errors

### 4. Review Output
**File**: `harris_resume.pdf`

**Verification Checklist**:
- [ ] Company names appear in red
- [ ] Job titles are bold
- [ ] Dates are italic
- [ ] Layout is correct
- [ ] No missing content

### 5. ATS Testing (NEW)
**Purpose**: Ensure resume is ATS-compatible while maintaining human readability

**Basic ATS Test**:
```bash
python ats_testing_script.py harris_resume.pdf
```

**Advanced ATS Test**:
```bash
python advanced_ats_test.py harris_resume.pdf --output ats_results.json
```

**Create ATS-Optimized Version**:
```bash
python create_ats_optimized_resume.py
xelatex harris_resume_ats_optimized.tex
```

**Compare Versions**:
```bash
python compare_resumes.py
```

**ATS Verification Checklist**:
- [ ] ATS score is 70+ (target: 90+)
- [ ] Text extracts cleanly
- [ ] Contact information is complete
- [ ] Work experience is parseable
- [ ] Skills section is properly formatted
- [ ] No problematic characters
- [ ] Human readability maintained
- [ ] PDF fits on one page with all sections

## Detailed Workflow

### Step 1: Content Creation

#### 1.1 Edit Markdown
```bash
# Open the source file
code my-resume/resume.md

# Or use any text editor
nano my-resume/resume.md
```

#### 1.2 Follow Definition List Format
- Job titles: `**Bold Title**`
- Company names: `: Company Name | _Date Range_`
- Bullet points: `*   Achievement`
- Section separators: `---`

#### 1.3 Validate Format
- Check all colons are present
- Verify consistent formatting
- Test with small sections first

### Step 2: LaTeX Conversion

#### 2.1 Manual Conversion Process
1. Open `harris_resume.tex`
2. Locate the Work Experience section
3. Replace content with LaTeX equivalents
4. Ensure proper `\cvevent` structure

#### 2.2 LaTeX Structure

**Standard Format (Visual Only):**
```latex
\cvsection{Work Experience}

\cvevent{Job Title}{Company Name}{Date Range}{}

\textbf{Project Subheading}
\begin{itemize}
\item Achievement 1
\item Achievement 2
\end{itemize}

\cvevent{Next Job}{Next Company}{Next Dates}{}
\begin{itemize}
\item Next achievement
\end{itemize}
```

**ATS-Optimized Format (Recommended):**
```latex
\cvsection{Work Experience}

\atscvevent{Job Title}{Company Name}{Date Range}{}

\textbf{Project Subheading}
\begin{itemize}
\item Achievement 1
\item Achievement 2
\end{itemize}

\atscvevent{Next Job}{Next Company}{Next Dates}{}
\begin{itemize}
\item Next achievement
\end{itemize}
```

**Note**: The `\atscvevent` command renders work experience in ATS-friendly format (`Job Title: Company | Dates`) while maintaining visual appeal. This is the recommended approach for better ATS compatibility.

#### 2.2.1 Custom LaTeX Command Definition

To use the ATS-optimized format, add this command definition to your LaTeX file:

```latex
% Custom ATS-friendly work experience command
\newcommand{\atscvevent}[4]{%
  % ATS-friendly format that parsers can extract
  \textbf{#1}: #2 | \textit{#3}%
  \vspace{0.3em}%
}
```

This command takes four parameters:
- `#1`: Job Title (rendered in bold)
- `#2`: Company Name (rendered in normal text)
- `#3`: Date Range (rendered in italics)
- `#4`: Location (not used in current implementation)

#### 2.3 Special Characters
- `&` becomes `\&`
- `%` becomes `\%`
- `$` becomes `\$`
- `#` becomes `\#`

### Step 3: Compilation

#### 3.1 Check Prerequisites
```bash
# Verify XeLaTeX is available
which xelatex

# Check current directory
pwd
```

#### 3.2 Compile LaTeX
```bash
# First compilation
xelatex harris_resume.tex

# Second compilation (for cross-references)
xelatex harris_resume.tex
```

#### 3.3 Handle Errors
- Check `harris_resume.log` for errors
- Fix LaTeX syntax issues
- Recompile after fixes

### Step 4: Quality Assurance

#### 4.1 Visual Inspection
- Open `harris_resume.pdf`
- Check all sections are present
- Verify formatting is correct
- Look for missing content

#### 4.2 Color Verification
- Company names should be red
- Job titles should be bold
- Dates should be italic
- Headings should be dark red

#### 4.3 Layout Check
- Two-column layout is correct
- Sidebar is properly positioned
- Text doesn't overflow
- Images are properly sized

## Automation Scripts

### Basic Compilation Script
Create `compile.sh`:
```bash
#!/bin/bash
echo "Compiling resume with XeLaTeX..."
xelatex harris_resume.tex
xelatex harris_resume.tex
echo "Compilation complete. Output: harris_resume.pdf"
```

Make executable:
```bash
chmod +x compile.sh
./compile.sh
```

### Advanced Build Script
Create `build.sh`:
```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting resume build process...${NC}"

# Check if XeLaTeX is available
if ! command -v xelatex &> /dev/null; then
    echo -e "${RED}Error: XeLaTeX not found. Please install TeX Live.${NC}"
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -f harris_resume.aux harris_resume.log harris_resume.out

# First compilation
echo -e "${YELLOW}First compilation...${NC}"
xelatex -interaction=nonstopmode harris_resume.tex

# Check for errors
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: First compilation failed. Check harris_resume.log${NC}"
    exit 1
fi

# Second compilation (for cross-references)
echo -e "${YELLOW}Second compilation...${NC}"
xelatex -interaction=nonstopmode harris_resume.tex

# Check if PDF was created
if [ -f "harris_resume.pdf" ]; then
    echo -e "${GREEN}Success! Resume generated: harris_resume.pdf${NC}"
    
    # Open PDF if on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open harris_resume.pdf
    fi
else
    echo -e "${RED}Error: PDF was not generated.${NC}"
    exit 1
fi
```

## Version Control

### Git Workflow
```bash
# Before making changes
git checkout -b feature/update-resume

# After editing Markdown
git add my-resume/resume.md
git commit -m "Update resume content"

# After updating LaTeX
git add harris_resume.tex
git commit -m "Update LaTeX formatting"

# After successful compilation
git add harris_resume.pdf
git commit -m "Generate updated PDF"

# Push changes
git push origin feature/update-resume
```

### File Tracking
- **Track**: `resume.md`, `harris_resume.tex`
- **Ignore**: `*.aux`, `*.log`, `*.out`
- **Optional**: `harris_resume.pdf` (can be regenerated)

## Troubleshooting Workflow

### Common Issues
1. **Compilation fails**: Check LaTeX syntax
2. **Missing colors**: Verify XeLaTeX usage
3. **Formatting issues**: Check Definition List format
4. **Missing content**: Verify manual conversion

### Debug Steps
1. Check `harris_resume.log` for errors
2. Test with minimal content
3. Verify XeLaTeX installation
4. Check font availability

## Best Practices

### Content Management
- Keep Markdown as source of truth
- Update LaTeX manually for now
- Test changes incrementally
- Maintain backup versions

### Compilation
- Always use XeLaTeX
- Run compilation twice
- Check for errors in log
- Verify output quality

### Quality Assurance
- Review PDF output
- Check color formatting
- Verify layout integrity
- Test on different systems

## ATS Testing Integration

### Testing Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

### Testing Scripts Overview
- **`ats_testing_script.py`**: Basic ATS compatibility testing
- **`advanced_ats_test.py`**: Simulates actual ATS parsing
- **`compare_resumes.py`**: Compares original vs optimized versions
- **`create_ats_optimized_resume.py`**: Creates ATS-optimized versions

### ATS Testing Best Practices
1. **Always test after changes**: Run ATS tests after any resume modifications
2. **Compare versions**: Use comparison tool to verify improvements
3. **Target score**: Aim for 90+ ATS score
4. **Maintain readability**: Ensure human appeal is preserved
5. **Document results**: Save test results for future reference

## Future Improvements

### Automation Goals
- Automated Markdown to LaTeX conversion
- Template variable substitution
- Automated compilation pipeline
- Quality assurance checks
- **NEW**: Automated ATS optimization pipeline

### Potential Tools
- Custom Pandoc filters
- LaTeX template engines
- CI/CD pipeline
- Automated testing
- **NEW**: Real ATS system integration testing
