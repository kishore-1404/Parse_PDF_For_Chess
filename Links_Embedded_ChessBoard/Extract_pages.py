import fitz  # PyMuPDF

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    """
    Extract pages from input_pdf and save them to output_pdf.
    
    Parameters:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to the output PDF file where extracted pages will be saved.
        start_page (int): Page number to start extraction (1-based index).
        end_page (int): Page number to end extraction (inclusive).
    """
    doc = fitz.open(input_pdf)
    output_doc = fitz.open()
    
    for page_num in range(start_page - 1, min(end_page, len(doc))):
        output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    output_doc.save(output_pdf)
    output_doc.close()
    doc.close()

# Example usage
input_pdf = "e.pdf"
output_pdf = "DeadlyPuzzles.pdf"
start_page = 1973
end_page = 1998
extract_pages(input_pdf, output_pdf, start_page, end_page )

print(f"Pages {start_page} to {end_page} have been extracted and saved to {output_pdf}")