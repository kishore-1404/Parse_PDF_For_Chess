import chess.pgn

def reorder_pgn(input_file, output_file):
    puzzles = {}
    with open(input_file, 'r', encoding="utf-8") as f:
        pgn = chess.pgn.read_game(f)
        while pgn is not None:
            puzzle_number = pgn.headers.get("Puzzle")
            if puzzle_number is not None:
                puzzles[puzzle_number] = pgn
            pgn = chess.pgn.read_game(f)
    with open(output_file, 'w', encoding="utf-8") as f:
        for puzzle_number in sorted(puzzles.keys(), key=lambda x: int(x)):
            f.write(str(puzzles[puzzle_number]) + "\n\n")


    # i = 1
    # for puzzle_number in sorted(puzzles.keys(), key=lambda x: int(x)):
    #     # print(puzzles[puzzle_number])
    #     if puzzles[puzzle_number].headers.get("Puzzle") != str(i):
    #         print(f"Missing puzzle {i} to {puzzles[puzzle_number].headers.get("Puzzle")}")
    #         # print(puzzles[puzzle_number].headers.get("Puzzle"))
    #         i = int(puzzles[puzzle_number].headers.get("Puzzle"))
    #     # else:
    #     #     print(i)
    #     i += 1

# Example usage:
reorder_pgn("merged_games.pgn", "a.pgn")
