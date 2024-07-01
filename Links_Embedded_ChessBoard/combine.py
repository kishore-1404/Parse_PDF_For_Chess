def read_pgn_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content.split("\n\n")

def combine_puzzles_and_solutions(puzzles, solutions):
    combined = []
    for i, (puzzle, solution) in enumerate(zip(puzzles, solutions), start=1):
        combined.append(f"Puzzle {i}:\n{puzzle}\n\nSolution {i}:\n{solution}\n")
    return combined

def write_combined_file(combined, output_file_path):
    with open(output_file_path, 'w') as file:
        for entry in combined:
            file.write(entry + "\n")

# Example usage
puzzles_file_path = 'DeadlyPuzzlesPGN.txt'
solutions_file_path = 'DeadlyPuzzlesSolPGN.txt'
output_file_path = 'CombinedPuzzlesAndSolutions.txt'

puzzles = read_pgn_file(puzzles_file_path)
solutions = read_pgn_file(solutions_file_path)

combined_entries = combine_puzzles_and_solutions(puzzles, solutions)
write_combined_file(combined_entries, output_file_path)

print(f"Combined file has been written to {output_file_path}")
