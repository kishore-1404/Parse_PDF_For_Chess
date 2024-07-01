import os
import chess.pgn



def split_pgn_file(input_file, output_dir, illegal_pgns_log):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(input_file)
    puzzle_type = os.path.splitext(base_name)[0]
    specific_output_dir = os.path.join(output_dir, puzzle_type)

    if not os.path.exists(specific_output_dir):
        os.makedirs(specific_output_dir)
    
    with open(input_file, encoding="utf-8") as pgn:
        puzzle_number = 0
        while True:
            try:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break

                puzzle_number += 1
                event = game.headers.get("Event", "Puzzle")
                puzzle_id = game.headers.get("Puzzle", str(puzzle_number))
                game.headers["PuzzleType"] = puzzle_type

                output_file = os.path.join(specific_output_dir, f"puzzle_{puzzle_id}.pgn")
                with open(output_file, 'w', encoding="utf-8") as out:
                    out.write(str(game))

                print(f"Saved {event} (Puzzle {puzzle_id}) to {output_file}")

            except Exception as e:
                error_message = f"Error processing game {puzzle_number} in {input_file}: {e}"
                print(error_message)
                with open(illegal_pgns_log, 'a', encoding="utf-8") as log:
                    log.write(f"{error_message}\n")
                continue

def process_pgn_files(input_dir, output_dir):
    illegal_pgns_log = os.path.join(output_dir, "illegal_pgns.txt")
    if os.path.exists(illegal_pgns_log):
        os.remove(illegal_pgns_log)  # Clear the log file if it already exists

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pgn"):
            input_file = os.path.join(input_dir, file_name)
            split_pgn_file(input_file, output_dir, illegal_pgns_log)

# Usage
input_directory = os.getcwd()  # This sets the input directory to the current directory
output_directory = os.path.join(os.getcwd(), "Data")
process_pgn_files(input_directory, output_directory)
