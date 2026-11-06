import os

import requests

token = os.environ["GITHUB_TOKEN"]
url = "https://api.github.com/graphql"
query = '{ user(login: "mohammedadalachi") { contributionsCollection { contributionCalendar { weeks { contributionDays { contributionCount } } } } } }'
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(url, json={"query": query}, headers=headers, timeout=10)
if response.status_code != 200:
    raise ConnectionError(f"GitHub answered with status: {response.status_code}")
calendar = response.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]

SPRITE = [
    "......H....H......",
    ".....HH...HHH.....",
    "....HHHH.HHHH.....",
    "...HHHHHHHHHHH....",
    "...HHHHHHHHHHH....",
    "...HHSHHHHSHHH....",
    "...HSSSHHSSSH.....",
    "...HSESSSSESS.....",
    "....SSSSSSSS......",
    ".....SSSSSS.......",
    "...GGWWWWWWGG.....",
    "..GGGWWBBWWWGWWWWW",
    "..SSBWWBBWWBBBWWWW",
    "..SSBBBBBBBBBSSSSS",
    "....BBBBBBBBB.....",
    "....BBBBBBBBB.....",
    ".....BB...BB......",
    ".....BB...BB......",
    ".....BB...BB......",
    "....WWW...WWW.....",
    "....WWW...WWW.....",
]
COLORS = {"H": "#1b1b2f", "S": "#f2c29b", "E": "#111111", "G": "#e0a800", "W": "#f4f4f4", "B": "#2748d6"}
PIXEL = 5
CELL = 14
SQUARE = 11
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
PERIOD = 14.0
FLIGHT = 1.5
GAP = 1.7

grid_x = 120
grid_y = 26
width = grid_x + len(weeks) * CELL + 14
height = 150
sprite_x = 10
sprite_y = 22
hand_x = sprite_x + 17 * PIXEL
hand_y = sprite_y + 12 * PIXEL + 2

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
parts.append(f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="#0d1117" stroke="#39ff14" stroke-width="2"/>')

for row, line in enumerate(SPRITE):
    for col, letter in enumerate(line):
        if letter != ".":
            parts.append(f'<rect x="{sprite_x + col * PIXEL}" y="{sprite_y + row * PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="{COLORS[letter]}"/>')

css = []
x_end = grid_x + len(weeks) * CELL
for week_index, week in enumerate(weeks):
    for day_index, day in enumerate(week["contributionDays"]):
        count = day["contributionCount"]
        x = grid_x + week_index * CELL
        y = grid_y + day_index * CELL
        level = 0 if count == 0 else min(4, 1 + (count - 1) // 3)
        color = LEVELS[level]
        if count == 0:
            parts.append(f'<rect x="{x}" y="{y}" width="{SQUARE}" height="{SQUARE}" rx="2" fill="{color}"/>')
            continue
        name = f"s{week_index}_{day_index}"
        hit = day_index * GAP + 0.25 + FLIGHT * (x - grid_x) / (x_end - grid_x)
        p = hit / PERIOD * 100
        css.append(f"@keyframes {name} {{0%,{p - 0.4:.2f}%{{fill:{color}}}{p:.2f}%{{fill:#ffd000}}{p + 3:.2f}%,96%{{fill:#161b22}}100%{{fill:{color}}}}}")
        css.append(f".{name}{{animation:{name} {PERIOD}s linear infinite}}")
        parts.append(f'<rect class="{name}" x="{x}" y="{y}" width="{SQUARE}" height="{SQUARE}" rx="2" fill="{color}"/>')

for day_index in range(7):
    start = day_index * GAP
    row_y = grid_y + day_index * CELL + SQUARE / 2
    p0 = start / PERIOD * 100
    p1 = (start + 0.25) / PERIOD * 100
    p2 = (start + 0.25 + FLIGHT) / PERIOD * 100
    name = f"b{day_index}"
    css.append(
        f"@keyframes {name} {{0%,{p0:.2f}%{{transform:translate({hand_x}px,{hand_y}px);opacity:0}}"
        f"{p0 + 0.01:.2f}%{{transform:translate({hand_x}px,{hand_y}px);opacity:1}}"
        f"{p1:.2f}%{{transform:translate({grid_x - 8}px,{row_y}px);opacity:1}}"
        f"{p2:.2f}%{{transform:translate({x_end}px,{row_y}px);opacity:1}}"
        f"{p2 + 0.01:.2f}%,100%{{transform:translate({x_end}px,{row_y}px);opacity:0}}}}"
    )
    css.append(f".{name}{{animation:{name} {PERIOD}s linear infinite;opacity:0}}")
    parts.append(f'<g class="{name}"><circle r="8" fill="#ff7a00" opacity="0.55"/><circle r="5" fill="#ffe14d"/><circle r="2.5" fill="#ffffff"/></g>')

parts.insert(1, "<style>" + "".join(css) + "</style>")
parts.append("</svg>")

with open("saiyan/blasts.svg", "w", encoding="utf-8") as file:
    file.write("\n".join(parts))
print(f"Squares drawn: {len(weeks) * 7}, size {width}x{height}")