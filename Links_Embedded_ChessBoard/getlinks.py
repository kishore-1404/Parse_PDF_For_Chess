import pdfx
import fitz  # PyMuPDF

def extract_urls_from_pdf(pdf_path, write_file):
    # Initialize pdfx object to extract URLs
    pdf = pdfx.PDFx(pdf_path)
    extracted_urls = pdf.get_references_as_dict()
    
    # Initialize PyMuPDF object to extract page numbers
    doc = fitz.open(pdf_path)

    url_page_pairs = []

    # Iterate through pages and extract links with page numbers
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        links = page.get_links()

        for link in links:
            uri = link.get('uri')
            if uri:
                url_page_pairs.append((page_num + 1, uri))

    # Sort the URL-page pairs based on page numbers
    sorted_url_page_pairs = sorted(url_page_pairs, key=lambda x: x[0])

    # Write sorted URLs to a text file
    with open(write_file, "w") as f:
        for page, url in sorted_url_page_pairs:
            f.write(f"{url}\n")

# Example usage
pdf_path = "DeadlyPuzzlesSol.pdf"  # Replace with your actual PDF path
write_file = "DeadlyPuzzlesSol.txt"
extract_urls_from_pdf(pdf_path, write_file)

print(f"URLs extracted from {pdf_path} have been written to {write_file}")
