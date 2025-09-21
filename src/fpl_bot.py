import os
import requests
import datetime
import markdown

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

    sorted_by_gain = sorted(enriched, key=lambda x: x['ownership_change'], reverse=True)
    sorted_by_loss = sorted(enriched, key=lambda x: x['ownership_change'])

    top20 = sorted_by_gain[:20]
    bottom20 = sorted_by_loss[:20]

    top_table = generate_markdown_table("Top 20 Ownership Gains", top20)
    bottom_table = generate_markdown_table("Top 20 Ownership Losses", bottom20)

    lines = [f"# FPL Daily Report | {today}", "", top_table, bottom_table]
    return "\n".join(lines)

def save_txt(text):
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

    print(f"✅ Markdown saved to: {file_path}")
    return filename

def save_html(text):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"fpl_report_{today}_{timestamp}.html"

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "docs")
    os.makedirs(output_dir, exist_ok=True)

    html_body = markdown.markdown(text)
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FPL Report {today}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background-color: #f2f2f2; }}
  </style>
</head>
<body>
{html_body}
</body>
</html>"""

    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(full_html)

    print(f"✅ HTML saved to: {file_path}")
    return filename

def update_index_html(latest_filename):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "docs")
    html_files = sorted(
        [f for f in os.listdir(output_dir) if f.endswith(".html") and f != "index.html"],
        reverse=True
    )

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FPL Bot Homepage</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f9f9f9; }}
    h1, h2 {{ color: #333; }}
    ul {{ padding-left: 20px; }}
    a {{ color: #007acc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <h1>📊 FPL Bot Daily Reports</h1>
  <p>Latest report: <a href="{latest_filename}">{latest_filename}</a></p>

  <h2>📅 Historical Reports</h2>
  <ul>
""")
        for file in html_files:
            f.write(f'    <li><a href="{file}">{file}</a></li>\n')

        f.write("""  </ul>
  <p><em>This page updates automatically via GitHub Actions.</em></p>
</body>
</html>""")

    print(f"✅ index.html updated with {len(html_files)} links")

if __name__ == "__main__":
    try:
        players, teams = fetch_fpl_data()
        team_map = get_team_name_map(teams)
        report = generate_report(players, team_map)

        save_txt(report)
        md_filename = save_markdown(report)
        html_filename = save_html(report)
        update_index_html(html_filename)

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
