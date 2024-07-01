import re

def parse_pgn(input_pgn):
    # Split the input PGN by puzzles using regex
    puzzles = re.split(r'\n\n', input_pgn.strip())
    parsed_puzzles = []

    for puzzle in puzzles:
        lines = puzzle.strip().split('\n')
        metadata = []
        moves = []
        
        for line in lines:
            if line.startswith(';'):
                continue
            elif line.startswith('['):
                metadata.append(line)
            else:
                moves.append(line)
        
        parsed_puzzles.append((metadata, ' '.join(moves)))
    
    return parsed_puzzles

def format_moves(moves):
    # Ensure moves are properly formatted with periods after move numbers
    moves = re.sub(r'(\d+)(\.\.\.)', r'\1...', moves)
    moves = re.sub(r'(\d+)(\.)', r'\1.', moves)
    return moves

def add_additional_metadata(metadata, puzzle_type, difficulty):
    # Add additional metadata to the puzzle
    metadata.append(f'[Source "{puzzle_type}"]')
    metadata.append(f'[Medals "{difficulty}"]')
    metadata.append(f'[Annotator "James Rizzitano"]')
    metadata.append(f'[PGNBy "Om Kishore"]')
    return metadata

def format_puzzles(parsed_puzzles, puzzle_type, difficulty):
    formatted_puzzles = []

    for metadata, moves in parsed_puzzles:
        metadata = add_additional_metadata(metadata, puzzle_type, difficulty)
        formatted_moves = format_moves(moves)
        formatted_puzzle = '\n'.join(metadata) + '\n\n' + formatted_moves
        formatted_puzzles.append(formatted_puzzle)
    
    return formatted_puzzles

def write_pgn(output_file, formatted_puzzles):
    with open(output_file, 'w', encoding='utf-8') as f:
        for puzzle in formatted_puzzles:
            f.write(puzzle + '\n\n')

def main(input_file, output_file, puzzle_type, difficulty):
    with open(input_file, 'r', encoding='utf-8') as f:
        input_pgn = f.read()
    
    parsed_puzzles = parse_pgn(input_pgn)
    formatted_puzzles = format_puzzles(parsed_puzzles, puzzle_type, difficulty)
    write_pgn(output_file, formatted_puzzles)

if __name__ == "__main__":
    input_file = 'DeadlyPuzzles.pgn'   # Replace with your input file path
    output_file = 'output.pgn' # Replace with your desired output file path
    puzzle_type = 'DeadlyPuzzles'   # Define your puzzle type here
    difficulty = 6             # Define your difficulty level here
    main(input_file, output_file, puzzle_type, difficulty)
