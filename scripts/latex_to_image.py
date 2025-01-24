import os
import re
import subprocess
from pathlib import Path

def extract_bracketed_latex(markdown_text):
    """
    Search for bracketed LaTeX blocks in the Markdown text.
    Example: [ \text{DumpIndex} = \frac{Noise - Effort}{Context + Details} ]

    Returns a list of strings, each being the content inside [ ... ].
    """
    # Regex Explanation:
    # - \[\s* matches '[' followed by optional whitespace
    # - (.*?) is a lazy capturing group for anything (including newlines, thanks to re.DOTALL)
    # - \s*\] matches optional whitespace plus the closing bracket ']'
    pattern = re.compile(r'\[\s*(.*?)\s*\]', re.DOTALL)
    blocks = pattern.findall(markdown_text)
    print(f"DEBUG: Found {len(blocks)} bracketed block(s).")
    return blocks

def latex_to_image(latex_code, output_path):
    """
    Takes a LaTeX snippet (latex_code) and compiles it to a PNG (output_path) using
    LaTeX + dvipng.

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

def replace_brackets_with_images(markdown_text, bracketed_blocks, image_paths):
    """
    Replaces each bracketed LaTeX block (e.g., [ \frac{a}{b} ]) with
    the corresponding ![LaTeX Image](path) in the Markdown text.

    NOTE: The replacement pattern must match EXACTLY the bracket style
    in your Markdown. For example, [ \frac{a}{b} ] with spaces or
    [\frac{a}{b}] with no spaces.
    """
    updated_text = markdown_text
    for block_content, image_path in zip(bracketed_blocks, image_paths):
        # We assume the original text is: [ block_content ]
        # with exactly one space after '[' and one before ']'
        original = f"[ {block_content} ]"
        # If your usage is different, adjust the string or use regex replace
        updated_text = updated_text.replace(original, f"![LaTeX Image]({image_path})")

    return updated_text

def process_markdown_file(markdown_file):
    """
    Processes a single Markdown file:
      - Extract bracketed LaTeX blocks
      - For each block, compile to PNG
      - Replace the bracketed text with an image link
      - Write the updated Markdown back
    """
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 1) Extract bracketed blocks
    bracketed_blocks = extract_bracketed_latex(markdown_text)
    if not bracketed_blocks:
        return  # No bracketed LaTeX found, no changes needed

    # 2) Convert each block to an image
    image_paths = []
    for i, block in enumerate(bracketed_blocks):
        # e.g. "assets/latex_0.png", "assets/latex_1.png"
        image_path = f"assets/latex_{i}.png"
        success = latex_to_image(block, image_path)
        if not success:
            print(f"Failed to convert block: {block}")
            continue
        image_paths.append(image_path)

    # 3) Replace bracketed LaTeX with ![LaTeX Image](...)
    if image_paths:
        new_markdown_text = replace_brackets_with_images(markdown_text, bracketed_blocks, image_paths)
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
