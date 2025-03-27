from flask import Blueprint, jsonify
from db.db_connection import get_db_connection
import psycopg2.extras

leaders_bp = Blueprint('leaders', __name__)

@leaders_bp.route('/skater-stats-leaders/current', methods=['GET'])
def get_top_scorers():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM top_scorers ORDER BY goals DESC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


@leaders_bp.route('/goalie-stats-leaders/current', methods=['GET'])
def get_top_goalies():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM top_goalies ORDER BY wins DESC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

