# file_analyzer.py
import sys
import json
from collections import Counter


def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.splitlines()
        words = content.split()
        characters = list(content)

        word_count = Counter(words)
        char_count = Counter(characters)

        file_credentials = {
            'file_path': file_path,
            'total_characters': len(characters),
            'total_words': len(words),
            'total_lines': len(lines),
            'most_common_char': char_count.most_common(1)[0],
            'most_common_word': word_count.most_common(1)[0],
        }

    return file_credentials


if __name__ == '__main__':
    file_path = sys.stdin.readline().strip()
    result = analyze_file(file_path)
    print(json.dumps(result))
