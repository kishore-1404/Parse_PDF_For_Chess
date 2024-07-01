import re

def read_puzzles_txt(txt_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    puzzles = []
    puzzle = {}
    for line in lines:
        line = line.strip()
        if line.startswith('Puzzle '):
            if puzzle:
                puzzles.append(puzzle)
            puzzle = {'puzzle_fen': '', 'solution_fen': ''}
        elif line.startswith('PGN '):
            pass  # Skip the PGN number line
        elif line.startswith('[FEN'):
            fen = re.findall(r'\[FEN "(.*?)"\]', line)[0]
            if 'puzzle_fen' not in puzzle or not puzzle['puzzle_fen']:
                puzzle['puzzle_fen'] = fen
            else:
                puzzle['solution_fen'] = fen
    if puzzle:
        puzzles.append(puzzle)
    
    return puzzles

def read_puzzles_pgn(pgn_file):
    with open(pgn_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    puzzles = []
    puzzle = {'metadata': [], 'moves': ''}
    for line in lines:
        line = line.strip()
        if line.startswith('; Puzzle '):
            if puzzle['moves']:
                puzzles.append(puzzle)
            puzzle = {'metadata': [], 'moves': ''}
        elif line.startswith(';') or line.startswith('['):
            puzzle['metadata'].append(line)
        else:
            puzzle['moves'] += ' ' + line
    if puzzle['moves']:
        puzzles.append(puzzle)
    
    return puzzles

def combine_puzzles(txt_puzzles, pgn_puzzles, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, (txt_puzzle, pgn_puzzle) in enumerate(zip(txt_puzzles, pgn_puzzles), 1):
            file.write(f"; Puzzle {i}\n")
            for line in pgn_puzzle['metadata']:
                file.write(line + "\n")
            file.write(f"[FEN \"{txt_puzzle['puzzle_fen']}\"]\n")
            # file.write("[Solution \"\"]\n")
            file.write(f"{pgn_puzzle['moves'].strip()}\n\n")
            # file.write(f"[SolutionFEN \"{txt_puzzle['solution_fen']}\"]\n\n")

# File paths
txt_file = 'CombinedPuzzlesAndSolutions.txt'
pgn_file = 'Extracted_Sol.pgn'
output_file = 'DeadlyPuzzles.pgn'

# Read puzzles from the files
txt_puzzles = read_puzzles_txt(txt_file)
pgn_puzzles = read_puzzles_pgn(pgn_file)

# Combine puzzles and write to output file
combine_puzzles(txt_puzzles, pgn_puzzles, output_file)
