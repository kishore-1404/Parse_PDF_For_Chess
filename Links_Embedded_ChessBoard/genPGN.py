def process_urls(input_file_path):
    """
    Process the URLs from the input file to extract and format FEN strings.
    
    Args:
    input_file_path (str): Path to the input text file containing URLs.

    Returns:
    list: List of formatted FEN strings.
    """
    # Open the input file and read the URLs
    with open(input_file_path, 'r') as file:
        urls = file.readlines()

    # Strip any leading/trailing whitespace from URLs and remove duplicates while preserving order
    seen = set()
    urls = [url.strip() for url in urls if url.strip() and not (url.strip() in seen or seen.add(url.strip()))]

    formatted_lines = []
    for url in urls:
        try:
            # Extract the FEN string from the URL
            fen = url.split('/analysis/')[1].strip()

            # Replace underscores with spaces in the FEN string
            fen = fen.replace('_', ' ')

            # Basic validation: check the number of fields in the FEN string
            if len(fen.split()) == 6:
                # Format the FEN string with the headers
                formatted_lines.append('[Variant "From Position"]')
                formatted_lines.append(f'[FEN "{fen}"]')
                formatted_lines.append('')  # Add a blank line for separation
            else:
                print(f"Invalid FEN string format in URL: {url}")
        except IndexError:
            print(f"Invalid URL format: {url}")

    return formatted_lines


def write_pgns_to_file(pgns, output_file_path):
    """
    Write the formatted PGNs to the output file.
    
    Args:
    pgns (list): List of formatted FEN strings.
    output_file_path (str): Path to the output text file.
    """
    with open(output_file_path, 'w') as file:
        for line in pgns:
            file.write(line + '\n')


# Example usage
input_file_path = 'DeadlyPuzzlesSol.txt'  # Replace with your actual text file containing URLs
output_file_path = 'DeadlyPuzzlesSolPGN.txt'

pgns = process_urls(input_file_path)
write_pgns_to_file(pgns, output_file_path)

print(f"PGNs have been written to {output_file_path}")
