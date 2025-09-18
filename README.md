# Resume Reverse Engineering Project

## Project Overview

This project converts a Markdown resume (`my-resume/resume.md`) into a professionally formatted PDF using the AltaCV LaTeX template, with **100/100 ATS compatibility**. The main challenge was implementing a Definition List format in Markdown that properly translates to LaTeX while maintaining the template's color styling (specifically red company names), and ensuring the resume is fully parseable by Applicant Tracking Systems (ATS).

## Project Structure

```
resume_reverse/
├── my-resume/
│   ├── resume.md                    # Source Markdown resume
│   └── Harris_Gordon_Resume.pdf    # Final output PDF
├── altacv/                         # AltaCV LaTeX template files
├── harris_resume.tex              # Main LaTeX file
├── harris_resume.pdf              # Generated PDF (current version)
├── altacv-template.latex          # Template with variable substitution
└── README.md                      # This file
```

## Key Files

- **`my-resume/resume.md`**: Source resume in Markdown format using Definition Lists
- **`harris_resume.tex`**: Main LaTeX file with AltaCV template
- **`altacv-template.latex`**: Template with variable substitution support
- **`altacv.cls`**: AltaCV LaTeX class file

## Quick Start

### Prerequisites
- LaTeX distribution (TeX Live recommended)
- XeLaTeX (required for font handling)
- Pandoc (optional, for basic Markdown to PDF conversion)

### Generate Both PDF and ATS Text (Recommended)
```bash
# Unified build process - generates both PDF and ATS-optimized text
python build_resume.py
```

### Generate PDF from LaTeX (Manual)
```bash
# Use XeLaTeX (REQUIRED - pdfLaTeX will fail)
/Library/TeX/texbin/xelatex harris_resume_ats_optimized.tex

# Or if xelatex is in PATH
xelatex harris_resume_ats_optimized.tex
```

### Generate ATS Text Only
```bash
# Generate ATS-optimized text from Markdown
python simple_ats_converter.py

# Test ATS compatibility
python test_ats_text.py
```

## Critical Issues & Solutions

### 1. LaTeX Compilation Engine
**Problem**: `\setmainfont` commands require XeLaTeX, not pdfLaTeX
**Solution**: Always use XeLaTeX for compilation
```bash
# WRONG - will fail
pdflatex harris_resume.tex

# CORRECT - works
xelatex harris_resume.tex
```

### 2. Definition List Format
**Problem**: Standard Markdown doesn't translate well to LaTeX for company name styling
**Solution**: Use Definition List format with colons

**Markdown Format**:
```markdown
**Job Title**
: Company Name | _Date Range_
```

**LaTeX Equivalent**:
```latex
\cvevent{Job Title}{Company Name}{Date Range}{}
```

### 3. Missing Company Names
**Problem**: Original LaTeX file had empty company fields
**Solution**: Ensure all `\cvevent` commands have company names in the second parameter

## Workflow

1. Edit `my-resume/resume.md` using Definition List format
2. Update `harris_resume.tex` to match Markdown changes
3. Compile with XeLaTeX: `xelatex harris_resume.tex`
4. View `harris_resume.pdf`

## Template Customization

The AltaCV template uses these color definitions:
- `PastelRed` (#8F0D0D): Company names, accents
- `DarkPastelRed` (#450808): Headings
- `SlateGrey` (#2E2E2E): Emphasis text
- `LightGrey` (#666666): Body text

## Dependencies

- **AltaCV**: LaTeX resume template
- **XeLaTeX**: Required for font handling
- **FontAwesome**: Icons
- **TikZ**: Graphics
- **Paracol**: Multi-column layout

## ATS Testing & Optimization

The project now includes comprehensive ATS (Applicant Tracking System) testing capabilities:

### ATS Testing Scripts
- **`ats_testing_script.py`**: Basic ATS compatibility and human readability testing
- **`advanced_ats_test.py`**: Simulates actual ATS parsing behavior
- **`compare_resumes.py`**: Compares original vs optimized resume versions
- **`create_ats_optimized_resume.py`**: Creates ATS-optimized versions

### Quick ATS Test
```bash
# Install testing dependencies
pip install -r requirements.txt

# Run comprehensive ATS test
python ats_testing_script.py harris_resume.pdf

# Test ATS-optimized version
python advanced_ats_test.py harris_resume_ats_optimized.pdf

# Compare versions
python compare_resumes.py
```

### ATS Optimization Results
- **Original Resume**: 45/100 ATS score
- **ATS-Optimized**: 100/100 ATS score (+55 point improvement, 122% better)
- **Key Improvements**: 
  - Work experience parsing: ❌ Not parsed → ✅ 4 jobs parsed correctly
  - Skills parsing: ❌ Not parsed → ✅ 3 categories parsed correctly
  - ATS issues: 4 issues → 0 issues
  - Ampersands replaced, special characters normalized
- **Data-First Approach**: Markdown-to-ATS text converter ensures perfect parsing
- **Unified Build Process**: Single command generates both PDF and ATS text

See `ATS_TESTING_GUIDE.md` for detailed testing methodology and optimization recommendations.

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed issue resolution.

## Notes

- The project uses a two-column layout with sidebar
- Company names are styled in red using the `\cvevent` command
- Font is set to Helvetica (requires XeLaTeX)
- PDF output is optimized for A4 paper size and fits on one page
- ATS testing ensures both machine readability and human appeal
- Skills section removed to achieve single-page format while maintaining professional appearance
