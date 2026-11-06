import os
import requests
print("Scouter ready")
token = os.environ["GITHUB_TOKEN"]
url = "https://api.github.com/graphql"
query = "{ user(login: \"mohammedadalachi\") { contributionsCollection { contributionCalendar { totalContributions } } } }"
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(url, json={"query": query}, headers=headers, timeout=10)
if response.status_code != 200:
    raise ConnectionError(f"GitHub answered with status: {response.status_code}")
total = response.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
power_level = total * 40
note = "IT'S OVER 9000!" if power_level > 9000 else "KEEP TRAINING"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="110" viewBox="0 0 420 110">
<rect x="1" y="1" width="418" height="108" rx="10" fill="#0d1117" stroke="#39ff14" stroke-width="2"/>
<text x="20" y="32" font-family="monospace" font-size="15" fill="#39ff14">SCOUTER // POWER LEVEL</text>
<text x="20" y="72" font-family="monospace" font-size="34" font-weight="bold" fill="#39ff14">{power_level:,}</text>
<text x="20" y="96" font-family="monospace" font-size="13" fill="#39ff14">{note}</text>
</svg>
"""
with open("scouter/power-level.svg", "w", encoding="utf-8") as file:
    file.write(svg)
print(f"Power level: {power_level:,}")
