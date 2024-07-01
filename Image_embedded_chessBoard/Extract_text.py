import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_txt_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("text")
    
    with open(output_txt_path, 'w', encoding='utf-8') as file:
        file.write(text)

pdf_path = 'wood_easy.pdf'
output_txt_path = 'wood_easy_to_text.txt'
extract_text_from_pdf(pdf_path, output_txt_path)
