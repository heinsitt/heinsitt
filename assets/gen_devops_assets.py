#!/usr/bin/env python3
"""Generate the DevOps-loop profile assets: banner, section rule, language card.

Dark and light, pure SVG + SMIL. Run inside assets/:  python3 gen_devops_assets.py
"""
import math

W, H = 1000, 300
FAM = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

PHASES = ["PLAN", "CODE", "BUILD", "TEST", "RELEASE", "DEPLOY", "OPERATE", "MONITOR"]

THEMES = {
    "dark": dict(
        bg=[("#0A0E14", 0), ("#0D141D", 55), ("#080B11", 100)],
        grid="#7EA6C4", grid_op=.055,
        ink="#F1F5F9", muted="#8CA0B3", accent="#38BDF8",
        loop=["#38BDF8", "#8B5CF6", "#F59E0B", "#22C55E",
              "#14B8A6", "#EC4899", "#F43F5E", "#A3E635"],
        glow="255,255,255", glow_op=.10,
        pulse="#FFFFFF", pulse_op=.80,
        vig="#000000", vig_op=.42,
        border="rgba(255,255,255,0.10)",
        track="#16202B", track_op=1.0,
    ),
    "light": dict(
        bg=[("#F7F9FC", 0), ("#EDF2F8", 55), ("#F9FBFD", 100)],
        grid="#5C7A93", grid_op=.075,
        ink="#0A0E14", muted="#5A6B7C", accent="#0284C7",
        loop=["#0284C7", "#7C3AED", "#B45309", "#15803D",
              "#0F766E", "#BE185D", "#BE123C", "#4D7C0F"],
        glow="255,255,255", glow_op=.05,
        pulse="#0A0E14", pulse_op=.55,
        vig="#0A0E14", vig_op=.05,
        border="rgba(10,14,20,0.10)",
        track="#D9E2EC", track_op=1.0,
    ),
}


# ── the loop ────────────────────────────────────────────────────────────────
def loop_points(cx, cy, a, b, n=1600):
    """Gerono lemniscate, sampled densely so equal arc pieces can be cut."""
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        pts.append((cx + a * math.cos(t), cy + b * math.sin(t) * math.cos(t)))
    return pts


def cumulative(pts):
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.dist(pts[i - 1], pts[i]))
    return d


def point_at(pts, dist, total):
    """Walk the polyline to an arc-length position (wraps)."""
    target = dist % total
    lo, hi = 0, len(pts) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    i = max(1, lo)
    prev_d, next_d = cum[i - 1], cum[i]
    span = next_d - prev_d or 1e-9
    f = (target - prev_d) / span
    x = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f
    y = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f
    return x, y


def slice_path(pts, start, end, total, step=3.0):
    """Polyline path between two arc-length positions along the loop."""
    length = end - start
    n = max(8, int(length / step))
    out = []
    for k in range(n + 1):
        x, y = point_at(pts, start + length * k / n, total)
        out.append(f"{x:.2f} {y:.2f}")
    return "M" + " L".join(out)


def arrow(x, y, tangent, size, colour):
    """Small solid chevron at the end of a segment, pointing along the flow."""
    tx, ty = tangent
    norm = math.hypot(tx, ty) or 1.0
    tx, ty = tx / norm, ty / norm
    nx, ny = -ty, tx
    tip = (x + tx * size, y + ty * size)
    b1 = (x - nx * size * .85, y - ny * size * .85)
    b2 = (x + nx * size * .85, y + ny * size * .85)
    d = (f"M{tip[0]:.2f} {tip[1]:.2f} L{b1[0]:.2f} {b1[1]:.2f} "
         f"L{b2[0]:.2f} {b2[1]:.2f} Z")
    return f'<path d="{d}" fill="{colour}"/>'


cum = None


def loop_path(pts, total, step=3.0):
    return slice_path(pts, 0, total - 0.01, total, step)


def build_loop(centre, colour_list, width=22, gap=16.0, a=196, b=176):
    """Eight arrow segments around one closed lemniscate."""
    cx, cy = centre
    pts = loop_points(cx, cy, a, b)
    global cum
    cum = cumulative(pts)
    total = cum[-1]
    out = []
    for i, colour in enumerate(colour_list):
        start = total * i / 8 + gap / 2
        end = total * (i + 1) / 8 - gap / 2
        d = slice_path(pts, start, end, total)
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" '
                   f'stroke-width="{width}" stroke-linecap="round"/>')
        ex, ey = point_at(pts, end, total)
        px, py = point_at(pts, end - 6, total)
        out.append("    " + arrow(ex, ey, (ex - px, ey - py), 9.5, colour))
    return "\n    ".join(out), loop_path(pts, total), total


def legend(t, x0, y, spacing=50):
    out = []
    for i, phase in enumerate(PHASES):
        x = x0 + i * spacing
        out.append(f'<circle cx="{x:.1f}" cy="{y - 2.4:.1f}" r="3.1" fill="{t["loop"][i]}"/>')
        out.append(f'<text x="{x + 9:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="7.2" '
                   f'letter-spacing="1.1" fill="{t["muted"]}">{phase}</text>')
    return "\n    ".join(out)


def build_banner(t):
    loop_svg, full_path, total = build_loop((716, 148), t["loop"], a=186, b=176)
    name_id = "loop-main"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" role="img" aria-labelledby="bt bd">
  <title id="bt">Hein Sitt Tun, Associate DevOps Engineer, with a live DevOps infinity loop</title>
  <desc id="bd">Blueprint panel: name and role on the left, and on the right an eight phase DevOps loop drawn as coloured arrow segments that flow continuously around the figure eight.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t["bg"][0][0]}"/>
      <stop offset=".55" stop-color="{t["bg"][1][0]}"/>
      <stop offset="1" stop-color="{t["bg"][2][0]}"/>
    </linearGradient>
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M25 0H0V25" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}" stroke-width="1"/>
    </pattern>
    <pattern id="dots" width="100" height="100" patternUnits="userSpaceOnUse">
      <circle cx="50" cy="50" r="1.1" fill="{t["grid"]}" fill-opacity="{t["grid_op"] * 2.2:.3f}"/>
    </pattern>
    <linearGradient id="spectrum" x1="0" y1="0" x2="1" y2="0">
      {''.join(f'<stop offset="{i / 7:.3f}" stop-color="{c}"/>' for i, c in enumerate(t["loop"]))}
    </linearGradient>
    <radialGradient id="vig" cx="50%" cy="45%" r="72%">
      <stop offset="45%" stop-color="{t["vig"]}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{t["vig"]}" stop-opacity="{t["vig_op"]}"/>
    </radialGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <clipPath id="frame"><rect width="1000" height="300" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1000" height="300" fill="url(#bg)"/>
    <rect width="1000" height="300" fill="url(#grid)"/>
    <rect width="1000" height="300" fill="url(#dots)"/>
    <rect width="1000" height="300" fill="url(#vig)"/>

    <!-- loop glow -->
    <path d="{full_path}" fill="none" stroke="rgba({t["glow"]},{t["glow_op"]})"
          stroke-width="30" stroke-linecap="round" filter="url(#soft)"/>

    <!-- the eight phase segments -->
    {loop_svg}

    <!-- flow: a bright pulse travelling the loop -->
    <path id="{name_id}" d="{full_path}" fill="none" stroke="none"/>
    <path d="{full_path}" fill="none" stroke="{t["pulse"]}" stroke-opacity="{t["pulse_op"]}"
          stroke-width="6" stroke-linecap="round" pathLength="100"
          stroke-dasharray="6 94">
      <animate attributeName="stroke-dashoffset" values="0;-100" dur="5s" repeatCount="indefinite"/>
    </path>
    <circle r="7" fill="{t["pulse"]}" fill-opacity="0.18">
      <animateMotion dur="9s" repeatCount="indefinite">
        <mpath href="#{name_id}"/>
      </animateMotion>
    </circle>
    <circle r="3.1" fill="{t["pulse"]}" fill-opacity="{t["pulse_op"]}">
      <animateMotion dur="9s" repeatCount="indefinite">
        <mpath href="#{name_id}"/>
      </animateMotion>
    </circle>

    <!-- phase legend -->
    <g>
    {legend(t, 522, 266, 49.5)}
    </g>

    <!-- divider between the two halves -->
    <path d="M486 62 V238" stroke="{t["ink"]}" stroke-opacity="0.10" stroke-width="1"/>
    <path d="M482 62 H490 M482 238 H490" stroke="{t["accent"]}" stroke-opacity="0.45" stroke-width="1.2"/>

    <!-- type block -->
    <text x="56" y="106" font-family="{MONO}" font-size="10.5" letter-spacing="3.4" fill="{t["accent"]}">ASSOCIATE DEVOPS ENGINEER</text>
    <text x="54" y="162" font-family="{FAM}" font-size="54" font-weight="700" letter-spacing="-0.6" fill="{t["ink"]}">Hein Sitt Tun</text>
    <rect x="56" y="180" width="244" height="2.4" rx="1.2" fill="url(#spectrum)"/>
    <text x="56" y="214" font-family="{FAM}" font-size="13" fill="{t["muted"]}">Cloud &amp; Automation · Infrastructure as Code · Observability</text>
    <g>
      <circle cx="60" cy="236.5" r="3" fill="{t["loop"][3]}">
        <animate attributeName="opacity" values="1;.35;1" dur="2.6s" repeatCount="indefinite"/>
      </circle>
      <text x="72" y="240" font-family="{MONO}" font-size="9.5" letter-spacing="2.2" fill="{t["muted"]}">YANGON, MYANMAR</text>
    </g>

    <!-- corner marks -->
    <g stroke="{t["accent"]}" stroke-opacity="0.30" stroke-width="1.2" fill="none">
      <path d="M20 34 V20 H34"/><path d="M966 20 H980 V34"/>
      <path d="M20 266 V280 H34"/><path d="M980 266 V280 H966"/>
    </g>
  </g>
  <rect x="0.5" y="0.5" width="999" height="299" rx="18" fill="none" stroke="{t["border"]}"/>
</svg>
'''


def build_rule(t):
    a = t["accent"]
    chevrons = "".join(
        f'<path d="M{500 + i * 16} 9 l5 3 l-5 3" fill="none" stroke="{t["loop"][i + 2]}" '
        f'stroke-width="1.7" stroke-linecap="round" opacity="0.9"/>'
        for i in range(3))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="24" viewBox="0 0 1000 24" role="img" aria-label="Section divider with a DevOps loop palette">
  <defs>
    <linearGradient id="rshot" x1="0" y1="0" x2="1" y2="0">
      {''.join(f'<stop offset="{i / 7:.3f}" stop-color="{c}"/>' for i, c in enumerate(t["loop"]))}
    </linearGradient>
    <linearGradient id="rfade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["ink"]}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t["ink"]}" stop-opacity="0.28"/>
      <stop offset="1" stop-color="{t["ink"]}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="rclip"><rect width="1000" height="24" rx="6"/></clipPath>
  </defs>
  <g clip-path="url(#rclip)">
    <rect x="0" y="11.3" width="1000" height="1.4" fill="url(#rfade)"/>
    <rect x="330" y="10.7" width="340" height="2.6" rx="1.3" fill="url(#rshot)" opacity=".85"/>
    <g>{chevrons}</g>
    <circle r="2.4" fill="{a}">
      <animateMotion dur="6s" repeatCount="indefinite" path="M330 12 H670"/>
      <animate attributeName="opacity" values="1;.45;1" dur="6s" repeatCount="indefinite"/>
    </circle>
    <path d="M14 8 v8 M986 8 v8" stroke="{a}" stroke-opacity=".35" stroke-width="1.2"/>
  </g>
</svg>
'''


LANGS = [("TypeScript", "56.7 %", 56.7, "#3178C6"), ("HTML", "32.7 %", 32.7, "#E34F26"),
         ("CSS", "8.2 %", 8.2, "#663399"), ("JavaScript", "2.2 %", 2.2, "#F7DF1E")]


def build_langs(t):
    bx, by, bw, bh = 40, 74, 920, 16
    x = bx
    bars = []
    for _, _, pct, col in LANGS:
        w = pct / 100 * bw
        bars.append(f'<rect x="{x:.2f}" y="{by}" width="{w:.2f}" height="{bh}" fill="{col}"/>')
        x += w
    bars.append(f'<rect x="{x:.2f}" y="{by}" width="{bx + bw - x:.2f}" height="{bh}" fill="{t["muted"]}" opacity=".55"/>')
    spots = [(45, 138), (351.7, 138), (658.3, 138), (45, 168), (351.7, 168)]
    legend_rows = []
    for (lx, ly), (name, pct, _, col) in zip(spots, LANGS):
        legend_rows.append(
            f'<circle cx="{lx:.1f}" cy="{ly - 4:.1f}" r="4" fill="{col}"/>'
            f'<text x="{lx + 13:.1f}" y="{ly:.1f}" font-family="{FAM}" font-size="12.5" fill="{t["ink"]}">{name}</text>'
            f'<text x="{lx + 13:.1f}" y="{ly + 15:.1f}" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}">{pct}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="212" viewBox="0 0 1000 212" role="img" aria-labelledby="lt ld">
  <title id="lt">Language breakdown — TypeScript 56.7 percent, HTML 32.7 percent, CSS 8.2 percent, JavaScript 2.2 percent</title>
  <desc id="ld">Byte-weighted language distribution across Hein Sitt's public repositories.</desc>
  <defs>
    <linearGradient id="lbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t["bg"][0][0]}"/>
      <stop offset="1" stop-color="{t["bg"][1][0]}"/>
    </linearGradient>
    <pattern id="lgrid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M25 0H0V25" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}" stroke-width="1"/>
    </pattern>
    <linearGradient id="lshot" x1="0" y1="0" x2="1" y2="0">
      {''.join(f'<stop offset="{i / 7:.3f}" stop-color="{c}"/>' for i, c in enumerate(t["loop"]))}
    </linearGradient>
    <clipPath id="lbar"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8"/></clipPath>
    <clipPath id="lcard"><rect width="1000" height="212" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#lcard)">
    <rect width="1000" height="212" fill="url(#lbg)"/>
    <rect width="1000" height="212" fill="url(#lgrid)"/>

    <text x="40" y="46" font-family="{FAM}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Language breakdown</text>
    <text x="960" y="46" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.6" fill="{t["muted"]}">18 PUBLIC REPOSITORIES · 1.4 MB · GITHUB LINGUIST</text>
    <rect x="40" y="60" width="920" height="2.4" rx="1.2" fill="url(#lshot)" opacity=".55"/>

    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{t["track"]}"/>
    <g clip-path="url(#lbar)">
      {''.join(bars)}
    </g>
    <rect x="{bx}" y="{by + bh + 42}" width="{bw}" height="3" rx="1.5" fill="{t["track"]}"/>

    <g>{''.join(legend_rows)}</g>

    <g stroke="{t["accent"]}" stroke-opacity=".28" stroke-width="1.1" fill="none">
      <path d="M14 28 V14 H28"/><path d="M972 14 H986 V28"/>
      <path d="M14 184 V198 H28"/><path d="M986 184 V198 H972"/>
    </g>
  </g>
  <rect x=".5" y=".5" width="999" height="211" rx="18" fill="none" stroke="{t["border"]}"/>
</svg>
'''


def main():
    for theme, t in THEMES.items():
        open(f"banner-{theme}.svg", "w").write(build_banner(t))
        open(f"rule-{theme}.svg", "w").write(build_rule(t))
        open(f"langs-{theme}.svg", "w").write(build_langs(t))
    print("wrote banner, rule and langs for:", ", ".join(THEMES))


if __name__ == "__main__":
    main()
