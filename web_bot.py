from flask import Flask, render_template, request, jsonify, session
import json
import random
import logging
import threading
import os
import hashlib

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'joke-bot-secret-key-change-in-production')

# Thread lock for concurrent access
jokes_lock = threading.Lock()
votes_lock = threading.Lock()

def load_jokes():
    jokes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jokes.json')
    with open(jokes_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_jokes(jokes):
    jokes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jokes.json')
    with open(jokes_path, 'w', encoding='utf-8') as file:
        json.dump(jokes, file, ensure_ascii=False, indent=2)

def load_votes():
    votes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'votes.json')
    if os.path.exists(votes_path):
        with open(votes_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_votes(votes):
    votes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'votes.json')
    with open(votes_path, 'w', encoding='utf-8') as file:
        json.dump(votes, file, ensure_ascii=False, indent=2)

JOKES = load_jokes()
VOTES = load_votes()  # {"ip_hash:category:index": true}

def load_pending_jokes():
    pending_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_jokes.json')
    if os.path.exists(pending_path):
        with open(pending_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_pending_jokes(pending):
    pending_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_jokes.json')
    with open(pending_path, 'w', encoding='utf-8') as file:
        json.dump(pending, file, ensure_ascii=False, indent=2)

PENDING_JOKES = load_pending_jokes()

CATEGORIES = {
    'Happy': 'Happy',
    'Sad': 'Sad',
    'Scary': 'Scary',
    'Angry': 'Angry',
    'Mysterious': 'Mysterious',
    'Disgusting': 'Disgusting',
    'Bored': 'Bored'
}

# Shuffle categories order once at startup
_cat_keys = list(CATEGORIES.keys())
random.shuffle(_cat_keys)
CATEGORIES = {k: CATEGORIES[k] for k in _cat_keys}

def get_random_joke_weighted(category: str, exclude_index: int = -1):
    jokes_list = JOKES.get(category, [])
    if not jokes_list:
        return None, -1
    if len(jokes_list) <= 1:
        return jokes_list[0], 0
    indices = [i for i in range(len(jokes_list)) if i != exclude_index]
    weights = [1.5 ** jokes_list[i].get('rating', 0) for i in indices]
    chosen = random.choices(indices, weights=weights, k=1)[0]
    return jokes_list[chosen], chosen

def get_client_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def get_vote_key(ip, category, joke_index):
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
    return f"{ip_hash}:{category}:{joke_index}"

def update_rating(category: str, joke_index: int, is_like: bool, client_ip: str):
    vote_key = get_vote_key(client_ip, category, joke_index)

    with votes_lock:
        if vote_key in VOTES:
            return False, "already_voted"

    with jokes_lock:
        if category not in JOKES:
            return False, "not_found"

        if joke_index < 0 or joke_index >= len(JOKES[category]):
            return False, "not_found"

        joke = JOKES[category][joke_index]
        current_rating = joke.get('rating', 0)
        current_votes = joke.get('votes', 0)

        if is_like:
            new_rating = current_rating + 1
        else:
            new_rating = current_rating - 1

        joke['rating'] = new_rating
        joke['votes'] = current_votes + 1

        save_jokes(JOKES)

    with votes_lock:
        VOTES[vote_key] = True
        save_votes(VOTES)

    return True, "ok"

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    from flask import Response
    import json
    return Response(json.dumps(CATEGORIES, ensure_ascii=False), mimetype='application/json')

@app.route('/api/joke', methods=['POST'])
def get_joke():
    data = request.json
    category = data.get('category')
    exclude_index = data.get('exclude_index', -1)

    if category not in CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    joke, joke_index = get_random_joke_weighted(category, exclude_index)

    if joke is None:
        return jsonify({'error': 'No jokes found in this category'}), 404

    rating = joke.get('rating', 0)
    votes = joke.get('votes', 0)

    # Create numeric joke_id
    joke_id = sum(len(JOKES.get(cat, [])) for cat in list(CATEGORIES.keys())[:list(CATEGORIES.keys()).index(category)]) + joke_index

    session['current_joke'] = {
        'category': category,
        'index': joke_index
    }

    return jsonify({
        'text': joke['text'],
        'rating': rating,
        'votes': votes,
        'category': category,
        'index': joke_index,
        'id': joke_id
    })

@app.route('/api/joke/<int:joke_id>', methods=['GET'])
def get_joke_by_id(joke_id):
    # Convert numeric joke_id to category:index
    offset = 0
    for category in CATEGORIES.keys():
        jokes_in_cat = len(JOKES.get(category, []))
        if joke_id < offset + jokes_in_cat:
            index = joke_id - offset
            joke = JOKES[category][index]
            rating = joke.get('rating', 0)
            votes = joke.get('votes', 0)

            session['current_joke'] = {
                'category': category,
                'index': index
            }

            return jsonify({
                'text': joke['text'],
                'rating': rating,
                'votes': votes,
                'category': category,
                'index': index,
                'id': joke_id
            })
        offset += jokes_in_cat
    
    return jsonify({'error': 'Joke not found'}), 404

@app.route('/api/rate', methods=['POST'])
def rate_joke():
    data = request.json
    is_like = data.get('like')
    joke_id = data.get('joke_id')

    # Try to get from request body first
    if joke_id is not None:
        try:
            offset = 0
            for category in CATEGORIES.keys():
                jokes_in_cat = len(JOKES.get(category, []))
                if joke_id < offset + jokes_in_cat:
                    joke_index = joke_id - offset
                    client_ip = get_client_ip()
                    success, reason = update_rating(category, joke_index, is_like, client_ip)
                    if success or reason == "already_voted":
                        joke = JOKES[category][joke_index]
                        session['current_joke'] = {'category': category, 'index': joke_index}
                        return jsonify({
                            'rating': joke.get('rating', 0),
                            'votes': joke.get('votes', 0)
                        }), 200
                offset += jokes_in_cat
        except Exception:
            pass

    # Fallback to session
    joke_data = session.get('current_joke')
    if not joke_data:
        return jsonify({'error': 'No joke rated yet'}), 400

    category = joke_data['category']
    joke_index = joke_data['index']
    client_ip = get_client_ip()

    success, reason = update_rating(category, joke_index, is_like, client_ip)

    if success or reason == "already_voted":
        joke = JOKES[category][joke_index]
        return jsonify({
            'rating': joke.get('rating', 0),
            'votes': joke.get('votes', 0)
        }), 200
    else:
        return jsonify({'error': 'Error rating joke'}), 500

@app.route('/api/submit_joke', methods=['POST'])
def submit_joke():
    data = request.json
    text = data.get('text', '').strip()
    category = data.get('category')

    if not text:
        return jsonify({'error': 'Joke text is required'}), 400

    if not category or category not in CATEGORIES:
        return jsonify({'error': 'Valid category is required'}), 400

    with jokes_lock:
        joke_entry = {
            'id': len(PENDING_JOKES) + 1,
            'text': text,
            'category': category,
            'rating': 0,
            'votes': 0,
            'status': 'pending'
        }
        PENDING_JOKES.append(joke_entry)
        save_pending_jokes(PENDING_JOKES)

    return jsonify({'success': True, 'message': 'Joke submitted for review!'}), 200

@app.route('/api/pending_jokes', methods=['GET'])
def get_pending_jokes():
    return jsonify({
        'pending': PENDING_JOKES,
        'count': len(PENDING_JOKES)
    })

@app.route('/api/approve_joke/<int:joke_id>', methods=['POST'])
def approve_joke(joke_id):
    global PENDING_JOKES
    with jokes_lock:
        joke = None
        for j in PENDING_JOKES:
            if j.get('id') == joke_id:
                joke = j
                break

        if joke is None:
            return jsonify({'error': 'Joke not found'}), 404

        category = joke['category']
        if category not in JOKES:
            JOKES[category] = []

        JOKES[category].append({
            'text': joke['text'],
            'rating': 0,
            'votes': 0
        })
        save_jokes(JOKES)

        PENDING_JOKES = [j for j in PENDING_JOKES if j.get('id') != joke_id]
        save_pending_jokes(PENDING_JOKES)

    return jsonify({'success': True, 'message': 'Joke approved!'}), 200

@app.route('/api/reject_joke/<int:joke_id>', methods=['POST'])
def reject_joke(joke_id):
    global PENDING_JOKES
    with jokes_lock:
        PENDING_JOKES = [j for j in PENDING_JOKES if j.get('id') != joke_id]
        save_pending_jokes(PENDING_JOKES)

    return jsonify({'success': True, 'message': 'Joke rejected!'}), 200

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/pending')
def pending_page():
    return render_template('pending.html')

@app.route('/submit')
def submit_page():
    return render_template('submit.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"Web server starting on http://{host}:{port}")
    print(f"Share this URL so anyone can access the joke bot!")
    app.run(host=host, port=port, debug=False)
