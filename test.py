import os
from pathlib import Path
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Title, NarrativeText, Image, Table

def extract_elements_from_pdf(pdf_path: str, output_dir: str = "output"):
    """
    Parses a PDF using the 'unstructured' library to extract text, tables, and images.
    
    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where extracted images will be saved.

    Returns:
        dict: A dictionary containing the extracted title, abstract, full text,
              a list of extracted tables (as HTML), and a list of image summaries.
    """
    print(f"Extracting elements from PDF: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)

    try:
        
        elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",
            extract_images_in_pdf=True,
            extract_image_block_output_dir=output_dir,
        )
    except Exception as e:
        print(f"Hi-res strategy failed with error: {e}. Falling back to fast strategy.")
        elements = partition_pdf(filename=pdf_path, strategy="fast")
    
    title = "Title Not Found"
    abstract = "Abstract Not Found"
    full_text_parts = []
    tables_html = []
    image_summaries = []

    found_title = False
    found_abstract = False

    for el in elements:
        
        if isinstance(el, Title):
            title = el.text
            found_title = True
            full_text_parts.append(el.text)

        elif isinstance(el, NarrativeText):
            if found_title and not found_abstract:
                if len(el.text.split()) > 30:
                    abstract = el.text
                    found_abstract = True
            full_text_parts.append(el.text)

        elif isinstance(el, Table):
            # For tables, the HTML representation is often more useful
            if el.metadata.text_as_html:
                tables_html.append(el.metadata.text_as_html)
            full_text_parts.append(el.text)

        elif isinstance(el, Image):
            image_summary = f"Image found. Caption: '{el.text}'"
            image_summaries.append(image_summary)
            full_text_parts.append(f"[Image: {el.text}]")

    full_text = "\n\n".join(full_text_parts)
    
    return {
        "title": title,
        "abstract": abstract,
        "full_text": full_text,
        "tables_as_html": tables_html,
        "image_summaries": image_summaries
    }
if __name__ == "__main__":
    pdf_file = "Paper1.pdf"
    
    if not Path(pdf_file).exists():
        print(f"Error: The file '{pdf_file}' was not found. Please place it in the same directory as the script.")
    else:
        extracted_data = extract_elements_from_pdf(pdf_file)

        print("\n" + "="*50)
        print("          EXTRACTION COMPLETE")
        print("="*50 + "\n")
        
        print(f"## TITLE ##\n{extracted_data['title']}\n")
        print(f"## ABSTRACT ##\n{extracted_data['abstract']}\n")
        
        print("## IMAGES FOUND ##")
        if extracted_data['image_summaries']:
            for summary in extracted_data['image_summaries']:
                print(f"- {summary}")
            print(f"\nNote: Actual image files have been saved in the '{'output'}' directory.\n")
        else:
            print("No images found.\n")

        print("## TABLES FOUND (as HTML) ##")
        if extracted_data['tables_as_html']:
            for i, table_html in enumerate(extracted_data['tables_as_html']):
                print(f"\n--- Table {i+1} ---\n{table_html}\n")
        else:
            print("No tables found.\n")