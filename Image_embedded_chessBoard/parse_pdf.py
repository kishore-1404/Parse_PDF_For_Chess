import fitz

def parse_pdf_to_text(pdf_path, output_file):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Initial page number
    initial_num = 1

    # Iterate through each page
    for page_num in range(len(doc)):
        # Get the page
        page = doc.load_page(page_num)
        # Extract text from the page
        page_text = page.get_text()

        # Process text on each page
        for line in page_text.split("\n"):
            # Check if the line contains only digits
            if line.strip().isdigit():
                # If the line matches the expected sequence
                if int(line.strip()) == initial_num:
                    # Increment the initial number
                    initial_num += 1
                    # Append the line to the text
                    text += "\n\n\n" + line + "\n"
            else:
                # Append the line to the text
                text += line + "\n"

    # Write the extracted text to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

# Example usage
pdf_path = "75_Open_Middle_Game_Sol.pdf"
output_file = "parsed_text.txt"
parse_pdf_to_text(pdf_path, output_file)
