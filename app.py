from flask import Flask, jsonify
from flask_cors import CORS
from api.teams import teams_bp
from api.leaders import leaders_bp

app = Flask(__name__)
CORS(app)

# Prevent caching for API responses
@app.after_request
def add_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Root route for health check
@app.route("/")
def home():
    return "NHL Stats API is live!"

# Register Blueprints
app.register_blueprint(teams_bp, url_prefix='/api/teams')
app.register_blueprint(leaders_bp, url_prefix='/api') 