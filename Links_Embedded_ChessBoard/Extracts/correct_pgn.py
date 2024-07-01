import os
import re

def correct_pgn_formatting(pgn_content):
    """Fixes spaces between move notation and evaluation symbols."""
    pgn_content = re.sub(r'\s\+\–', '+–', pgn_content)
    pgn_content = re.sub(r'\s\–\+', '–+', pgn_content)
    pgn_content = re.sub(r'\s\+=', '+=', pgn_content)
    pgn_content = re.sub(r'\s=\+', '=+', pgn_content)

    return pgn_content

def process_pgn_file(input_file, output_file):
    """Processes a PGN file, correcting formatting and writing to output."""
    with open(input_file, 'r', encoding='utf-8') as file:
        pgn_content = file.read()

    corrected_pgn_content = correct_pgn_formatting(pgn_content)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(corrected_pgn_content)

def process_all_png_files(current_directory, output_directory="Puzzles"):
    """Iterates over all PNG files in the current directory, processes them,
       and writes outputs to the specified output directory (default: Puzzles)."""

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)  # Handle existing directory gracefully

    for filename in os.listdir(current_directory):
        if filename.lower().endswith(".pgn"):  # Case-insensitive PNG extension check
            input_file = os.path.join(current_directory, filename)
            # Construct the output filename within the Puzzles directory
            output_filename = os.path.join(output_directory, filename)
            process_pgn_file(input_file, output_filename)

if __name__ == "__main__":
    current_directory = os.getcwd()  # Get the current working directory
    process_all_png_files(current_directory)

    print("PNG files processed and corrected PGN files written to Puzzles directory.")
