import os
import re
import hashlib
import subprocess
from pathlib import Path

def extract_latex_blocks(markdown_text):
    """
    Extrahiert LaTeX-Blöcke aus Markdown-Text.
    Unterstützt verschiedene Blockformate.
    """
    # Regex für verschiedene LaTeX-Block-Formate
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
    """
    Erzeugt einen sicheren Dateinamen aus LaTeX-Code.
    """
    # Entferne problematische Zeichen und kürze
    clean_latex = re.sub(r'[^\w\-]', '_', latex_code.strip())
    clean_latex = clean_latex[:30]  # Länge begrenzen
    hash_part = hashlib.md5(latex_code.encode()).hexdigest()[:8]
    return f"latex_{clean_latex}_{hash_part}.png"

def latex_to_image(latex_code, output_path):
    """
    Konvertiert LaTeX-Code zu PNG-Bild.
    """
    os.makedirs("assets", exist_ok=True)
    
    # LaTeX-Dokument mit vollständigem Kontext
    latex_document = f"""
    \\documentclass[preview]{{standalone}}
    \\usepackage{{amsmath}}
    \\usepackage{{amssymb}}
    \\begin{{document}}
    \\Large
    $${latex_code}$$
    \\end{{document}}
    """
    
    # Temporäre Datei schreiben
    with open("temp.tex", "w", encoding="utf-8") as f:
        f.write(latex_document)
    
    try:
        # PDF generieren
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], 
                       capture_output=True, text=True, check=True)
        
        # PDF zu PNG konvertieren
        subprocess.run(["convert", "-density", "300", "temp.pdf", 
                        "-quality", "90", "-trim", output_path], 
                       capture_output=True, text=True, check=True)
        
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
    """
    Aktualisiert Markdown-Datei mit LaTeX-Bildern.
    """
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
    """
    Hauptfunktion zur Verarbeitung aller Markdown-Dateien.
    """
    md_files = list(Path(".").rglob("*.md"))
    print(f"Gefundene Markdown-Dateien: {len(md_files)}")
    
    for md_file in md_files:
        print(f"Verarbeite: {md_file}")
        update_markdown(md_file)

if __name__ == "__main__":
    main()
