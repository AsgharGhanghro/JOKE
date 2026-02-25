from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # type: ignore
import random
import logging
import re


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../client')
CORS(app)

def analyze_joke_features(joke):
    """Analyze joke features for better scoring"""
    features = {
        'has_question': '?' in joke,
        'has_exclamation': '!' in joke,
        'has_because': 'because' in joke.lower(),
        'has_why': 'why' in joke.lower(),
        'word_count': len(joke.split()),
        'has_punctuation': bool(re.search(r'[.,;:!?]', joke)),
        'has_ellipsis': '...' in joke,
        'has_setup_punchline': len(joke.split()) > 6 and ('?' in joke or 'because' in joke.lower())
    }
    return features

def evaluate_joke_score(joke):
    """Better joke evaluation with feature scoring"""
    features = analyze_joke_features(joke)
    
    # Start with base score
    score = 50
    
    # Feature-based scoring
    if features['has_setup_punchline']:
        score += 20  # Good structure
    
    if features['has_question'] and features['has_exclamation']:
        score += 15  # Question + punchline format
    
    if features['has_question']:
        score += 10  # Question format is good for jokes
    
    if features['has_exclamation']:
        score += 8   # Excitement in punchline
    
    if features['has_because']:
        score += 12  # Explanation format
    
    if features['has_why']:
        score += 10  # Classic joke format
    
    if features['has_ellipsis']:
        score += 5   # Builds anticipation
    
    # Word count scoring (optimal: 10-30 words)
    word_count = features['word_count']
    if 10 <= word_count <= 30:
        score += 10  # Perfect length
    elif 5 <= word_count < 10 or 30 < word_count <= 50:
        score += 5   # Okay length
    elif word_count < 5:
        score -= 10  # Too short
    else:
        score -= 5   # Too long
    
    # Check for puns/wordplay
    pun_words = ['bear', 'bare', 'son', 'sun', 'flower', 'flour', 
                 'see', 'sea', 'write', 'right', 'knight', 'night']
    if any(word in joke.lower() for word in pun_words):
        score += 15  # Puns get extra points
    
    # Add some randomness (but less for consistency)
    score += random.randint(-8, 8)
    
    # Clamp between 0-100
    score = max(0, min(100, round(score)))
    
    return score

def get_feedback_and_rating(score):
    """Get feedback and rating based on score"""
    if score >= 90:
        return "🤯 LEGENDARY! This joke is pure comedy gold!", "LEGENDARY"
    elif score >= 80:
        return "😂 HILARIOUS! You should be on stage with that one!", "EXCELLENT"
    elif score >= 70:
        return "😆 EXCELLENT! That would get big laughs anywhere!", "GREAT"
    elif score >= 60:
        return "😄 VERY GOOD! Solid joke structure and timing!", "GOOD"
    elif score >= 50:
        return "🙂 GOOD JOKE! Not bad at all.", "AVERAGE"
    elif score >= 40:
        return "😐 AVERAGE. Could use some polishing.", "BELOW AVERAGE"
    elif score >= 30:
        return "😕 BELOW AVERAGE. The punchline needs work.", "POOR"
    elif score >= 20:
        return "😬 POOR JOKE. Try a different approach.", "BAD"
    else:
        return "💀 TERRIBLE! My circuits are crying...", "TERRIBLE"

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/health')
def health_check():
    return jsonify({
        "status": "online",
        "message": "JokeBot API v2.0",
        "features": ["joke_evaluation", "battery_system", "voice_feedback"]
    })

@app.route('/evaluate', methods=['POST'])
def evaluate_joke():
    """Evaluate a joke"""
    try:
        data = request.json
        joke = data.get('joke', '').strip()
        
        if not joke:
            return jsonify({"error": "No joke provided"}), 400
        
        if len(joke.split()) < 3:
            return jsonify({
                "error": "Joke too short",
                "suggestion": "Add more words or a proper punchline"
            }), 400
        
        logger.info(f"Evaluating joke: {joke[:50]}...")
        
        # Evaluate joke with better algorithm
        score = evaluate_joke_score(joke)
        feedback, rating = get_feedback_and_rating(score)
        
        # Additional metrics
        features = analyze_joke_features(joke)
        
        result = {
            "quality_score": score,
            "rating": rating,
            "feedback": feedback,
            "model_used": True,
            "confidence": min(0.95, 0.7 + (score / 100) * 0.25),
            "features": {
                "word_count": features['word_count'],
                "has_question": features['has_question'],
                "has_exclamation": features['has_exclamation'],
                "has_punchline": features['has_setup_punchline']
            }
        }
        
        logger.info(f"Evaluation complete: {score}% - {rating}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({
            "error": "Evaluation failed",
            "quality_score": 50,
            "feedback": "Error in evaluation",
            "rating": "ERROR"
        }), 500

@app.route('/battery/impact', methods=['POST'])
def calculate_battery_impact():
    """Calculate battery impact based on score"""
    try:
        data = request.json
        score = data.get('score', 50)
        
        # Calculate battery change
        if score >= 80:
            impact = 15
            message = "Great joke! Battery charged!"
        elif score >= 60:
            impact = 5
            message = "Good joke! Small charge."
        elif score >= 40:
            impact = 0
            message = "Average joke. No change."
        elif score >= 20:
            impact = -10
            message = "Weak joke. Battery drained."
        else:
            impact = -20
            message = "Terrible joke! Major drain!"
        
        return jsonify({
            "battery_change": impact,
            "message": message
        })
        
    except Exception as e:
        return jsonify({
            "battery_change": 0,
            "message": "Error calculating impact"
        }), 500

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    logger.info("🚀 Starting JokeBot Server v2.0...")
    logger.info("🌐 Server running at: http://localhost:5000")
    logger.info("🔋 Battery system: ACTIVE")
    logger.info("🎤 Voice feedback: ENABLED")
    app.run(host='0.0.0.0', port=5000, debug=True)