import os

def process_pgn_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith('[Difficulty '):
                parts = line.split(" ")
                difficulty = parts[1].rstrip(']\n')
                line = f'[Difficulty "{difficulty}"]\n'
            f.write(line)

def process_pgn_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.pgn'):
            file_path = os.path.join(directory_path, filename)
            process_pgn_file(file_path)
            print(f"Processed {file_path}")

directory_path = os.getcwd()
process_pgn_directory(directory_path)
