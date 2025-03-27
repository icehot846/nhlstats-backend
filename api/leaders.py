import requests
from flask import Blueprint, jsonify

bp = Blueprint('leaders', __name__)

@bp.route('/skater-stats-leaders/current')
def proxy_top_scorers():
    try:
        url = "https://api-web.nhle.com/v1/skater-stats-leaders/20242025/2?categories=goals&limit=5"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return jsonify(data["goals"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/goalie-stats-leaders/current')
def proxy_top_goalies():
    try:
        url = "https://api-web.nhle.com/v1/goalie-stats-leaders/current?categories=wins&limit=5"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return jsonify(data["wins"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
