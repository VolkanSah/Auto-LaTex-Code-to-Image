# LaTeX-to-Image Conversion

This repository contains a small helper script and GitHub Actions workflow that scans **all Markdown files** for LaTeX formulas. It supports these three patterns by default:

```
r'\[ *(.*?) *\]'    # [ formula ]
r'\\\[(.*?)\\\]'    # \[ formula \]
r'\$\$(.*?)\$\$'    # $$ formula $$
```

Whenever a formula is found, the script generates a **high-resolution PNG** and places it in an `assets` folder. It then replaces the LaTeX snippet in your `.md` file with a Markdown image link (`![LaTeX Formel](assets/xxx.png)`) plus a code fence displaying the original LaTeX code for reference.

## How to Use

1. **Manual Trigger**:  
   - Go to the [Actions](../../actions) tab in your repository.  
   - Select the **LaTeX-to-Image** workflow, then click **Run workflow**.

2. **Automatic Trigger** (optional):  
   - If you have a file like `latex_to_image.yml_auto` that triggers on `push`, the conversion runs automatically each time you push changes.  
   - Note that large/complex LaTeX or frequent push events may slow down your CI.




