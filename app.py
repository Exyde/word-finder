from flask import Flask, request, jsonify, send_from_directory
from itertools import permutations
from collections import Counter
import unicodedata

def normalize_text(text):
    """Normalise les accents et caractères spéciaux"""
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

def remove_accents(text):
    """Vire tous les accents d'un texte"""
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

app = Flask(__name__)
DICTIONNAIRE = set()



def load_dictionary():
    global DICTIONNAIRE
    with open('data/mots.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            word = line.strip().lower()
            if word and len(word) > 1:
                word_no_accent = remove_accents(word)
                DICTIONNAIRE.add(word_no_accent)
    
    print(f"Dictionnaire chargé : {len(DICTIONNAIRE)} mots")

load_dictionary()


def find_words(letters):
    letters = remove_accents(letters.lower())  # <-- ICI
    found_words = set()
    target_length = len(letters)
    
    from collections import Counter
    available_letters = Counter(letters)
    
    for word in DICTIONNAIRE:
        if len(word) != target_length:
            continue
        
        word_letters = Counter(word)
        
        if all(word_letters[char] <= available_letters[char] for char in word_letters):
            found_words.add(word)
    
    return sorted(list(found_words))
    

@app.route('/api/find-words', methods=['POST'])
def api_find_words():
    data = request.json
    letters = data.get('letters','')

    if not letters or (len(letters)) < 2:
        return jsonify ({'error' : 'Need at least 2 characters.'}), 400
    
    words = find_words(letters)
    return jsonify({'words' : words, 'count' : len(words)})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    load_dictionary()
    #app.run(debug=True, host='0.0.0.0', port=5000)