from flask import Blueprint, jsonify
from db.db_connection import get_db_connection
import psycopg2.extras

leaders_bp = Blueprint('leaders', __name__)

@leaders_bp.route('/skater-stats-leaders/current', methods=['GET'])
def get_top_scorers():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM top_scorers ORDER BY goals DESC;")
        top_scorers = cursor.fetchall()
        return jsonify(top_scorers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@leaders_bp.route('/goalie-stats-leaders/current', methods=['GET'])
def get_top_goalies():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM top_goalies ORDER BY wins DESC;")
        top_goalies = cursor.fetchall()
        return jsonify(top_goalies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

