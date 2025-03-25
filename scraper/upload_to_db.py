import requests
import psycopg2
import psycopg2.extras
from db.db_connection import get_db_connection

TEAM_ABBRS = ["TOR", "MTL", "CHI", "NYR", "BOS","ANA","BUF","CAR","CBJ","CGY","COL","DAL","DET",
                      "EDM","FLA","LAK","MIN","NJD","NSH","NYI","OTT","PHI","PIT",
                      "SEA","SJS","STL","TBL","UTA","VAN","VGK","WPG","WSH"] 

def fetch_team_stats(team_abbr):
    url = f"https://api-web.nhle.com/v1/club-stats/{team_abbr}/now"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def insert_team_if_not_exists(cursor, abbr):
    cursor.execute("SELECT id FROM teams WHERE abbreviation = %s", (abbr,))
    result = cursor.fetchone()
    if result:
        return result["id"]
    cursor.execute(
        "INSERT INTO teams (abbreviation) VALUES (%s) RETURNING id",
        (abbr,)
    )
    return cursor.fetchone()["id"]

def insert_players(cursor, team_id, players):
    for p in players:
        cursor.execute("""
            INSERT INTO players (
                player_id, team_id, first_name, last_name, position,
                games_played, goals, assists, points, plus_minus,
                penalty_minutes, power_play_goals, shorthanded_goals,
                game_winning_goals, overtime_goals, shots, shooting_percentage,
                avg_time_on_ice, faceoff_win_percentage
            ) VALUES (
                %(playerId)s, %(team_id)s, %(first_name)s, %(last_name)s, %(positionCode)s,
                %(gamesPlayed)s, %(goals)s, %(assists)s, %(points)s, %(plusMinus)s,
                %(penaltyMinutes)s, %(powerPlayGoals)s, %(shorthandedGoals)s,
                %(gameWinningGoals)s, %(overtimeGoals)s, %(shots)s, %(shootingPctg)s,
                %(avgTimeOnIcePerGame)s, %(faceoffWinPctg)s
            )
            ON CONFLICT (player_id) DO NOTHING
        """, {
            "playerId": p["playerId"],
            "team_id": team_id,
            "first_name": p["firstName"]["default"],
            "last_name": p["lastName"]["default"],
            **p
        })

def insert_goalies(cursor, team_id, goalies):
    for g in goalies:
        cursor.execute("""
            INSERT INTO goalies (
                player_id, team_id, first_name, last_name,
                games_played, games_started, wins, losses,
                overtime_losses, goals_against_avg, save_percentage,
                shots_against, saves, goals_against, shutouts
            ) VALUES (
                %(playerId)s, %(team_id)s, %(first_name)s, %(last_name)s,
                %(gamesPlayed)s, %(gamesStarted)s, %(wins)s, %(losses)s,
                %(overtimeLosses)s, %(goalsAgainstAverage)s, %(savePercentage)s,
                %(shotsAgainst)s, %(saves)s, %(goalsAgainst)s, %(shutouts)s
            )
            ON CONFLICT (player_id) DO NOTHING
        """, {
            "playerId": g["playerId"],
            "team_id": team_id,
            "first_name": g["firstName"]["default"],
            "last_name": g["lastName"]["default"],
            **g
        })

def main():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        for abbr in TEAM_ABBRS:
            print(f"Processing team {abbr}")
            stats = fetch_team_stats(abbr)
            team_id = insert_team_if_not_exists(cursor, abbr)

            insert_players(cursor, team_id, stats.get("skaters", []))
            insert_goalies(cursor, team_id, stats.get("goalies", []))

        conn.commit()
        print("✅ Data uploaded successfully.")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
