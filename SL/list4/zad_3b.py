# directory_analyzer.py
import sys
import os
import subprocess
import json

PATH_TO_ANALYZER = "zad_3.py"


def analyze_directory(directory_path):
    file_list = os.listdir(directory_path)
    results = []

    def is_ok(return_code):
        return return_code == 0

    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)

        if os.path.isfile(file_path):
            process = subprocess.Popen(['python', PATH_TO_ANALYZER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            stdout = process.communicate(file_path)

            if is_ok(process.returncode):
                results.append(json.loads(stdout))
            else:
                print(f"Error analyzing {file_path}", file=sys.stderr)

    return results


def create_summary(results):
    total_files = len(results)
    total_characters = sum(r['total_characters'] for r in results)
    total_words = sum(r['total_words'] for r in results)
    total_lines = sum(r['total_lines'] for r in results)

    most_common_char = max(((r['most_common_char'][0], r['most_common_char'][1]) for r in results), key=lambda x: x[1])
    most_common_word = max(((r['most_common_word'][0], r['most_common_word'][1]) for r in results), key=lambda x: x[1])

    return {
        'total_files': total_files,
        'total_characters': total_characters,
        'total_words': total_words,
        'total_lines': total_lines,
        'most_common_char': most_common_char,
        'most_common_word': most_common_word,
    }


if __name__ == '__main__':
    directory_path = sys.argv[1]
    results = analyze_directory(directory_path)
    summary_result = create_summary(results)
    print(summary_result)
