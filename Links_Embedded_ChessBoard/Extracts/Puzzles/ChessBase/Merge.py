import os
import chess.pgn

def merge_pgn_files(input_directory, output_file, error_log_file):
    # Create a list to hold all games
    all_games = []

    with open(error_log_file, 'w', encoding='utf-8') as error_log:
        # Iterate over all files in the input directory
        for filename in os.listdir(input_directory):
            if filename.endswith(".pgn"):
                try:
                    with open(os.path.join(input_directory, filename), 'r', encoding='utf-8') as pgn_file:
                        # Read the PGN file
                        while True:
                            try:
                                game = chess.pgn.read_game(pgn_file)
                                if game is None:
                                    break
                                # Modify headers
                                headers = game.headers
                                if 'Difficulty' in headers:
                                    headers['Medals'] = headers.pop('Difficulty')
                                if 'PuzzleType' in headers:
                                    headers['Source'] = headers.pop('PuzzleType')
                                headers['Annotator'] = "James Rizzitano"
                                headers['PGNBy'] = "Om Kishore"
                                all_games.append(game)
                            except Exception as e:
                                error_log.write(f"Error parsing game in file {filename}: {str(e)}\n")
                except Exception as e:
                    error_log.write(f"Error reading file {filename}: {str(e)}\n")
    
    # Write all games to the output PGN file
    with open(output_file, 'w', encoding='utf-8') as output_pgn:
        for game in all_games:
            try:
                exporter = chess.pgn.FileExporter(output_pgn)
                game.accept(exporter)
                output_pgn.write("\n\n")  # Separate games with double newlines
            except Exception as e:
                error_log.write(f"Error writing game to output file: {str(e)}\n")

# Example usage
input_directory =os.getcwd()
output_file = 'merged_games.pgn'
error_log_file = 'error_log.txt'
merge_pgn_files(input_directory, output_file, error_log_file)
