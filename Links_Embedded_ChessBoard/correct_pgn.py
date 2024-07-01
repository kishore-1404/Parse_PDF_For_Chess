import re

def correct_pgn_formatting(pgn_content):
    # Fix spaces between move notation and evaluation symbols
    pgn_content = re.sub(r'\s\+\–', '+–', pgn_content)
    pgn_content = re.sub(r'\s\–\+', '–+', pgn_content)
    pgn_content = re.sub(r'\s\+=', '+=', pgn_content)
    pgn_content = re.sub(r'\s=\+', '=+', pgn_content)
    
    # Ensure proper spacing after move numbers
    pgn_content = re.sub(r'(\d+)\s+', r'\1. ', pgn_content)

    # Fix spacing around braces
    pgn_content = re.sub(r'\s*{\s*', ' { ', pgn_content)
    pgn_content = re.sub(r'\s*}\s*', ' } ', pgn_content)

    # Fix spacing around move numbers and moves
    pgn_content = re.sub(r'\s*\.\s*', '. ', pgn_content)

    return pgn_content

def process_pgn_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        pgn_content = file.read()
    
    corrected_pgn_content = correct_pgn_formatting(pgn_content)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(corrected_pgn_content)

# Usage example
input_file = 'input.pgn'  # Replace with your input PGN file path
output_file = 'corrected_output.pgn'  # Replace with your desired output PGN file path

process_pgn_file(input_file, output_file)
