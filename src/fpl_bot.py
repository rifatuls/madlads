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
    return {team['id']: team['short_name'] for team in teams}

def format_delta(n):
    symbol = "△" if n > 0 else "▽"
    abs_n = abs(n)
    return f"{symbol} {abs_n/1_000_000:.1f}m" if abs_n >= 1_000_000 else f"{symbol} {abs_n/1000:.1f}K"

def generate_markdown_table(title, players):
    lines = [f"## {title}", "", "| Player | Team | Price | Ownership | Δ Change |", "|--------|------|--------|-----------|----------|"]
    for p in players:
        delta = format_delta(p['ownership_change'])
        lines.append(f"| {p['name']} | {p['team']} | £{p['price']} | {p['ownership_pct']:.1f}% | {delta} |")
    lines.append("")
    return "\n".join(lines)

def generate_report(players, team_map):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    enriched = []
    for p in players:
        ownership_pct = float(p['selected_by_percent'])
        if ownership_pct >= 2.0:
            enriched.append({
                'name': f"{p['first_name']} {p['second_name']}",
                'price': p['now_cost'] / 10,
                'team': team_map[p['team']],
                'ownership_pct': ownership_pct,
                'ownership_change': p['transfers_in_event'] - p['transfers_out_event']
            })

    sorted_players = sorted(enriched, key=lambda x: x['ownership_change'], reverse=True)
    top10 = sorted_players[:10]
    bottom10 = sorted_players[-10:]

    top_table = generate_markdown_table("Top 10 Ownership Gains", top10)
    bottom_table = generate_markdown_table("Bottom 10 Ownership Losses", bottom10)

    lines = [f"# FPL Daily Report | {today}", "", top_table, bottom_table]
    return "\n".join(lines)

def save_report(text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"fpl_report_{today}_{timestamp}.txt"

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(text)

    print(f"✅ TXT saved to: {file_path}")
    print("\n📄 File Preview:\n" + "-"*40)
    print(text)
    print("-"*40)

def save_markdown(text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"fpl_report_{today}_{timestamp}.md"

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "docs")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(text)

    # Update homepage
    index_path = os.path.join(output_dir, "index.md")
    with open(index_path, "w") as f:
        f.write(text)

    print(f"✅ Markdown saved to: {file_path}")

if __name__ == "__main__":
    try:
        players, teams = fetch_fpl_data()
        team_map = get_team_name_map(teams)
        report = generate_report(players, team_map)
        save_report(report)
        save_markdown(report)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
