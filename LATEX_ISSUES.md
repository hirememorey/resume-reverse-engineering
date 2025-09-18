# LaTeX Compilation Issues & Solutions

## Critical Issue: Font Engine Mismatch

### Problem
The template uses `\setmainfont{Helvetica}` which requires XeLaTeX, but the system defaults to pdfLaTeX.

### Error Messages
```
! Undefined control sequence.
l.10 \setmainfont
                 {Helvetica}
```

### Root Cause
- `\setmainfont` is a XeLaTeX/LuaLaTeX command
- pdfLaTeX doesn't recognize this command
- The template is designed for modern LaTeX engines

### Solution
**Always use XeLaTeX for compilation:**

```bash
# Find XeLaTeX path
which xelatex
# Output: /Library/TeX/texbin/xelatex

# Compile with full path
/Library/TeX/texbin/xelatex harris_resume.tex

# Or if in PATH
xelatex harris_resume.tex
```

### Why XeLaTeX?
1. **Font Support**: Handles system fonts (Helvetica) natively
2. **Unicode**: Better Unicode character support
3. **Template Compatibility**: AltaCV template designed for XeLaTeX
4. **FontSpec**: Required for `\setmainfont` commands

## Alternative Compilation Methods

### Method 1: Direct XeLaTeX (Recommended)
```bash
xelatex harris_resume.tex
```

### Method 2: Using Pandoc with XeLaTeX
```bash
pandoc my-resume/resume.md -o output.pdf --pdf-engine=xelatex
```

### Method 3: LaTeX Workshop (VS Code)
Configure `settings.json`:
```json
{
    "latex-workshop.latex.tools": [
        {
            "name": "xelatex",
            "command": "xelatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "latex-workshop.latex.recipes": [
        {
            "name": "xelatex",
            "tools": ["xelatex"]
        }
    ]
}
```

## Common Compilation Errors

### Error 1: Missing Font
```
Missing character: There is no (U+0020) in font [SimpleIcons.otf]/OT!
```
**Solution**: This is a warning, not an error. The PDF will still generate correctly.

### Error 2: PDF/A Compliance Warning
```
Package pdfx Warning: Setting all color commands to rgb
```
**Solution**: This is expected behavior for PDF/A compliance. Colors will still work.

### Error 3: Missing XMP Data
```
** pdfx: No file harris_resume.xmpdata . Metadata will be incomplete!
```
**Solution**: Create `harris_resume.xmpdata` file or ignore (PDF will still generate).

## Font Configuration

### Current Font Setup
```latex
\setmainfont{Helvetica}
\setsansfont{Helvetica}
\renewcommand{\familydefault}{\sfdefault}
```

### Alternative Fonts (if Helvetica unavailable)
```latex
% Option 1: Arial
\setmainfont{Arial}
\setsansfont{Arial}

% Option 2: System default
\setmainfont{System Font}
\setsansfont{System Font}

% Option 3: Fallback to LaTeX fonts
% Comment out font commands and use:
\usepackage[rm]{roboto}
\usepackage[defaultsans]{lato}
```

## Template-Specific Issues

### AltaCV Class Requirements
- **Engine**: XeLaTeX or LuaLaTeX (not pdfLaTeX)
- **Fonts**: System fonts via FontSpec
- **Packages**: TikZ, Paracol, FontAwesome

### Color Definitions
```latex
\definecolor{PastelRed}{HTML}{8F0D0D}      % Company names
\definecolor{DarkPastelRed}{HTML}{450808}  % Headings
\definecolor{SlateGrey}{HTML}{2E2E2E}     % Emphasis
\definecolor{LightGrey}{HTML}{666666}     % Body text
```

## Debugging Tips

### 1. Check LaTeX Engine
```bash
# Check available engines
which pdflatex
which xelatex
which lualatex
```

### 2. Verify Font Availability
```bash
# List available fonts (macOS)
fc-list | grep -i helvetica
```

### 3. Test Minimal Document
Create `test.tex`:
```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Helvetica}
\begin{document}
Test document
\end{document}
```
Compile with `xelatex test.tex`

### 4. Check Log Files
- `harris_resume.log`: Detailed compilation log
- `harris_resume.aux`: Auxiliary information
- Look for "Error" or "Undefined" messages

## Performance Optimization

### Compilation Speed
- Use `-interaction=nonstopmode` for faster compilation
- Run twice to resolve cross-references
- Clean auxiliary files between major changes

### File Size
- Optimize images before including
- Use appropriate image formats (PNG for photos, SVG for graphics)
- Consider PDF compression settings

## Platform-Specific Notes

### macOS
- XeLaTeX typically available in TeX Live
- Fonts accessible via Font Book
- Path: `/Library/TeX/texbin/xelatex`

### Linux
- Install `texlive-xetex` package
- May need additional font packages
- Check font paths in `/etc/fonts/`

### Windows
- Use MiKTeX or TeX Live
- Ensure XeLaTeX is in PATH
- May need to install fonts separately
