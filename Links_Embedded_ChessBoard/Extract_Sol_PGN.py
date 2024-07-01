import fitz  # PyMuPDF
from pprint import pprint

def extract_text_with_formatting(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text not in ["", "\n","Solutions for Deadly Puzzles"]:
                            text_data.append({
                                "text": text,
                                "font": span["font"],
                                "bold": "Bold" in span["font"],
                                "italic": "Italic" in span["font"]
                            })
    return text_data

def parse_puzzle_data(text_data):
    puzzles = []
    current_puzzle = {}
    current_comments = []
    previous_item = None

    for item in text_data:
        text = item["text"]
        if text == "back":
            if current_comments:
                current_puzzle["comments"].append(" ".join(current_comments))
            puzzles.append(current_puzzle)
            current_puzzle = {}
            current_comments = []
            previous_item = None
        else:
            if "White to play" in text or "Black to play" in text:
                current_puzzle["whom_to_play"] = text
            elif item["italic"]:
                current_puzzle["tournament"] = text
            elif previous_item and previous_item["text"] in ["White to play", "Black to play"]:
                if item["bold"]:
                    current_puzzle["players"] = text
            elif item["bold"]:
                if "moves" not in current_puzzle:
                    current_puzzle["moves"] = []
                if current_comments:
                    current_puzzle["comments"].append(" ".join(current_comments))
                    current_comments = []
                current_puzzle["moves"].append(text)
            else:
                if "comments" not in current_puzzle:
                    current_puzzle["comments"] = []
                current_comments.append(text)
        
        previous_item = item

    return puzzles

def format_puzzle_as_pgn(puzzle):
    pgn = []
    pgn.append(f"[Event \"{puzzle.get('tournament', '')}\"]")
    # pgn.append(f"[Site \"?\"]")
    # pgn.append(f"[Date \"????.??.??\"]")
    # pgn.append(f"[Round \"?\"]")
    # pgn.append(f"[White \"?\"]")
    # pgn.append(f"[Black \"?\"]")
    # pgn.append(f"[Result \"*\"]")

    if puzzle.get('whom_to_play'):
        pgn.append(f"; {puzzle['whom_to_play']}")

    players = puzzle['players'].split(" – ")
    atrribute = players[0].strip()  # Remove leading/trailing spaces
    attrib = atrribute.split(")")
    puzzle_number = attrib[0].strip()
    white_player = attrib[1].strip()
    black_player = players[1].strip()
    
    pgn.append(f"[Puzzle \"{puzzle_number}\"]") # Add PGN tag for puzzle number
    if puzzle.get('players'):
        # Add PGN tags for White and Black players
        pgn.append(f"[White \"{white_player}\"]")
        pgn.append(f"[Black \"{black_player}\"]")

    moves = puzzle.get('moves', [])
    comments = puzzle.get('comments', [])
    
    move_text = []
    for i in range(len(moves)):
        move = moves[i]
        comment = comments[i] if i < len(comments) else ""
        move_text.append(f"{move} {{ {comment} }}")

    pgn.append(" ".join(move_text))
    pgn.append("*")  # Add a final result marker
    
    return "\n".join(pgn)

def write_puzzles_to_file(puzzles, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, puzzle in enumerate(puzzles, 1):
            file.write(f"; Puzzle {i}\n")
            file.write(format_puzzle_as_pgn(puzzle))
            file.write("\n\n")

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'DeadlyPuzzlesSol.pdf'
text_data = extract_text_with_formatting(pdf_path)
puzzles = parse_puzzle_data(text_data)
# pprint(puzzles)

# Replace 'output_file.pgn' with the desired output text file path
output_file = 'Extracted_Sol.pgn'
write_puzzles_to_file(puzzles, output_file)
