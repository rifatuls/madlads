<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h1>⚽️ Daily FPL Bot</h1>
  <p>Automated Python bot that fetches Fantasy Premier League data daily, generates a report of top/bottom ownership changes, and commits the output to GitHub via scheduled workflow.</p>
  <p><img src="https://github.com/rifatuls/madlads/actions/workflows/daily.yml/badge.svg" alt="Daily FPL Bot Status"></p>

  <h2>📦 Features</h2>
  <ul>
    <li>Pulls live FPL data from <a href="https://fantasy.premierleague.com" target="_blank">fantasy.premierleague.com</a></li>
    <li>Calculates daily ownership changes for all players</li>
    <li>Outputs a timestamped <code>.txt</code> report to <code>output/</code></li>
    <li>Commits and pushes the report automatically via GitHub Actions</li>
  </ul>

  <h2>🚀 Setup</h2>
  <ol>
    <li>Clone the repo:
      <pre><code>git clone https://github.com/rifatuls/madlads.git
cd madlads</code></pre>
    </li>
    <li>Install dependencies:
      <pre><code>pip install requests</code></pre>
    </li>
    <li>Run locally:
      <pre><code>python src/fpl_bot.py</code></pre>
    </li>
    <li>Output will appear in:
      <pre><code>output/fpl_report_YYYY-MM-DD_HHMMSS.txt</code></pre>
    </li>
  </ol>

  <h2>🤖 GitHub Actions</h2>
  <ul>
    <li>Scheduled to run daily at <strong>10:10 AM Bangladesh time (UTC+6)</strong></li>
    <li>Uses <code>GITHUB_TOKEN</code> to securely commit changes</li>
    <li>Workflow file: <code>.github/workflows/daily.yml</code></li>
  </ul>

  <h2>📁 Folder Structure</h2>
  <pre><code>madlads/
├── src/
│   └── fpl_bot.py
├── output/
│   └── fpl_report_YYYY-MM-DD_HHMMSS.txt
├── .github/
│   └── workflows/
│       └── daily.yml
├── README.md</code></pre>

  <h2>🧠 Notes</h2>
  <ul>
    <li>The bot uses timestamped filenames to ensure a new commit every day.</li>
    <li>If you fork this repo, make sure GitHub Actions is enabled and you have write access.</li>
    <li>You can manually trigger the bot via the <strong>Actions</strong> tab → <code>workflow_dispatch</code>.</li>
  </ul>
</body>
</html>
