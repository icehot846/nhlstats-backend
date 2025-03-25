import requests

TEAM_ABBRS = ["TOR", "MTL", "CHI", "NYR", "BOS","ANA","BUF","CAR","CBJ","CGY","COL","DAL","DET",
                      "EDM","FLA","LAK","MIN","NJD","NSH","NYI","OTT","PHI","PIT",
                      "SEA","SJS","STL","TBL","UTA","VAN","VGK","WPG","WSH"]

def fetch_team_stats(team_abbr):
    url = f"https://api-web.nhle.com/v1/club-stats/{team_abbr}/now"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    for abbr in TEAM_ABBRS:
        try:
            stats = fetch_team_stats(abbr)
            print(f"✅ Fetched stats for {abbr} — {len(stats.get('skaters', []))} players, {len(stats.get('goalies', []))} goalies")
        except Exception as e:
            print(f"❌ Failed to fetch {abbr}: {e}")

if __name__ == "__main__":
    main()
