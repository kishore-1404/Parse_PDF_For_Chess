import chess.pgn

def extract_puzzle_numbers_from_pgn(pgn_file):
    puzzles = set()
    with open(pgn_file, "r", encoding="utf-8") as file:
        while True:
            game = chess.pgn.read_game(file)
            if game is None:
                break
            main_node = game
            while main_node.variations:
                main_node = main_node.variations[0]
            if "Puzzle" in main_node.headers:
                puzzle_number = int(main_node.headers["Puzzle"])
                puzzles.add(puzzle_number)
    return puzzles

def find_missing_puzzles(puzzles):
    missing_puzzles = []
    for i in range(1, 1001):
        if i not in puzzles:
            missing_puzzles.append(i)
    return missing_puzzles

# Example usage:
pgn_file = "a.pgn"
puzzles = extract_puzzle_numbers_from_pgn(pgn_file)
missing_puzzles = find_missing_puzzles(puzzles)
if missing_puzzles:
    print("Missing puzzles:", missing_puzzles)
else:
    print("No missing puzzles.")
