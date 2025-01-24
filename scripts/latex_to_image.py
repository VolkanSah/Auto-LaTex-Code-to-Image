# Code by Github Copliot & Volkan Sah 2023-2025
# MIT Free for all. DONT SELL FREE CODE AND RESPECT CREDITS, OR YOU WILL PAY IN FUTURE FOR TOOLS LIKE THIS!
# OPENSOURCE 4 LIFE! 
import os
import re
import subprocess
from pathlib import Path

def extract_latex_blocks(markdown_text):
    # Regex to match LaTeX blocks
    latex_blocks = re.findall(r'\$\$(.*?)\$\$', markdown_text, re.DOTALL)
    return latex_blocks

def latex_to_image(latex_code, output_path):
    # Create a LaTeX file
    latex_document = f"""
    \\documentclass{{standalone}}
    \\usepackage{{amsmath}}
    \\begin{{document}}
    {latex_code}
    \\end{{document}}
    """
    with open("temp.tex", "w") as f:
        f.write(latex_document)

    # Compile LaTeX to DVI
    subprocess.run(["latex", "temp.tex"])

    # Convert DVI to PNG
    subprocess.run(["dvipng", "temp.dvi", "-o", output_path])

    # Clean up temporary files
    os.remove("temp.tex")
    os.remove("temp.dvi")
    os.remove("temp.log")
    os.remove("temp.aux")

def replace_latex_with_images(markdown_text, latex_blocks, image_paths):
    for latex, image_path in zip(latex_blocks, image_paths):
        markdown_text = markdown_text.replace(f"$${latex}$$", f"![LaTeX Image]({image_path})")
    return markdown_text

def process_markdown_file(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    latex_blocks = extract_latex_blocks(markdown_text)
    image_paths = []

    for i, latex in enumerate(latex_blocks):
        image_path = f"assets/latex_{i}.png"
        latex_to_image(latex, image_path)
        image_paths.append(image_path)

    new_markdown_text = replace_latex_with_images(markdown_text, latex_blocks, image_paths)

    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write(new_markdown_text)

def main():
    for markdown_file in Path(".").rglob("*.md"):
        process_markdown_file(markdown_file)

if __name__ == "__main__":
    main()
