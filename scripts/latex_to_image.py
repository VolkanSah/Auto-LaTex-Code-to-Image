import os
import re
import subprocess
from pathlib import Path

def extract_latex_blocks(markdown_text):
    """Extrahiert LaTeX-Blöcke aus Markdown-Text."""
    patterns = [r'\[ *(.*?) *\]']
    return re.findall(patterns[0], markdown_text, re.DOTALL)

def generate_image_filename(markdown_file, index):
    """Generiert eindeutigen Dateinamen."""
    base_name = Path(markdown_file).stem.replace('-', '_')
    return f"latex_code_{base_name}_{index+1}.png"

def latex_to_image(latex_code, output_path):
    """Konvertiert LaTeX zu Bild mit weißem Hintergrund."""
    os.makedirs("assets", exist_ok=True)
    
    latex_document = f"""
    \\documentclass[preview]{{standalone}}
    \\usepackage{{amsmath}}
    \\usepackage{{color}}
    \\pagecolor{{white}}
    \\begin{{document}}
    \\Large
    $${latex_code}$$
    \\end{{document}}
    """
    
    with open("temp.tex", "w", encoding="utf-8") as f:
        f.write(latex_document)
    
    try:
        # PDF mit vollem Rand generieren
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], 
                       capture_output=True, text=True, check=True)
        
        # PDF zu PNG konvertieren mit weißem Hintergrund
        subprocess.run(["convert", "-density", "300", "temp.pdf", 
                        "-quality", "90", 
                        "-background", "white", 
                        "-alpha", "remove", 
                        "-bordercolor", "white", 
                        "-border", "20", 
                        output_path], 
                       capture_output=True, text=True, check=True)
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e}")
        return False
    
    finally:
        for ext in [".tex", ".pdf", ".log", ".aux"]:
            temp_file = f"temp{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)

def update_markdown(markdown_file):
    """Aktualisiert Markdown-Datei mit LaTeX-Bildern."""
    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    latex_blocks = extract_latex_blocks(content)
    
    for index, latex_code in enumerate(latex_blocks):
        image_filename = generate_image_filename(markdown_file, index)
        image_path = os.path.join("assets", image_filename)
        
        if latex_to_image(latex_code, image_path):
            replacement = (
                f"![{latex_code}](assets/{image_filename})\n\n"
                f"```latex\n{latex_code}\n```"
            )
            content = content.replace(f"[ {latex_code} ]", replacement)
    
    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    """Verarbeitet alle Markdown-Dateien."""
    md_files = list(Path(".").rglob("*.md"))
    print(f"Gefundene Markdown-Dateien: {len(md_files)}")
    
    for md_file in md_files:
        print(f"Verarbeite: {md_file}")
        update_markdown(md_file)

if __name__ == "__main__":
    main()
