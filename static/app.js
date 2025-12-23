const input = document.getElementById('letters');
const searchBtn = document.getElementById('search-btn');
const loader = document.getElementById('loader');
const results = document.getElementById('results');
const wordsList = document.getElementById('words-list');
const count = document.getElementById('count');
const errorDiv = document.getElementById('error');

// Fonction de recherche
async function searchWords() {
    const letters = input.value.trim();
    
    // Reset
    errorDiv.classList.add('hidden');
    results.classList.add('hidden');
    wordsList.innerHTML = '';
    
    if (!letters) {
        showError('Entre des lettres !');
        return;
    }
    
    // Affiche le loader
    loader.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/find-words', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ letters: letters })
        });
        
        const data = await response.json();
        
        loader.classList.add('hidden');
        
        if (!response.ok) {
            showError(data.error || 'Erreur de recherche');
            return;
        }
        
        // Affiche les résultats
        displayResults(data.words, data.count);
        
    } catch (error) {
        loader.classList.add('hidden');
        showError('Erreur de connexion au serveur');
        console.error(error);
    }
}

function displayResults(words, total) {
    count.textContent = total;
    
    if (total === 0) {
        wordsList.innerHTML = '<p style="grid-column: 1/-1; text-align:center; color:#999;">Aucun mot trouvé 😢</p>';
    } else {
        words.forEach(word => {
            const wordItem = document.createElement('div');
            wordItem.className = 'word-item';
            wordItem.textContent = word;
            wordsList.appendChild(wordItem);
        });
    }
    
    results.classList.remove('hidden');
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

// Events
searchBtn.addEventListener('click', searchWords);
input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchWords();
    }
});