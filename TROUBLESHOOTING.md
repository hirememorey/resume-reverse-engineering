# Troubleshooting Guide

## Quick Diagnosis

### Check System Status
```bash
# Verify XeLaTeX installation
which xelatex

# Check current directory
pwd

# List available files
ls -la *.tex *.md *.pdf
```

### Test Basic Compilation
```bash
# Try compiling
xelatex harris_resume.tex

# Check for errors
cat harris_resume.log | grep -i error
```

## Common Issues & Solutions

### Issue 1: Compilation Fails with Font Error

#### Symptoms
```
! Undefined control sequence.
l.10 \setmainfont
                 {Helvetica}
```

#### Root Cause
Using pdfLaTeX instead of XeLaTeX

#### Solution
```bash
# Use XeLaTeX instead
xelatex harris_resume.tex

# Or with full path
/Library/TeX/texbin/xelatex harris_resume.tex
```

#### Prevention
- Always use XeLaTeX for this template
- Create alias: `alias compile-resume='xelatex harris_resume.tex'`

### Issue 2: Company Names Not Red

#### Symptoms
- Company names appear in default color
- No red styling in PDF output

#### Root Cause
Missing colons in Markdown Definition List format

#### Solution
**Check Markdown format:**
```markdown
# WRONG
**Job Title**
Company Name | _Date Range_

# CORRECT
**Job Title**
: Company Name | _Date Range_
```

**Verify LaTeX structure:**
```latex
# WRONG
\cvevent{Job Title}{}{Date Range}{}

# CORRECT
\cvevent{Job Title}{Company Name}{Date Range}{}
```

#### Prevention
- Always include colons before company names
- Test with small sections first
- Use the validation checklist

### Issue 3: Missing Company Names in PDF

#### Symptoms
- Company names don't appear in PDF
- Empty spaces where company names should be

#### Root Cause
Empty second parameter in `\cvevent` commands

#### Solution
**Check LaTeX file:**
```latex
# Find and fix empty company fields
\cvevent{Job Title}{}{Date Range}{}
# Should be:
\cvevent{Job Title}{Company Name}{Date Range}{}
```

**Search and replace:**
```bash
# Find empty company fields
grep -n "\\cvevent.*{}{" harris_resume.tex
```

### Issue 4: LaTeX Compilation Hangs

#### Symptoms
- Compilation starts but never finishes
- No error messages
- Process appears stuck

#### Root Cause
- Missing font files
- Infinite loop in LaTeX processing
- Large file processing

#### Solution
```bash
# Kill the process
pkill xelatex

# Check for missing fonts
fc-list | grep -i helvetica

# Try with different font
# Edit harris_resume.tex and change:
\setmainfont{Arial}  # Instead of Helvetica
```

### Issue 5: PDF Generation Fails

#### Symptoms
- LaTeX compiles successfully
- No PDF file created
- Error messages about output

#### Root Cause
- Permission issues
- Disk space problems
- LaTeX output configuration

#### Solution
```bash
# Check disk space
df -h

# Check permissions
ls -la harris_resume.*

# Try different output directory
xelatex -output-directory=/tmp harris_resume.tex
```

### Issue 6: Formatting Issues in PDF

#### Symptoms
- Text overlaps
- Incorrect spacing
- Missing sections
- Layout problems

#### Root Cause
- LaTeX syntax errors
- Template compatibility issues
- Font size problems

#### Solution
**Check LaTeX syntax:**
```bash
# Look for syntax errors
grep -n "\\\\" harris_resume.tex | grep -v "\\\\[a-zA-Z]"

# Check for unmatched braces
grep -o '{' harris_resume.tex | wc -l
grep -o '}' harris_resume.tex | wc -l
```

**Verify template compatibility:**
- Ensure using correct AltaCV version
- Check for package conflicts
- Verify font availability

### Issue 7: Slow Compilation

#### Symptoms
- Compilation takes several minutes
- System becomes unresponsive
- High CPU usage

#### Root Cause
- Large images
- Complex TikZ graphics
- Font loading issues

#### Solution
```bash
# Optimize images
# Convert large images to appropriate size

# Use faster compilation flags
xelatex -interaction=nonstopmode harris_resume.tex

# Check for large files
ls -lh *.png *.jpg *.pdf
```

## Debugging Commands

### Check LaTeX Installation
```bash
# Verify TeX Live installation
tex --version

# Check XeLaTeX specifically
xelatex --version

# List available packages
tlmgr list --only-installed | grep altacv
```

### Analyze Compilation Log
```bash
# View full log
cat harris_resume.log

# Find errors only
grep -i error harris_resume.log

# Find warnings
grep -i warning harris_resume.log

# Check font issues
grep -i font harris_resume.log
```

### Test Minimal Document
Create `test.tex`:
```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Helvetica}
\begin{document}
Test document
\end{document}
```

Compile:
```bash
xelatex test.tex
```

### Check Font Availability
```bash
# List all fonts
fc-list

# Search for specific font
fc-list | grep -i helvetica

# Check font paths
fc-cache -v
```

## System-Specific Issues

### macOS Issues

#### Font Problems
```bash
# Refresh font cache
sudo atsutil databases -remove

# Check font installation
ls /Library/Fonts/ | grep -i helvetica
```

#### XeLaTeX Path Issues
```bash
# Find XeLaTeX
find /usr -name xelatex 2>/dev/null
find /Library -name xelatex 2>/dev/null

# Add to PATH
export PATH="/Library/TeX/texbin:$PATH"
```

### Linux Issues

#### Missing Packages
```bash
# Install required packages
sudo apt-get install texlive-xetex texlive-fonts-recommended

# Or for CentOS/RHEL
sudo yum install texlive-xetex
```

#### Font Configuration
```bash
# Install fonts
sudo fc-cache -fv

# Check font configuration
fc-list | grep -i helvetica
```

### Windows Issues

#### MiKTeX vs TeX Live
- Use TeX Live for better XeLaTeX support
- Ensure XeLaTeX is in PATH
- Check font installation

#### Font Installation
- Install fonts through Windows Font Manager
- Restart after font installation
- Verify font availability

## Recovery Procedures

### Complete Reset
```bash
# Backup current work
cp harris_resume.tex harris_resume.tex.backup
cp my-resume/resume.md my-resume/resume.md.backup

# Clean LaTeX auxiliary files
rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

# Start fresh compilation
xelatex harris_resume.tex
```

### Restore from Backup
```bash
# Restore from backup
cp harris_resume.tex.backup harris_resume.tex

# Recompile
xelatex harris_resume.tex
```

### Minimal Working Version
Create `minimal.tex`:
```latex
\documentclass[10pt,a4paper,withhyper]{altacv}
\geometry{left=1.25cm,right=1.25cm,top=1.5cm,bottom=1.5cm,columnsep=1.2cm}
\usepackage{paracol}
\setmainfont{Helvetica}
\setsansfont{Helvetica}
\renewcommand{\familydefault}{\sfdefault}

\definecolor{SlateGrey}{HTML}{2E2E2E}
\definecolor{LightGrey}{HTML}{666666}
\definecolor{DarkPastelRed}{HTML}{450808}
\definecolor{PastelRed}{HTML}{8F0D0D}
\colorlet{name}{black}
\colorlet{tagline}{PastelRed}
\colorlet{heading}{DarkPastelRed}
\colorlet{headingrule}{LightGrey}
\colorlet{accent}{PastelRed}
\colorlet{emphasis}{SlateGrey}
\colorlet{body}{LightGrey}

\begin{document}
\name{Test Name}
\tagline{Test Tagline}
\makecvheader

\cvsection{Work Experience}
\cvevent{Test Job}{Test Company}{Test Dates}{}
\begin{itemize}
\item Test achievement
\end{itemize}

\end{document}
```

## ATS Testing Issues

### Issue 1: ATS Test Scripts Not Working

#### Symptoms
- Python scripts fail to run
- Import errors for PDF libraries
- Missing dependencies

#### Solution
```bash
# Install required dependencies
pip install -r requirements.txt

# Verify installation
python -c "import PyPDF2, pdfplumber; print('Dependencies OK')"
```

### Issue 2: Low ATS Score

#### Symptoms
- ATS score below 70
- Text extraction issues
- Parsing errors

#### Solution
```bash
# Run comprehensive analysis
python advanced_ats_test.py harris_resume.pdf

# Create optimized version
python create_ats_optimized_resume.py

# Test optimized version
python advanced_ats_test.py harris_resume_ats_optimized.pdf
```

### Issue 3: ATS Optimization Not Working

#### Symptoms
- Optimized version has same issues
- No improvement in ATS score
- Characters not replaced properly

#### Solution
1. Check LaTeX file for manual fixes needed
2. Verify character replacements in source
3. Recompile with XeLaTeX
4. Test with comparison script

### Issue 4: Human Readability Lost

#### Symptoms
- Resume looks worse after optimization
- Formatting broken
- Visual appeal reduced

#### Solution
1. Use comparison tool to identify changes
2. Adjust optimization parameters
3. Test both versions side by side
4. Maintain balance between ATS and human appeal

## Getting Help

### Log Analysis
1. Check `harris_resume.log` for errors
2. Look for specific error messages
3. Search for solutions online
4. Check LaTeX documentation

### ATS Testing Resources
- `ATS_TESTING_GUIDE.md`: Comprehensive testing methodology
- Test result JSON files for detailed analysis
- Comparison tool output for version differences

### Community Resources
- LaTeX Stack Exchange
- AltaCV GitHub repository
- TeX Live documentation
- Font configuration guides
- ATS compatibility forums

### Escalation Steps
1. Try minimal working example
2. Check system requirements
3. Verify installation
4. Run ATS tests for specific issues
5. Contact support if needed

## Prevention Checklist

### Before Starting
- [ ] Verify XeLaTeX installation
- [ ] Check font availability
- [ ] Test with minimal document
- [ ] Backup existing work

### During Development
- [ ] Test changes incrementally
- [ ] Check compilation after each change
- [ ] Maintain working backups
- [ ] Document any customizations

### Before Final Compilation
- [ ] Validate Markdown format
- [ ] Check LaTeX syntax
- [ ] Verify all content is present
- [ ] Test on different systems
