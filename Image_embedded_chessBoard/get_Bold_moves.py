import fitz
import os

def extract_images_from_pdf(pdf_document,page_num, output_folder, puzzle_number, save_first_image=True):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # # Open the PDF file
    # pdf_document = fitz.open(pdf_path)

    # # Iterate through each page
    # for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    image_list = page.get_images(full=True)

    # Print the number of images found on this page
    print(f"Found {len(image_list)} images on page {page_num}")

    if not image_list:
        print("Images didn't found.")
    # Determine the image to save based on the parameter
    img_index = 0 if save_first_image else -1
    img = image_list[img_index]
    xref = img[0]
    base_image = pdf_document.extract_image(xref)
    image_bytes = base_image["image"]

    # Determine the image format
    image_ext = base_image["ext"]

    # Save the image
    image_filename = f"{puzzle_number}_{page_num+1}_{img_index+1}.{image_ext}"
    image_path = os.path.join(output_folder, image_filename)

    with open(image_path, "wb") as image_file:
        image_file.write(image_bytes)

    print(f"Image {img_index+1} on page {page_num+1} saved as {image_filename}")

    print("Image extraction complete.")

def extract_images_above_text(pdf_document, page_num, output_folder, line_y1, puzzle_number,save_last_image=False):
    page = pdf_document[page_num]
    image_list = page.get_images(full=True)
    if save_last_image:
        img_index = -1
        img = image_list[img_index]
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        # Determine the image format
        image_ext = base_image["ext"]

        # Save the image
        image_filename = f"{puzzle_number}_{page_num+1}_{img_index+1}.{image_ext}"
        image_path = os.path.join(output_folder, image_filename)

        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return 1

    else:
        for img in (image_list):
            xref = img[0]
        # Print the image tuple to understand its structure
            print(f"Image tuple: {img}")
            # # print(xref)
            # img_info_list = page.get_image_info(xref)
            # img_info = img_info_list[0]  # Extract the first element from the list
            # img_bbox = img_info['bbox']
            # print(img_bbox)
        # Find the image just above the text line
        for img in reversed(image_list):
            xref = img[0]
            # print(xref)
            img_info_list = page.get_image_info(xref)
            img_info = img_info_list[0]  # Extract the first element from the list
            img_bbox = img_info['bbox']
            if img_bbox[3] < line_y1:  # Check if the bottom of the image is above the text line
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                # Save the image
                image_filename = f"{puzzle_number}_{page_num+1}_.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                print(f"Image on page {page_num+1} saved as {image_filename}")
                return 0
        # If no image found above the text line, extract the last image from the previous page
        if page_num > 0:
            previous_page_num = page_num - 1
            return extract_images_above_text(pdf_document, previous_page_num, output_folder,line_y1, puzzle_number, save_last_image=True)
            
    print("Error: No image found above the text line.")
    return -1000

def parse_pdf_to_text(pdf_path, output_file):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""
    puzzle_page =""
    puzzle_Number = 0
    with open(output_file, "w", encoding="utf-8") as f:
        # # Initial page number
        # initial_num = 1
        puzzle_details = 0
        previous = False
        given_gap = False
        Commenting = False
        # Iterate through each page
        for page_num in range(len(doc)):
            # Get the page
            # if page_num==30:
            #     pdb.set_trace()
            page = doc.load_page(page_num)
            page_height = page.rect.height  # Get the height of the page
            top_third = page_height // 3.5 
            # Extract blocks from the page
            blocks = page.get_text("dict")["blocks"]

            for b in blocks:
                if "lines" in b:
                    for i, l in enumerate(b["lines"]):
                        line_y1 = l["bbox"][1]
                        if len(l["spans"]) ==  1:
                            for s in l["spans"]:
                                font = s["font"]
                                font = font.lower()
                                line = s["text"]
                                if line.strip().isdigit() :
                                    if "bold" in font:
                                        if Commenting:
                                            text += " }" + "\n"
                                            f.write(text)
                                            text = ""
                                            Commenting = False
                                        f.write("\n\n\n\n")
                                        f.write(line + "\n")
                                        puzzle_Number = line
                                        puzzle_details = 1
                                    elif puzzle_details == 2 :
                                        i == len(b["lines"]) - 1
                                        f.write(line + "\n")
                                        puzzle_details = 3
                                    
                                elif "bold" in font and puzzle_details==1:
                                    f.write(line + "\n")
                                    puzzle_details = 2
                                elif puzzle_details == 2:
                                    f.write(line + "\n")
                                    puzzle_details = 3
                                elif "italic" in font:
                                    f.write(text + "\n")
                                    text = ""
                                    f.write(line + "\n\n")
                                    puzzle_details = 0
                                    # print(type(ind))
                                    # print(type(page_num))
                                    ind = extract_images_above_text(doc,page_num, "extracted_images", line_y1, puzzle_number=puzzle_Number)
                                    puzzle_page += puzzle_Number+"\n"+ f"{page_num-ind}" + "\n" + line + "\n\n"
                                elif puzzle_details == 3:
                                    for s in l["spans"]:
                                        text += line
                                elif not "bold" in font:
                                    if not Commenting:
                                        if previous:
                                            text += "\n"
                                        text += "{ " + line
                                        Commenting = True
                                    else:
                                        text += line
                                    previous = False
                        elif puzzle_details == 3:
                            for s in l["spans"]:
                                line = s["text"]
                                font = s["font"] 
                                text += line
                        else:            
                            for s in l["spans"]:
                                line = s["text"]
                                font = s["font"]  
                                font = font.lower()                  
                                # Check if the font indicates special text (like bold for chess moves)
                                if "bold" in font:
                                    # Append the line to the text
                                    if Commenting:
                                        text += " }" + "\n"
                                        f.write(text)
                                        text = ""
                                        Commenting = False
                                    f.write(line)
                                    previous = True
                                elif font == "chess":
                                    if(previous):
                                        f.write(line)
                                    else:
                                        text += line
                                else:
                                    if not Commenting:
                                        if previous:
                                            text += "\n"
                                        text += "{ " + line
                                        Commenting = True
                                    else:
                                        text += line
                                    previous = False


    # # Write the extracted text to a file
    with open("puzzle_pages.txt", "w", encoding="utf-8") as f:
        f.write(puzzle_page)

# # Example usage
# pdf_path = "a.pdf"
# output_folder = "extracted_images"
# save_first_image = True  # Change to False to save the last image instead of the first
# extract_images_from_pdf(pdf_path, output_folder, save_first_image)


# Example usage
pdf_path = "75_Open_Middle_Game_Sol.pdf"
output_file = "Moves_text.txt"
parse_pdf_to_text(pdf_path, output_file)
