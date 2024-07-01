import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)

        # Print the number of images found on this page
        print(f"Found {len(image_list)} images on page {page_num}")

        # Iterate through the images
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Determine the image format
            image_ext = base_image["ext"]

            # Save the image
            image_filename = f"{page_num+1}_{img_index+1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            print(f"Image {img_index+1} on page {page_num+1} saved as {image_filename}")

    print("Image extraction complete.")

# Example usage
pdf_path = "wood_easy.pdf"
output_folder = "extracted_images"
extract_images_from_pdf(pdf_path, output_folder)
