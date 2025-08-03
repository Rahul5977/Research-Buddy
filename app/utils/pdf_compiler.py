# In app/utils/pdf_compiler.py
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

def compile_booklet_from_data(job_id: str, summary: str, citations: str, tables: list, images: list) -> str:
    """Compiles a PDF booklet from data using a LaTeX template."""

    output_dir = f"outputs/{job_id}"
    os.makedirs(output_dir, exist_ok=True)

    # Set up Jinja2 to load the LaTeX template
    # The 'templates' folder should be in your project root
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('booklet_template_v2.tex') # Use a new template version

    # Render the template with the data, including the new lists
    latex_content = template.render(
        summary=summary,
        citations=citations,
        tables=tables,
        images=images
    )

    tex_path = os.path.join(output_dir, "booklet.tex")
    pdf_path = os.path.join(output_dir, "booklet.pdf")

    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    # Compile LaTeX to PDF
    try:
        # We run it twice to ensure table of contents and references are correct
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
                check=True,
                capture_output=True,
                text=True
            )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        error_message = f"pdflatex compilation failed. Ensure a TeX distribution (like MiKTeX) is installed. Error: {e}"
        print(error_message)
        raise RuntimeError(error_message)

    return pdf_path