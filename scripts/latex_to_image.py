# v2
import os
import re
import hashlib
import subprocess
from pathlib import Path

def extract_latex_blocks(markdown_text):
    # Unverändert
    patterns = [
        r'\[ *(.*?) *\]',   # [ Formel ]
        r'\\\[(.*?)\\\]',   # \[ Formel \]
        r'\$\$(.*?)\$\$'    # $$ Formel $$
    ]
    
    latex_blocks = []
    for pattern in patterns:
        blocks = re.findall(pattern, markdown_text, re.DOTALL)
        latex_blocks.extend(blocks)
    
    return latex_blocks

def sanitize_filename(latex_code):
    # ÄNDERUNG: Einfachere Namensgebung
    clean_latex = re.sub(r'[^\w\-]', '_', latex_code.strip())
    clean_latex = clean_latex[:50]  # Längere Dateinamen erlauben
    return f"latex_{clean_latex}.png"

def latex_to_image(latex_code, output_path):
    os.makedirs("assets", exist_ok=True)
    
    # ÄNDERUNG: Angepasste LaTeX-Dokumentvorlage
    latex_document = f"""
    \\documentclass[preview]{{standalone}}
    \\usepackage{{amsmath}}
    \\usepackage{{amssymb}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage[T1]{{fontenc}}
    \\begin{{document}}
    \\normalsize  % Kleinere Standardschrift
    $${latex_code}$$
    \\end{{document}}
    """
    
    with open("temp.tex", "w", encoding="utf-8") as f:
        f.write(latex_document)
    
    try:
        # PDF generieren
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], 
                       capture_output=True, text=True, check=True)
        
        # ÄNDERUNG: Verbesserte PDF-zu-PNG-Konvertierung
        subprocess.run(["convert", 
            "-density", "200",  # Geringere Dichte
            "temp.pdf", 
            "-quality", "90", 
            "-background", "white",  # Weißer Hintergrund
            "-alpha", "remove",      # Transparenz entfernen
            "-bordercolor", "white", 
            "-border", "20",         # Etwas größerer Rand
            output_path
        ], capture_output=True, text=True, check=True)
        
        print(f"Bild erstellt: {output_path}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei Konvertierung: {e}")
        return False
    
    finally:
        # Temporäre Dateien löschen
        for ext in [".tex", ".pdf", ".log", ".aux"]:
            temp_file = f"temp{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)

def update_markdown(markdown_file):
    # Unverändert
    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    latex_blocks = extract_latex_blocks(content)
    
    for latex_code in latex_blocks:
        # Bildpfad generieren
        image_filename = sanitize_filename(latex_code)
        image_path = os.path.join("assets", image_filename)
        
        # LaTeX zu Bild konvertieren
        if latex_to_image(latex_code, image_path):
            # Markdown-Ersetzung
            replacement = (
                f"![LaTeX Formel]({image_path})\n\n"
                f"```latex\n{latex_code}\n```\n"
            )
            content = content.replace(f"[ {latex_code} ]", replacement)
    
    # Geänderte Datei speichern
    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Unverändert
    md_files = list(Path(".").rglob("*.md"))
    print(f"Gefundene Markdown-Dateien: {len(md_files)}")
    
    for md_file in md_files:
        print(f"Verarbeite: {md_file}")
        update_markdown(md_file)

if __name__ == "__main__":
    main()
