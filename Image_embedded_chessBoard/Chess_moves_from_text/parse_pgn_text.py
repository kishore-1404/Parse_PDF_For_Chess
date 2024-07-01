import re

def extract_pgn(text):
    # Split the text into lines
    lines = text.split("\n")

    # Initialize variables
    game_metadata = []
    moves = []
    comments = []

    # Define a regex pattern for moves
    move_pattern = re.compile(r'\d+\.\s*[a-zA-Z0-9+#=]+')

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # If the line is a move
        if move_pattern.search(line):
            # If there are comments, add them to the previous move if any move exists
            if comments and moves:
                moves[-1] += ' {' + ' '.join(comments) + '}'
                comments = []

            # Extract moves from the line
            move_text = move_pattern.findall(line)
            moves.extend(move_text)
        
        # If the line is a comment
        else:
            comments.append(line)

    # If there are leftover comments, add them to the last move if any move exists
    if comments and moves:
        moves[-1] += ' {' + ' '.join(comments) + '}'

    # Compile the PGN
    pgn = '\n'.join(game_metadata) + '\n\n' + ' '.join(moves) + '\n'

    return pgn

def main():
    # Read the text from the file
    with open('Fun.txt', 'r') as file:
        text = file.read()

    # Extract the PGN
    pgn = extract_pgn(text)

    # Write the PGN to a new file
    with open('output.pgn', 'w') as file:
        file.write(pgn)

if __name__ == "__main__":
    main()
