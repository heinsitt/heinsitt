#!/usr/bin/env python3
"""Build the language card for the profile README from the GitHub API.

One card per theme. Counts the primary language of every public, non-fork
repository, and prints the byte share underneath. Python is drawn dark green.

Run from the repository root:  python3 assets/gen_langs.py
Uses GITHUB_TOKEN when it is set, otherwise the anonymous rate limit.
"""
import json
import os
import urllib.request

USER = "heinsitt"
W, H = 1000, 212
SANS = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# GitHub Linguist colours, with Python overridden to the dark green he asked for
COLOURS = {
    "Python": ("#166534", "#15803D"),
    "TypeScript": ("#3178C6", "#3178C6"),
    "JavaScript": ("#F1E05A", "#B58900"),
    "HTML": ("#E34C26", "#C2410C"),
    "CSS": ("#8B5CF6", "#663399"),
    "Shell": ("#89E051", "#4D7C0F"),
    "Go Template": ("#00ADD8", "#0E7490"),
    "Dockerfile": ("#5B7C99", "#384D54"),
    "Jupyter Notebook": ("#DA5B0B", "#B45309"),
    "PHP": ("#A97BFF", "#6B46C1"),
    "Java": ("#B07219", "#8A4B12"),
}
FALLBACK = ("#7C8797", "#5A6472")

THEMES = {
    "dark": dict(bg=[("#0B1016", 0), ("#0F1620", 55), ("#0A0F15", 100)], ink="#F1F5F9",
                 muted="#8CA0B3", faint="#5C6B7A", hair="rgba(255,255,255,0.10)",
                 track="#1B2431", border="rgba(255,255,255,0.08)", idx=0),
    "light": dict(bg=[("#F9FBFD", 0), ("#EEF3F9", 55), ("#F7FAFD", 100)], ink="#0A0E14",
                  muted="#54677A", faint="#7C8B99", hair="rgba(10,14,20,0.10)",
                  track="#DCE4EC", border="rgba(10,14,20,0.10)", idx=1),
}


def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "heinsitt-profile-langs"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def collect():
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
    totals, primary, counted = {}, {}, 0
    for repo in repos:
        if repo.get("fork"):
            continue
        langs = api(f"/repos/{repo['full_name']}/languages")
        if not langs:
            continue
        counted += 1
        for name, size in langs.items():
            totals[name] = totals.get(name, 0) + size
        top = max(langs, key=langs.get)
        primary[top] = primary.get(top, 0) + 1
    return counted, primary, totals


def build(t, counted, primary, totals):
    items = sorted(primary.items(), key=lambda kv: (-kv[1], kv[0]))
    if len(items) > 8:
        head, tail = items[:7], items[7:]
        items = head + [("Other", sum(n for _, n in tail))]
    total_repos = sum(n for _, n in items)

    cx, cy, r, sw = 150, 132, 58, 16
    start, slices = 0.0, []
    for name, n in items:
        pct = n / total_repos * 100
        colour = COLOURS.get(name, FALLBACK)[t["idx"]]
        dash = max(pct - 0.5, 0.4)
        slices.append(
            f'      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{colour}" '
            f'stroke-width="{sw}" pathLength="100" stroke-dasharray="{dash:.3f} {100 - dash:.3f}" '
            f'stroke-dashoffset="{-start:.3f}"/>')
        start += pct

    legend = []
    for i, (name, n) in enumerate(items):
        col, row = divmod(i, 4)
        x = 300 + col * 340
        y = 86 + row * 30
        colour = COLOURS.get(name, FALLBACK)[t["idx"]]
        pct = n / total_repos * 100
        legend.append(
            f'    <rect x="{x}" y="{y - 9}" width="10" height="10" rx="2.5" fill="{colour}"/>'
            f'<text x="{x + 18}" y="{y}" font-family="{SANS}" font-size="12.5" fill="{t["ink"]}">{name}</text>'
            f'<text x="{x + 300}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
            f'fill="{t["muted"]}">{n} repo{"s" if n != 1 else ""} · {pct:.0f}%</text>')

    grand = sum(totals.values()) or 1
    vol = " · ".join(f"{k} {v / grand * 100:.0f}%" for k, v in
                     sorted(totals.items(), key=lambda kv: -kv[1])[:5])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">Languages used across {counted} public repositories</title>
  <desc id="d">Primary language of each repository: {", ".join(f"{k} {v}" for k, v in items)}. Share of code by volume: {vol}.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t["bg"][0][0]}"/><stop offset=".55" stop-color="{t["bg"][1][0]}"/><stop offset="1" stop-color="{t["bg"][2][0]}"/>
    </linearGradient>
    <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <path d="M0 0V8" stroke="{t["ink"]}" stroke-opacity="0.028" stroke-width="1"/>
    </pattern>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#hatch)"/>

    <text x="40" y="44" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Languages used</text>
    <text x="960" y="44" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.1" fill="{t["muted"]}">{counted} REPOS WITH CODE · PRIMARY LANGUAGE</text>
    <path d="M40 58H960" stroke="{t["hair"]}" stroke-width="1"/>

    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["track"]}" stroke-width="{sw}"/>
    <g transform="rotate(-90 {cx} {cy})">
{chr(10).join(slices)}
      <animateTransform attributeName="transform" type="rotate" values="-90 {cx} {cy};270 {cx} {cy}" dur="120s" repeatCount="indefinite"/>
    </g>
    <text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="700" fill="{t["ink"]}">{total_repos}</text>
    <text x="{cx}" y="{cy + 20}" text-anchor="middle" font-family="{MONO}" font-size="8" letter-spacing="2" fill="{t["faint"]}">REPOS</text>

{chr(10).join(legend)}

    <text x="300" y="196" font-family="{MONO}" font-size="9" letter-spacing="0.6" fill="{t["faint"]}">SHARE OF CODE BY VOLUME · {vol.upper()}</text>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["border"]}"/>
</svg>
'''


def main():
    counted, primary, totals = collect()
    for theme, t in THEMES.items():
        open(f"assets/langs-{theme}.svg", "w").write(build(t, counted, primary, totals))
    print("languages:", ", ".join(f"{k} {v}" for k, v in primary.items()), "| repos", counted)


if __name__ == "__main__":
    main()
