import os
import re
import hashlib
import subprocess
from pathlib import Path

def extract_bracketed_latex(markdown_text):
    """
    Search for bracketed LaTeX blocks in the Markdown text.
    Returns list of tuples: (original_match, latex_content)
    """
    pattern = re.compile(r'(\[ *([^\]]+) *\])', re.DOTALL)
    blocks = pattern.findall(markdown_text)
    print(f"DEBUG: Found {len(blocks)} bracketed block(s).")
    return blocks

def sanitize_filename(latex_code):
    """
    Create a clean, unique filename from LaTeX code.
    Uses a hash to ensure unique filenames and avoid problematic characters.
    """
    # Remove whitespace and create a hash
    clean_latex = latex_code.replace(' ', '_').replace('\\', '_')
    hash_part = hashlib.md5(latex_code.encode()).hexdigest()[:8]
    return f"latex_{clean_latex[:20]}_{hash_part}.png"

def latex_to_image(latex_code, output_path):
    """
    Compiles LaTeX snippet to PNG using LaTeX + dvipng.
    Returns True on success, False on error.
    """
    # Ensure the "assets" directory exists
    os.makedirs("assets", exist_ok=True)

    # Prepare a minimal LaTeX document
    latex_document = f"""
    \\documentclass{{standalone}}
    \\usepackage{{amsmath}}
    \\begin{{document}}
    {latex_code}
    \\end{{document}}
    """
    # Write the LaTeX to a temporary .tex file
    with open("temp.tex", "w", encoding="utf-8") as f:
        f.write(latex_document)

    # Compile the .tex file to a .dvi
    result_latex = subprocess.run(["latex", "temp.tex"], capture_output=True, text=True)
    if result_latex.returncode != 0:
        print("ERROR: latex compilation failed.")
        print("STDOUT:", result_latex.stdout)
        print("STDERR:", result_latex.stderr)
        return False

    # Convert the .dvi file to a PNG
    result_dvipng = subprocess.run(["dvipng", "temp.dvi", "-o", output_path], capture_output=True, text=True)
    if result_dvipng.returncode != 0:
        print("ERROR: dvipng conversion failed.")
        print("STDOUT:", result_dvipng.stdout)
        print("STDERR:", result_dvipng.stderr)
        return False

    # Clean up temp files
    for tmp_file in ["temp.tex", "temp.dvi", "temp.log", "temp.aux"]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

    print(f"DEBUG: Created image '{output_path}' from LaTeX snippet.")
    return True

def replace_and_preserve_latex(markdown_text, latex_blocks, image_paths):
    """
    Replace bracketed LaTeX while preserving the original text.
    """
    updated_text = markdown_text
    for (original_match, block_content), image_path in zip(latex_blocks, image_paths):
        # Insert image link before the original LaTeX block
        replacement = f"![LaTeX Image]({image_path})\n\n{original_match}"
        updated_text = updated_text.replace(original_match, replacement)

    return updated_text

def process_markdown_file(markdown_file):
    """
    Process a single Markdown file to convert LaTeX to images.
    """
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 1) Extract bracketed blocks
    latex_blocks = extract_bracketed_latex(markdown_text)
    if not latex_blocks:
        return  # No bracketed LaTeX found, no changes needed

    # 2) Convert each block to an image
    image_paths = []
    for block in latex_blocks:
        latex_code = block[1]  # The actual LaTeX content
        # Generate a descriptive filename
        image_filename = sanitize_filename(latex_code)
        image_path = os.path.join("assets", image_filename)
        
        success = latex_to_image(latex_code, image_path)
        if not success:
            print(f"Failed to convert block: {latex_code}")
            continue
        image_paths.append(image_path)

    # 3) Replace and preserve LaTeX blocks
    if image_paths:
        new_markdown_text = replace_and_preserve_latex(markdown_text, latex_blocks, image_paths)
        
        # 4) Overwrite the original file with the updated content
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(new_markdown_text)
        print(f"Updated file: {markdown_file}")

def main():
    """
    Main entry point: search for all .md files in the repo,
    then process each one to convert bracketed LaTeX.
    """
    md_files = list(Path(".").rglob("*.md"))
    print(f"Found {len(md_files)} Markdown file(s).")

    for md_file in md_files:
        print(f"Processing: {md_file}")
        process_markdown_file(md_file)

if __name__ == "__main__":
    main()
