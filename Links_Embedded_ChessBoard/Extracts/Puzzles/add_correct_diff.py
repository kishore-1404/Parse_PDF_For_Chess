import os

def process_pgn_file(file_path):
    games = []
    current_game = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[Event '):
                if current_game:
                    games.append(current_game)
                current_game = {'headers': [], 'moves': []}
            if current_game is not None:
                if line.startswith('[Difficulty '):
                    difficulty = line.split('"')[1]
                    current_game['headers'].append(f'[Medals "{difficulty}"]')
                else:
                    current_game['headers'].append(line)
            elif line:
                current_game['moves'].append(line)
        if current_game:
            games.append(current_game)

    with open(file_path, 'w', encoding='utf-8') as f:
        for game in games:
            for header in game['headers']:
                f.write(header + '\n')
            f.write('\n')
            for move in game['moves']:
                f.write(move + '\n')
            f.write('\n')

def process_pgn_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.pgn'):
            file_path = os.path.join(directory_path, filename)
            process_pgn_file(file_path)
            print(f"Processed {file_path}")

directory_path = os.getcwd()
process_pgn_directory(directory_path)
