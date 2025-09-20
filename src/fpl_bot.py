import os
import requests
import datetime

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['elements'], data['teams']

def get_team_name_map(teams):
    return {team['id']: team['name'] for team in teams}

def generate_report(players, team_map):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    lines = [f"FPL Daily Report - {today}\n"]

    enriched = []
    for p in players:
        enriched.append({
            'name': f"{p['first_name']} {p['second_name']}",
            'price': p['now_cost'] / 10,
            'team': team_map[p['team']],
            'ownership_change': p['transfers_in_event'] - p['transfers_out_event']
        })

    sorted_players = sorted(enriched, key=lambda x: x['ownership_change'], reverse=True)
    top10 = sorted_players[:10]
    bottom10 = sorted_players[-10:]

    lines.append("\nTop 10 Ownership Gains:")
    for p in top10:
        lines.append(f"{p['name']} ({p['team']}) - £{p['price']} - Δ {p['ownership_change']}")

    lines.append("\nBottom 10 Ownership Losses:")
    for p in bottom10:
        lines.append(f"{p['name']} ({p['team']}) - £{p['price']} - Δ {p['ownership_change']}")

    return "\n".join(lines)

def save_report(text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Always write a new file with timestamp to force commit
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    file_path = os.path.join(output_dir, f"fpl_report_{today}_{timestamp}.txt")
    with open(file_path, "w") as f:
        f.write(text)

if __name__ == "__main__":
    try:
        players, teams = fetch_fpl_data()
        team_map = get_team_name_map(teams)
        report = generate_report(players, team_map)
        save_report(report)
        print("✅ Report generated successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
