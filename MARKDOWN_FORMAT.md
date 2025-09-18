# Markdown Definition List Format Guide

## Overview

This project uses a specific Markdown format called "Definition Lists" to ensure proper translation to LaTeX while maintaining the template's color styling. The key requirement is using colons (`:`) before company names to trigger the red styling in the LaTeX output.

## Definition List Format

### Basic Structure
```markdown
**Job Title**
: Company Name | _Date Range_

**Another Job Title**
: Another Company | _Another Date Range_
```

### Key Requirements
1. **Colon before company name** - This is the most critical part
2. **Bold job titles** - Use `**Job Title**`
3. **Company and dates on same line** - Separated by ` | `
4. **Italic dates** - Use `_Date Range_`

## Complete Example

```markdown
### Work Experience

**Independent Consultant / Venture Builder**
: Self-Employed | _February 2025 - Present_

***Project 1: Turnaround Operator (YC-Backed Series A Client)***
*   Embedded as the founding Account Manager to stabilize a chaotic GTM motion and retain high-value enterprise accounts.
*   Saved $900k in at-risk ARR by quarterbacking a P0 crisis response for a flagship account, co-designing a new enterprise release protocol to rebuild trust.

---

**Co-Founder & CEO, Scalpel**
: Scalpel | _October 2022 - January 2025_
*   Built a vertical SaaS platform for medical supply management that cut 20+ weekly staff hours, leading the company to acquisition negotiations.
*   Raised venture funding from Bienville Capital after validating product-market fit with 65+ customer interviews.

---

**Commercial Product Manager, Capsule Pharmacy**
: Capsule Pharmacy | _February 2021 - October 2022_
*   Launched and scaled the company's first B2B2C growth product (Patient.Page), driving a 20% increase in new customer acquisition in Year 1.

---

**Co-Founder & COO, eevo**
: eevo | _May 2014 - January 2021_
*   Developed VR training tools that improved surgery patient satisfaction by 33%, leading the company from inception to a successful exit.
*   Raised venture funding from Techstars, Sinai Ventures, and FundersClub while leading product, operations, and sales.
```

## LaTeX Translation

### How Definition Lists Map to LaTeX
```markdown
**Job Title**
: Company Name | _Date Range_
```

Becomes:
```latex
\cvevent{Job Title}{Company Name}{Date Range}{}
```

### Why This Format Works
1. **Colon triggers LaTeX parsing** - The `:` tells the converter to treat the next line as a definition
2. **Company name gets styled** - The second parameter in `\cvevent` gets the red color
3. **Dates are formatted** - The third parameter gets italic styling
4. **Job title is bold** - The first parameter gets bold styling

## Common Mistakes to Avoid

### ❌ Wrong: Missing Colon
```markdown
**Job Title**
Company Name | _Date Range_
```
**Result**: Company name won't be styled in red

### ❌ Wrong: Colon in Wrong Place
```markdown
**Job Title**
Company Name: | _Date Range_
```
**Result**: LaTeX parsing error

### ❌ Wrong: Multiple Lines for Company
```markdown
**Job Title**
: Company Name
| _Date Range_
```
**Result**: Broken LaTeX structure

### ✅ Correct: Proper Format
```markdown
**Job Title**
: Company Name | _Date Range_
```
**Result**: Perfect LaTeX translation with red company names

## Advanced Formatting

### Project Subheadings
```markdown
***Project Name: Description***
*   Bullet point 1
*   Bullet point 2
```

### Section Separators
```markdown
---
```
Use horizontal rules between different jobs for visual separation.

### Bullet Points
```markdown
*   Standard bullet point
*   Another bullet point
```

### Emphasis
```markdown
**Bold text**
*Italic text*
_Italic text_ (alternative)
```

## Template Compatibility

### AltaCV Template Requirements
- **Job titles**: Must be in first parameter of `\cvevent`
- **Company names**: Must be in second parameter for red styling
- **Dates**: Must be in third parameter for italic styling
- **Location**: Fourth parameter (usually empty for this template)

### Color Mapping
- **Job titles**: Bold, dark red (`DarkPastelRed`)
- **Company names**: Red (`PastelRed`) - **This is why the colon is critical**
- **Dates**: Italic, light gray (`LightGrey`)
- **Body text**: Light gray (`LightGrey`)

## Validation Checklist

Before converting to LaTeX, verify:

- [ ] All job titles are bold (`**Title**`)
- [ ] All company names have colons before them (`: Company`)
- [ ] All dates are italic (`_Date Range_`)
- [ ] Company and dates are on the same line
- [ ] No extra spaces around colons
- [ ] Consistent formatting across all entries
- [ ] Proper section separators (`---`)

## Troubleshooting

### Company Names Not Red
**Problem**: Company names appear in default color instead of red
**Solution**: Check that colons are present before company names

### LaTeX Compilation Error
**Problem**: `\cvevent` command fails
**Solution**: Verify the Markdown structure matches the expected format

### Missing Company Names
**Problem**: Company names don't appear in LaTeX output
**Solution**: Ensure company names are on the line immediately after the colon

### Date Formatting Issues
**Problem**: Dates don't appear italic
**Solution**: Wrap dates in underscores: `_Date Range_`

## Best Practices

1. **Consistency**: Use the same format for all job entries
2. **Testing**: Always test with a small section first
3. **Validation**: Check the LaTeX output after each major change
4. **Backup**: Keep a working version before making changes
5. **Documentation**: Comment complex formatting decisions

## Example Conversion Script

If you need to automate the conversion, here's the pattern:

```bash
# Convert Markdown to LaTeX (basic)
pandoc resume.md -t latex -o resume.tex

# Then manually update the \cvevent commands to match the Definition List format
```

**Note**: Automated conversion may not preserve the exact Definition List format, so manual verification is recommended.
