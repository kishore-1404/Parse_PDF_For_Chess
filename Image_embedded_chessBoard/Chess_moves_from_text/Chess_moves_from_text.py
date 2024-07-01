import re

def is_chess_move_line(line):
    # Regex pattern for chess moves
    chess_move_pattern = re.compile(
        r'\b([KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](=[QRBN])?|O-O(-O)?|[a-h][1-8]|[KQRBN]?[a-h][1-8]\+?|[KQRBN]?[a-h][1-8]=[QRBN]|0-0-0|0-0|x[a-h][1-8])\b'
    )

    # Find all matches
    matches = chess_move_pattern.findall(line)

    # Check if the entire line contains only chess moves and/or move numbers
    if matches:
        # Removing all non-move parts from the line
        stripped_line = chess_move_pattern.sub('', line).strip()
        if not stripped_line or stripped_line.isdigit() or stripped_line == "...":
            return True
    return False

def identify_chess_move_lines(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            if is_chess_move_line(line.strip()):
                f.write(line)

# Example usage
input_file = "parsed_text.txt"
output_file = "chess_moves.txt"
identify_chess_move_lines(input_file, output_file)
