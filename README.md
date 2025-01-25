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

## Example

Write LaTeX in Markdown between `$$ ... $$`, for instance:

```markdown
$$
\text{Komplexitätsindex} 
= \frac{\text{Systemkomplexität} \cdot \text{Variablen}}
       {\text{Verständlichkeit} + \text{Dokumentation}}
$$
```

After the workflow runs, your `.md` file is updated to reference a newly created PNG in `assets/`, along with a code block containing the original snippet.

### Before

```markdown
$$
\frac{a + b}{c}
$$
```

### After

```markdown
![LaTeX Formel](assets/latex___frac_a___b__c_.png)

```latex
\frac{a + b}{c}
```
```

## Note on Patterns

You can also use other formats:

- `[ \frac{a}{b} ]`
- `\[ \frac{a}{b} \]`

The script searches for all three expressions. You’re free to **remove** or **customize** them in the Python code to match your preferred syntax.

## Tips

- If your LaTeX uses special packages, ensure they are installed via `texlive-latex-extra` or whichever distribution is needed.  
- Large formulas or TikZ graphics might require additional packages (like `pgf`).  
- Adjust the **ImageMagick** `convert` settings (e.g., `-density`, `-quality`) in the script for finer control over output resolution.

---

That’s it! Enjoy automating your LaTeX-to-image conversions.

















### Test 1
I am testing, soon! 

This small helper has two funktions! scann al markdown files in folder and subfolders for latexCode and Forms like 
```
        r'\[ *(.*?) *\]',   # [ Formel ]
        r'\\\[(.*?)\\\]',   # \[ Formel \]
        r'\$\$(.*?)\$\$'    # $$ Formel $$
```

and creates an Assets Folder and stores wimages in high resolution in it.

you must start the workflow manually or use latex_to_image.yml_auto for automatic builds and after every pusch. its an bad idea! 

second. if Workflow ontime configurt you can use in the repo where this script runs 
 simple latex code between 

 ``` 
§§
\text{Komplexitätsindex} = \frac{\text{Systemkomplexität} \cdot \text{Variablen}}{\text{Verständlichkeit} + \text{Dokumentation}}
\
$$

 ``` 

# example output
$$
\text{Komplexitätsindex} = \frac{\text{Systemkomplexität} \cdot \text{Variablen}}{\text{Verständlichkeit} + \text{Dokumentation}}
\
$$



