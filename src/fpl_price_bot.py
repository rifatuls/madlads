import os
import requests
import datetime

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['elements'], data['teams']

def get_team_code_map(teams):
    return {team['id']: team['short_name'] for team in teams}

def format_position(pos_id):
    return {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}.get(pos_id, "UNK")

def format_price_change(change):
    return f"+£{change:.1f}" if change > 0 else f"-£{abs(change):.1f}"

def generate_price_report(players, team_map):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    lines = [f"FPL Price Change Report | {today}\n"]

    risers = []
    fallers = []

    for p in players:
        # price_change = p.get('cost_change_start', 0) / 10
        # now_cost	Current price in tenths of £ (e.g. 47 = £4.7)
        # cost_change_start	| Change since season start (in tenths of £)
        # cost_change_event | Change since last gameweek
        # cost_change_start_fall | Total price drops since season start
        # cost_change_start_raise | Total price rises since season start
        price_change = p.get('cost_change_event', 0) / 10
        if price_change != 0:
            entry = {
                'name': f"{p['first_name']} {p['second_name']}",
                'team': team_map[p['team']],
                'position': format_position(p['element_type']),
                'ownership': float(p['selected_by_percent']),
                'price': p['now_cost'] / 10,
                'delta': format_price_change(price_change),
                'form': p['form']
            }
            if price_change > 0:
                risers.append(entry)
            else:
                fallers.append(entry)

    lines.append(f"Risers ({len(risers)})")
    lines.append("Name\tTeam\tPos\tOwnership\tPrice\t∆\tForm")
    for p in risers:
        lines.append(f"{p['name']}\t{p['team']}\t{p['position']}\t{p['ownership']:.1f}%\t£{p['price']:.1f}\t{p['delta']}\t{p['form']}")

    lines.append(f"\nFallers ({len(fallers)})")
    lines.append("Name\tTeam\tPos\tOwnership\tPrice\t∆\tForm")
    for p in fallers:
        lines.append(f"{p['name']}\t{p['team']}\t{p['position']}\t{p['ownership']:.1f}%\t£{p['price']:.1f}\t{p['delta']}\t{p['form']}")

    return "\n".join(lines)

def save_report(text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%H%M%S")
    file_path = os.path.join(output_dir, f"fpl_price_report_{today}_{timestamp}.txt")
    with open(file_path, "w") as f:
        f.write(text)

    print("\n📄 File Preview:\n" + "-"*40)
    print(text)
    print("-"*40)
    print(f"\n✅ Price report saved to: {file_path}")

if __name__ == "__main__":
    try:
        players, teams = fetch_fpl_data()
        team_map = get_team_code_map(teams)
        report = generate_price_report(players, team_map)
        save_report(report)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)