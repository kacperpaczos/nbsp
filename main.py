import os
import json
import re
from datetime import datetime

# Defining a class for terminal colors (form blender's svn)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Function to recursively find .json files in a given path (ignores '__output__' directory even if present)
def find_files(path='.'):
    for root, dirs, files in os.walk(path):
        if '__output__' in dirs:
            dirs.remove('__output__')
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)

def process_text(value):
    new_value = ""
    for word in value.split():
        if len(word) == 1:
            new_value += ' ' + word + '&nbsp;'
        else:
            new_value += ' ' + word
    return new_value.replace('&nbsp; ', '&nbsp;').strip()

# Function to process a file, change sentences if needed and return the data and changed sentences
def process_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    changed_sentences = []
    for key, value in data.items():
        if isinstance(value, str):
            new_value = process_text(value)
            if new_value != value:
                changed_sentences.append(new_value)
                data[key] = new_value

    return data, changed_sentences

# Function to save the result in a file with a timestamp in the '__output__' directory
def save_result(data, file_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    result_path = os.path.join('__output__', timestamp, file_path)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    with open(result_path, 'w') as file:
        json.dump(data, file)

# Główna funkcja do przetwarzania każdego znalezionego pliku, drukowania zmienionych zdań i zapisywania wyniku
def main(path='.'):
    for file_path in find_files(path):
        print("=" * (len("In file: " + file_path)))
        print(bcolors.WARNING + "In file: " + file_path + bcolors.ENDC)
        print("=" * (len("In file: " + file_path)))
        data, changed_sentences = process_file(file_path)
        for sentence in changed_sentences:
            colored_sentence = sentence.replace('&nbsp;', bcolors.OKGREEN + '&nbsp;' + bcolors.ENDC)
            print(colored_sentence)
        save_result(data, file_path)

# If the script is run directly, call the main function
if __name__ == '__main__':
    main()





