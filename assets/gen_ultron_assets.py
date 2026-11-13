#!/usr/bin/env python3
"""Generate the Ultron-inspired profile assets: banner, section rule, language card.

Dark and light, pure SVG + SMIL so the motion plays inside a GitHub README <img>.
Run inside the repo's assets/ folder:  python3 gen_ultron_assets.py
"""
import random

FAM = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(
        bg=[("#04060A", 0), ("#0A0D13", 55), ("#05070B", 100)],
        plate=["#161B23", "#0B0E14"],
        plate_edge="#2A323D",
        visor=["#1B2129", "#0C1015"],
        hatch="#FFFFFF", hatch_op=.030,
        rivet="#5A6674",
        accent="#FF3B30",
        accent_soft="#8E1B18",
        ember="#FF7A45",
        name="#F2F4F8",
        eyebrow="#FF6B5E",
        sub="#9FA9B7",
        loc="#7C8797",
        glow="255,59,48", glow_op=.55,
        eye_core="#FFF1EE",
        trace="#FF3B30",
        track="#1A1F27",
        sheen="#FFFFFF", sheen_op=.55,
        vig="#000000", vig_op=.62,
        border="rgba(255,255,255,0.09)",
        meta="#7A8493",
    ),
    "light": dict(
        bg=[("#F2F4F7", 0), ("#E7EBF0", 55), ("#F7F9FB", 100)],
        plate=["#E7ECF2", "#CFD7E1"],
        plate_edge="#B6BEC9",
        visor=["#1B2129", "#0C1015"],
        hatch="#0B0D12", hatch_op=.035,
        rivet="#8A94A2",
        accent="#B32020",
        accent_soft="#8E1B18",
        ember="#C2410C",
        name="#0B0D12",
        eyebrow="#9E1B1B",
        sub="#3D4855",
        loc="#5E6A79",
        glow="200,30,30", glow_op=.38,
        eye_core="#FFF3F0",
        trace="#B32020",
        track="#D5DBE3",
        sheen="#0B0D12", sheen_op=.18,
        vig="#0B0D12", vig_op=.06,
        border="rgba(11,13,18,0.10)",
        meta="#5A6472",
    ),
}


def eye(x, y, tilt, t):
    """One glowing visor slit with its bloom."""
    return f'''      <ellipse cx="{x}" cy="{y}" rx="76" ry="34" fill="url(#bloom)" opacity="0.9"/>
      <g transform="rotate({tilt} {x} {y})">
        <rect x="{x - 27}" y="{y - 6}" width="54" height="12" rx="6" fill="{t['accent']}" opacity="0.35"/>
        <rect x="{x - 23}" y="{y - 4.5}" width="46" height="9" rx="4.5" fill="url(#hot)">
          <animate attributeName="opacity" values="1;1;0.74;1;0.9;1" keyTimes="0;0.42;0.46;0.5;0.86;1" dur="7.4s" repeatCount="indefinite"/>
        </rect>
      </g>'''


def ember(cx, dur, begin, r, t):
    return f'''    <circle cx="{cx}" cy="310" r="{r}" fill="{t['ember']}" opacity="0">
      <animate attributeName="cy" values="310;196" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.85;0.55;0" keyTimes="0;0.18;0.7;1" dur="{dur}s" begin="-{begin}s" repeatCount="indefinite"/>
    </circle>'''


def build_banner(t):
    random.seed(1108)
    p = []
    a = t["accent"]
    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" role="img" aria-labelledby="ttl dsc">
  <title id="ttl">Hein Sitt Tun — Associate DevOps Engineer</title>
  <desc id="dsc">Ultron-inspired profile banner: a crimson visor on dark armour plates, with Hein Sitt Tun, Associate DevOps Engineer, Cloud and Automation, Infrastructure as Code, Observability, Yangon, Myanmar.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="{t['bg'][0][0]}"/>
      <stop offset="55%" stop-color="{t['bg'][1][0]}"/>
      <stop offset="100%" stop-color="{t['bg'][2][0]}"/>
    </linearGradient>
    <linearGradient id="plate" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="{t['plate'][0]}"/>
      <stop offset="100%" stop-color="{t['plate'][1]}"/>
    </linearGradient>
    <linearGradient id="visor" x1="0" y1="0" x2="0.15" y2="1">
      <stop offset="0%" stop-color="{t['visor'][0]}"/>
      <stop offset="100%" stop-color="{t['visor'][1]}"/>
    </linearGradient>
    <radialGradient id="bloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgb({t['glow']})" stop-opacity="{t['glow_op']}"/>
      <stop offset="55%" stop-color="rgb({t['glow']})" stop-opacity="{float(t['glow_op']) * 0.22:.3f}"/>
      <stop offset="100%" stop-color="rgb({t['glow']})" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="hot" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{t['eye_core']}"/>
      <stop offset="45%" stop-color="{a}"/>
      <stop offset="100%" stop-color="{t['accent_soft']}"/>
    </radialGradient>
    <linearGradient id="seam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a}" stop-opacity="0"/>
      <stop offset="18%" stop-color="{a}" stop-opacity="0.55"/>
      <stop offset="82%" stop-color="{a}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a}" stop-opacity="0"/>
      <stop offset="14%" stop-color="{a}" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="{a}" stop-opacity="0.9"/>
      <stop offset="86%" stop-color="{a}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="scanfade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{a}" stop-opacity="0"/>
      <stop offset="60%" stop-color="{a}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse">
      <path d="M-1 1 L1 -1 M0 9 L9 0 M8 10 L10 8" fill="none" stroke="{t['hatch']}" stroke-opacity="{t['hatch_op']}" stroke-width="1"/>
    </pattern>
    <radialGradient id="vig" cx="50%" cy="46%" r="72%">
      <stop offset="45%" stop-color="{t['vig']}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{t['vig']}" stop-opacity="{t['vig_op']}"/>
    </radialGradient>
    <clipPath id="frame"><rect width="1000" height="300" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1000" height="300" fill="url(#bg)"/>
    <rect width="1000" height="300" fill="url(#hatch)"/>''')

    # ── armour plates, rim lit down their inner edge ───────────────────────
    p.append(f'''    <path d="M0 0 H126 L74 78 L92 150 L0 196 Z" fill="url(#plate)"/>
    <path d="M126 0 L74 78 L92 150 L0 196" fill="none" stroke="url(#seam)" stroke-width="1.6"/>
    <path d="M1000 0 H874 L926 78 L908 150 L1000 196 Z" fill="url(#plate)"/>
    <path d="M874 0 L926 78 L908 150 L1000 196" fill="none" stroke="url(#seam)" stroke-width="1.6"/>''')

    for cx, cy in [(74, 26), (86, 62), (92, 118), (30, 168), (926, 26), (914, 62), (908, 118), (970, 168)]:
        p.append(f'    <circle cx="{cx}" cy="{cy}" r="1.7" fill="{t["rivet"]}" opacity="0.55"/>')

    # ── visor: the two slits are the whole point ──────────────────────────
    p.append(f'''    <ellipse cx="500" cy="54" rx="214" ry="66" fill="url(#bloom)" opacity="0.55"/>
    <path d="M368 26 H632 L660 54 L632 82 H368 L340 54 Z" fill="url(#visor)" stroke="{t['plate_edge']}" stroke-width="1.3"/>
    <path d="M368 26 H632 L660 54 L632 82 H368 L340 54 Z" fill="none" stroke="{a}" stroke-opacity="0.30" stroke-width="1"/>
    <path d="M352 54 H402 M598 54 H648" stroke="{a}" stroke-opacity="0.55" stroke-width="1.4"/>''')
    p.append(eye(462, 54, -7, t))
    p.append(eye(538, 54, 7, t))
    p.append(f'''    <path d="M420 92 H580" stroke="url(#seam)" stroke-width="1" opacity="0.45"/>''')

    # ── circuitry along the floor, with a pulse running out to the edges ──
    p.append(f'''    <path d="M0 264 H108 L136 236 H238" fill="none" stroke="{t['trace']}" stroke-opacity="0.22" stroke-width="1.2"/>
    <circle cx="238" cy="236" r="2.6" fill="{t['trace']}" opacity="0.5"/>
    <path d="M1000 270 H884 L856 242 H754" fill="none" stroke="{t['trace']}" stroke-opacity="0.22" stroke-width="1.2"/>
    <circle cx="754" cy="242" r="2.6" fill="{t['trace']}" opacity="0.5"/>
    <path d="M0 264 H108 L136 236 H238" fill="none" stroke="{t['trace']}" stroke-opacity="0.9" stroke-width="1.6" stroke-dasharray="14 260">
      <animate attributeName="stroke-dashoffset" values="280;-40" dur="5.5s" repeatCount="indefinite"/>
    </path>
    <path d="M1000 270 H884 L856 242 H754" fill="none" stroke="{t['trace']}" stroke-opacity="0.9" stroke-width="1.6" stroke-dasharray="14 260">
      <animate attributeName="stroke-dashoffset" values="280;-40" dur="6.8s" begin="-2.4s" repeatCount="indefinite"/>
    </path>''')

    # ── embers drifting up off the floor ─────────────────────────────────
    for i in range(14):
        cx = round(random.uniform(24, 976), 1)
        dur = round(random.uniform(9, 16), 1)
        begin = round(random.uniform(0, 12), 1)
        r = round(random.uniform(0.9, 2.1), 2)
        p.append(ember(cx, dur, begin, r, t))

    # ── copy block ───────────────────────────────────────────────────────
    p.append(f'''    <text x="500" y="122" text-anchor="middle" font-family="{FAM}" font-size="12" font-weight="700" letter-spacing="4.2" fill="{t['eyebrow']}">ASSOCIATE DEVOPS ENGINEER</text>
    <text x="500" y="180" text-anchor="middle" font-family="{FAM}" font-size="54" font-weight="700" letter-spacing="-0.6" fill="{t['name']}">Hein Sitt Tun</text>
    <rect x="352" y="195" width="296" height="1.6" fill="url(#title)"/>
    <path d="M500 191.5 L504.5 196 L500 200.5 L495.5 196 Z" fill="{a}">
      <animate attributeName="opacity" values="0.55;1;0.55" dur="3.6s" repeatCount="indefinite"/>
    </path>
    <text x="500" y="228" text-anchor="middle" font-family="{FAM}" font-size="15" letter-spacing="0.2" fill="{t['sub']}">Cloud &amp; Automation · Infrastructure as Code · Observability</text>
    <text x="500" y="256" text-anchor="middle" font-family="{FAM}" font-size="12.5" letter-spacing="0.9" fill="{t['loc']}">Yangon, Myanmar</text>''')

    # ── sweep, vignette, frame ───────────────────────────────────────────
    p.append(f'''    <rect x="0" y="-44" width="1000" height="44" fill="url(#scanfade)" opacity="0.28">
      <animate attributeName="y" values="-44;300" dur="8.5s" repeatCount="indefinite"/>
    </rect>
    <rect width="1000" height="300" fill="url(#vig)"/>
    <rect x="0.5" y="0.5" width="999" height="299" rx="18" fill="none" stroke="{t['border']}"/>''')

    p.append('  </g>')
    p.append('</svg>')
    return "\n".join(p)


def build_rule(t):
    a = t["accent"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="24" viewBox="0 0 1000 24" role="img" aria-label="Section divider">
  <defs>
    <linearGradient id="rl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a}" stop-opacity="0"/>
      <stop offset="22%" stop-color="{a}" stop-opacity="0.28"/>
      <stop offset="50%" stop-color="{a}" stop-opacity="0.62"/>
      <stop offset="78%" stop-color="{a}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="11.2" width="1000" height="1.4" fill="url(#rl)"/>
  <path d="M250 8.5 V15.5 M750 8.5 V15.5" stroke="{a}" stroke-opacity="0.30" stroke-width="1.2"/>
  <path d="M462 5 L500 12 L462 19" fill="none" stroke="{a}" stroke-opacity="0.55" stroke-width="1.3"/>
  <path d="M538 5 L500 12 L538 19" fill="none" stroke="{a}" stroke-opacity="0.55" stroke-width="1.3"/>
  <path d="M500 8 L504 12 L500 16 L496 12 Z" fill="{a}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3.2s" repeatCount="indefinite"/>
  </path>
  <circle cx="500" cy="12" r="9" fill="none" stroke="{a}" stroke-opacity="0.28">
    <animate attributeName="r" values="8;13;8" dur="3.2s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.32;0;0.32" dur="3.2s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


LANGS = [
    ("TypeScript", 56.7, "#3178C6"),
    ("HTML", 32.7, "#E34F26"),
    ("CSS", 8.2, "#663399"),
    ("JavaScript", 2.2, "#F7DF1E"),
]


def build_langs(t):
    a = t["accent"]
    bar_x, bar_w, bar_y, bar_h = 40.0, 920.0, 74.0, 16.0
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="212" viewBox="0 0 1000 212" role="img" aria-labelledby="lt ld">
  <title id="lt">Language breakdown — TypeScript 56.7%, HTML 32.7%, CSS 8.2%, JavaScript 2.2%, Other 0.1%</title>
  <desc id="ld">Byte-weighted language distribution across Hein Sitt's public repositories.</desc>
  <defs>
    <linearGradient id="lbg" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0" stop-color="{t['bg'][0][0]}"/>
      <stop offset="100%" stop-color="{t['bg'][1][0]}"/>
    </linearGradient>
    <pattern id="lgrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{t['hatch']}" stroke-opacity="{t['hatch_op']}" stroke-width="1"/>
    </pattern>
    <linearGradient id="lsheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['sheen']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['sheen']}" stop-opacity="{t['sheen_op']}"/>
      <stop offset="1" stop-color="{t['sheen']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lhead" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a}" stop-opacity="0.55"/>
      <stop offset="60%" stop-color="{a}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="lbar"><rect x="40" y="74" width="920" height="16" rx="8"/></clipPath>
    <clipPath id="lcard"><rect width="1000" height="212" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#lcard)">
    <rect width="1000" height="212" fill="url(#lbg)"/>
    <rect width="1000" height="212" fill="url(#lgrid)"/>
    <path d="M30 26 V18 H38 M970 26 V18 H962 M30 186 V194 H38 M970 186 V194 H962" fill="none" stroke="{a}" stroke-opacity="0.55" stroke-width="1.4"/>

    <text x="40" y="46" font-family="{FAM}" font-size="15.5" font-weight="700" letter-spacing="0.2" fill="{t['name']}">Language breakdown</text>
    <text x="960" y="46" text-anchor="end" font-family="{FAM}" font-size="11.5" fill="{t['meta']}">18 public repositories   ·   1.4 MB   ·   GitHub Linguist</text>
    <rect x="40" y="57" width="920" height="1" fill="url(#lhead)"/>

    <rect x="40" y="74" width="920" height="16" rx="8" fill="{t['track']}"/>
    <g clip-path="url(#lbar)">''']

    x = bar_x
    for _, pct, color in LANGS:
        w = round(pct / 100 * bar_w, 2)
        p.append(f'      <rect x="{x:.2f}" y="74" width="{w}" height="16" fill="{color}"/>')
        x += w
    p.append(f'''      <rect x="{x:.2f}" y="74" width="{bar_x + bar_w - x:.2f}" height="16" fill="{t['rivet']}" opacity="0.6"/>
      <rect x="-260" y="70" width="150" height="24" fill="url(#lsheen)" opacity="0.30">
        <animate attributeName="x" values="-260;1020" dur="7.5s" repeatCount="indefinite"/>
      </rect>
    </g>''')

    legend = [("TypeScript", "56.7%", "#3178C6", 45.0, 142.0),
              ("HTML", "32.7%", "#E34F26", 351.7, 142.0),
              ("CSS", "8.2%", "#663399", 658.3, 142.0),
              ("JavaScript", "2.2%", "#F7DF1E", 45.0, 182.0),
              ("Other", "0.1%", t["rivet"], 351.7, 182.0)]
    for name, pct_text, color, lx, ly in legend:
        p.append(f'''    <circle cx="{lx}" cy="{ly}" r="5" fill="{color}"/>
    <text x="{lx + 15}" y="{ly - 4}" font-family="{FAM}" font-size="12.5" font-weight="600" fill="{t['name']}">{name}</text>
    <text x="{lx + 15}" y="{ly + 12}" font-family="{FAM}" font-size="11.5" fill="{t['meta']}">{pct_text}</text>''')

    p.append(f'''  </g>

  <rect x="0.5" y="0.5" width="999" height="211" rx="18" fill="none" stroke="{t['border']}"/>
</svg>
''')
    return "\n".join(p)


def main():
    for theme, t in THEMES.items():
        open(f"banner-{theme}.svg", "w").write(build_banner(t))
        open(f"rule-{theme}.svg", "w").write(build_rule(t))
        open(f"langs-{theme}.svg", "w").write(build_langs(t))
        print(f"wrote banner-{theme}.svg + rule-{theme}.svg + langs-{theme}.svg")


if __name__ == "__main__":
    main()
