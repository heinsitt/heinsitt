#!/usr/bin/env python3
"""Generate the space-live profile assets: banner + section rule, dark and light.

Pure SVG + SMIL, so the motion plays inside a GitHub README <img>.
Run inside assets/:  python3 gen_space_assets.py
"""
import random

W, H = 1000, 300
FAM = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

THEMES = {
    "dark": dict(
        bg=[("#05080F", 0), ("#070C17", 52), ("#0B1322", 100)],
        nebula=[("22D3EE", .28, .075), ("8B5CF6", .25, .065),
                ("14B8A6", .18, .05), ("F0ABFC", .12, .03)],
        galaxy="#9BE8FF", galaxy_op=.075,
        stars=["#FFFFFF", "#CDEBFF", "#D7DEFF"], star_scale=1.2,
        name="#F7FAFF", eyebrow="#3BDCF0", sub="#A6B6CC", loc="#6C7E99",
        glow="255,255,255", glow_op=.10,
        planet=["#16455F", "#0A1B2C", "#04080E"], rim="#22D3EE", rim_op=.60,
        orbit="#22D3EE", orbit_op=.14,
        comet_head="#EAFBFF", comet_tail="#7FE7F5",
        sat_body="#DCE7F5", sat_panel="#123A52", sat_line="#8FA6C4",
        sat_beacon="#F0ABFC",
        vig="#000000", vig_op=.52,
        border="rgba(255,255,255,0.10)",
        glint="#FFFFFF", glint_op=.80,
    ),
    "light": dict(
        bg=[("#F8FBFF", 0), ("#EEF4FE", 52), ("#E5EDFB", 100)],
        nebula=[("22D3EE", .17, .045), ("6366F1", .15, .04),
                ("14B8A6", .11, .03), ("D946EF", .08, .022)],
        galaxy="#7DD3FC", galaxy_op=.20,
        stars=["#0B1220", "#164E63", "#4338CA"], star_scale=.7,
        name="#08111F", eyebrow="#0E7490", sub="#3F5069", loc="#66768D",
        glow="255,255,255", glow_op=.82,
        planet=["#F0F8FF", "#CBDCF2", "#AAC2E2"], rim="#0E7490", rim_op=.50,
        orbit="#0E7490", orbit_op=.16,
        comet_head="#0E7490", comet_tail="#38BDF8",
        sat_body="#F7FAFF", sat_panel="#0E7490", sat_line="#7E90A8",
        sat_beacon="#DB2777",
        vig="#8FA6C4", vig_op=.22,
        border="rgba(8,17,31,0.12)",
        glint="#0E7490", glint_op=.55,
    ),
}


def neb_defs(cid, color, o1, o2):
    color = "#" + color.lstrip("#")
    return (f'    <radialGradient id="{cid}" cx="50%" cy="50%" r="50%">\n'
            f'      <stop offset="0%" stop-color="{color}" stop-opacity="{o1}"/>\n'
            f'      <stop offset="55%" stop-color="{color}" stop-opacity="{o2}"/>\n'
            f'      <stop offset="100%" stop-color="{color}" stop-opacity="0"/>\n'
            f'    </radialGradient>')


def starfield(t, seed=11):
    """Three depth layers. Near stars keep clear of the centred text block."""
    rnd = random.Random(seed)
    s = t["star_scale"]
    out = []

    far = []
    for _ in range(78):
        x, y = round(rnd.uniform(4, 996), 1), round(rnd.uniform(4, 296), 1)
        r = round(rnd.uniform(0.4, 0.95), 2)
        o = round(rnd.uniform(0.16, 0.5) * s, 2)
        far.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{rnd.choice(t["stars"])}" opacity="{o}"/>')
    out.append('    <g>\n      ' + '\n      '.join(far) + '\n    </g>')

    mid = []
    for _ in range(26):
        x, y = round(rnd.uniform(8, 992), 1), round(rnd.uniform(8, 292), 1)
        r = round(rnd.uniform(0.9, 1.5), 2)
        hi = round(rnd.uniform(0.5, 0.85) * s, 2)
        lo = round(hi * rnd.uniform(0.25, 0.5), 2)
        d = round(rnd.uniform(3.4, 7.8), 1)
        b = -round(rnd.uniform(0, d), 1)
        mid.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{rnd.choice(t["stars"])}" opacity="{hi}">'
                   f'<animate attributeName="opacity" values="{hi};{lo};{hi}" '
                   f'dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')
    out.append('    <g>\n      ' + '\n      '.join(mid) + '\n    </g>')

    near, placed = [], 0
    while placed < 8:
        x, y = round(rnd.uniform(20, 980), 1), round(rnd.uniform(18, 282), 1)
        if 300 < x < 700 and 52 < y < 275:
            continue
        placed += 1
        r = round(rnd.uniform(1.5, 2.3), 2)
        hi = round(rnd.uniform(0.65, 0.95) * s, 2)
        lo = round(hi * 0.3, 2)
        gh = round(hi * 0.5, 2)
        d = round(rnd.uniform(4.2, 9.0), 1)
        b = -round(rnd.uniform(0, d), 1)
        c = rnd.choice(t["stars"])
        near.append(
            f'<g><circle cx="{x}" cy="{y}" r="{round(r*4.2,1)}" fill="url(#starglow)" opacity="{gh}">'
            f'<animate attributeName="opacity" values="{gh};{round(lo*0.35,2)};{gh}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{hi}">'
            f'<animate attributeName="opacity" values="{hi};{lo};{hi}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle></g>')

    # four-point flare star, upper left
    fx, fy = 92, 54
    near.append(
        f'<g transform="translate({fx} {fy})">'
        f'<path d="M0,-11 L1.5,-1.5 L11,0 L1.5,1.5 L0,11 L-1.5,1.5 L-11,0 L-1.5,-1.5 Z" '
        f'fill="{t["stars"][0]}" opacity="{round(.85*s,2)}">'
        f'<animate attributeName="opacity" values="{round(.85*s,2)};{round(.22*s,2)};{round(.85*s,2)}" '
        f'dur="6.5s" repeatCount="indefinite"/></path>'
        f'<circle r="1.6" fill="{t["stars"][0]}" opacity="{round(.9*s,2)}"/></g>')
    out.append('    <g>\n      ' + '\n      '.join(near) + '\n    </g>')
    return "\n".join(out)


def comet_defs(i, t, length):
    return (f'    <linearGradient id="cm{i}" gradientUnits="userSpaceOnUse" '
            f'x1="{-length}" y1="{-round(length*0.34,1)}" x2="0" y2="0">\n'
            f'      <stop offset="0%" stop-color="{t["comet_tail"]}" stop-opacity="0"/>\n'
            f'      <stop offset="55%" stop-color="{t["comet_tail"]}" stop-opacity="0.35"/>\n'
            f'      <stop offset="100%" stop-color="{t["comet_head"]}" stop-opacity="0.95"/>\n'
            f'    </linearGradient>')


def comet(i, x0, y0, x1, y1, dur, begin, length, width):
    return f'''    <g opacity="0">
      <animate attributeName="opacity" values="0;0.9;0.9;0;0" keyTimes="0;0.04;0.2;0.28;1"
               dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate"
               values="{x0} {y0};{x1} {y1}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <path d="M0,0 L{-length},{-round(length*0.34,1)}" stroke="url(#cm{i})"
            stroke-width="{width}" stroke-linecap="round" fill="none"/>
      <circle r="{round(width+0.8,1)}" fill="url(#comethead)"/>
    </g>'''


def build_banner(t):
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ttl dsc">')
    o.append('  <title id="ttl">Hein Sitt Tun — Associate DevOps Engineer</title>')
    o.append('  <desc id="dsc">Space-themed profile banner: a live starfield with drifting nebula clouds, shooting comets and an orbiting satellite behind the name Hein Sitt Tun, Associate DevOps Engineer, Cloud and Automation, Infrastructure as Code, Observability, Yangon, Myanmar.</desc>')
    o.append('  <defs>')

    stops = "".join(f'\n      <stop offset="{p}%" stop-color="{c}"/>' for c, p in t["bg"])
    o.append(f'    <linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">{stops}\n    </linearGradient>')

    for i, (c, o1, o2) in enumerate(t["nebula"], start=1):
        o.append(neb_defs(f"n{i}", c, o1, o2))

    o.append(f'''    <linearGradient id="gal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["galaxy"]}" stop-opacity="0"/>
      <stop offset="45%" stop-color="{t["galaxy"]}" stop-opacity="{t["galaxy_op"]}"/>
      <stop offset="57%" stop-color="{t["galaxy"]}" stop-opacity="{t["galaxy_op"]}"/>
      <stop offset="100%" stop-color="{t["galaxy"]}" stop-opacity="0"/>
    </linearGradient>''')

    o.append(f'''    <radialGradient id="starglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t["stars"][0]}" stop-opacity="0.55"/>
      <stop offset="40%" stop-color="{t["stars"][0]}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{t["stars"][0]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="comethead" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t["comet_head"]}" stop-opacity="1"/>
      <stop offset="45%" stop-color="{t["comet_head"]}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{t["comet_head"]}" stop-opacity="0"/>
    </radialGradient>''')

    p0, p1, p2 = t["planet"]
    o.append(f'''    <radialGradient id="planet" cx="30%" cy="0%" r="108%">
      <stop offset="0%" stop-color="{p0}"/>
      <stop offset="44%" stop-color="{p1}"/>
      <stop offset="100%" stop-color="{p2}"/>
    </radialGradient>
    <linearGradient id="planetrim" x1="0" y1="0" x2="0.75" y2="1">
      <stop offset="0%" stop-color="{t["rim"]}" stop-opacity="0"/>
      <stop offset="26%" stop-color="{t["rim"]}" stop-opacity="{t["rim_op"]}"/>
      <stop offset="60%" stop-color="{t["rim"]}" stop-opacity="{round(t['rim_op']*0.35,3)}"/>
      <stop offset="100%" stop-color="{t["rim"]}" stop-opacity="0"/>
    </linearGradient>''')

    o.append(f'''    <radialGradient id="tglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgb({t["glow"]})" stop-opacity="{t["glow_op"]}"/>
      <stop offset="62%" stop-color="rgb({t["glow"]})" stop-opacity="{round(t["glow_op"]*0.35,3)}"/>
      <stop offset="100%" stop-color="rgb({t["glow"]})" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig" cx="50%" cy="48%" r="76%">
      <stop offset="42%" stop-color="{t["vig"]}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{t["vig"]}" stop-opacity="{t["vig_op"]}"/>
    </radialGradient>''')

    o.append(f'''    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t["eyebrow"]}" stop-opacity="0"/>
      <stop offset="18%" stop-color="{t["eyebrow"]}"/>
      <stop offset="52%" stop-color="{t["orbit"]}"/>
      <stop offset="82%" stop-color="{t["orbit"]}"/>
      <stop offset="100%" stop-color="{t["orbit"]}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="satpanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["sat_panel"]}" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{t["sat_panel"]}" stop-opacity="0.55"/>
    </linearGradient>''')

    o.append(comet_defs(1, t, 120))
    o.append(comet_defs(2, t, 90))

    o.append(f'    <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="18"/></clipPath>')
    o.append('    <clipPath id="ruleclip"><rect x="405" y="177" width="190" height="6" rx="3"/></clipPath>')
    o.append('  </defs>')
    o.append('')
    o.append('  <g clip-path="url(#frame)">')
    o.append(f'    <rect width="{W}" height="{H}" fill="url(#bg)"/>')

    o.append('    <g transform="rotate(-14 500 150)">'
             '<rect x="-260" y="96" width="1520" height="128" fill="url(#gal)"/></g>')

    clouds = [("n1", 190, 54, 350, 205, 30, -4), ("n2", 828, 66, 330, 200, 37, -12),
              ("n3", 512, 280, 420, 205, 44, -20), ("n4", 620, 26, 205, 140, 33, -8)]
    for cid, cx, cy, rx, ry, dur, begin in clouds:
        o.append(f'    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{cid})">\n'
                 f'      <animate attributeName="cx" values="{cx};{cx+58};{cx}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>\n'
                 f'      <animate attributeName="cy" values="{cy};{cy+34};{cy}" dur="{dur+6}s" begin="{begin}s" repeatCount="indefinite"/>\n'
                 f'      <animate attributeName="rx" values="{rx};{rx+38};{rx}" dur="{dur+11}s" begin="{begin}s" repeatCount="indefinite"/>\n'
                 f'    </ellipse>')

    o.append(starfield(t))

    # orbit paths with travelling nodes
    o.append(f'''    <g fill="none" stroke="{t["orbit"]}" stroke-opacity="{t["orbit_op"]}" stroke-dasharray="2 9">
      <ellipse cx="500" cy="152" rx="482" ry="132"/>
      <ellipse cx="500" cy="152" rx="330" ry="92" stroke-dasharray="1.5 12" stroke-opacity="{round(t['orbit_op']*0.8,3)}"/>
    </g>
    <g>
      <animateMotion dur="52s" repeatCount="indefinite" begin="-8s"
        path="M 18,152 A 482,132 0 1 1 982,152 A 482,132 0 1 1 18,152"/>
      <circle r="5.5" fill="{t["orbit"]}" opacity="0.22"/>
      <circle r="2" fill="{t["comet_head"]}" opacity="0.9"/>
    </g>
    <g>
      <animateMotion dur="38s" repeatCount="indefinite" begin="-24s"
        path="M 830,152 A 330,92 0 1 0 170,152 A 330,92 0 1 0 830,152"/>
      <circle r="4" fill="{t["orbit"]}" opacity="0.2"/>
      <circle r="1.6" fill="{t["comet_head"]}" opacity="0.8"/>
    </g>''')

    # planet arc, bottom left
    o.append(f'''    <g>
      <circle cx="120" cy="392" r="188" fill="{t["rim"]}" opacity="{round(t['rim_op']*0.10,3)}">
        <animate attributeName="opacity" values="{round(t['rim_op']*0.10,3)};{round(t['rim_op']*0.22,3)};{round(t['rim_op']*0.10,3)}" dur="11s" repeatCount="indefinite"/>
      </circle>
      <circle cx="120" cy="392" r="180" fill="url(#planet)"/>
      <circle cx="120" cy="392" r="180" fill="none" stroke="url(#planetrim)" stroke-width="2"/>
      <ellipse cx="86" cy="330" rx="72" ry="26" fill="{t["rim"]}" opacity="{0.05 if t['star_scale']==1 else 0.10}" transform="rotate(-18 86 330)"/>
    </g>''')

    # satellite, upper right (outer group carries the float animation)
    o.append(f'''    <g transform="translate(872 62)">
      <animateTransform attributeName="transform" type="translate"
        values="872 62;866 70;872 62" dur="16s" repeatCount="indefinite"/>
      <g transform="rotate(-18)">
        <rect x="-36" y="-8" width="26" height="16" rx="2.5" fill="url(#satpanel)"/>
        <rect x="10" y="-8" width="26" height="16" rx="2.5" fill="url(#satpanel)"/>
        <line x1="-23.5" y1="-6" x2="-23.5" y2="6" stroke="{t["sat_line"]}" stroke-opacity="0.35"/>
        <line x1="23.5" y1="-6" x2="23.5" y2="6" stroke="{t["sat_line"]}" stroke-opacity="0.35"/>
        <rect x="-8" y="-10" width="16" height="20" rx="3" fill="{t["sat_body"]}" stroke="{t["sat_line"]}" stroke-opacity="0.4"/>
        <circle cx="0" cy="-2" r="2.4" fill="{t["rim"]}" opacity="0.85"/>
        <line x1="0" y1="-10" x2="0" y2="-17" stroke="{t["sat_line"]}" stroke-opacity="0.6"/>
        <circle cx="0" cy="-18.5" r="4.5" fill="{t["sat_beacon"]}" opacity="0.25">
          <animate attributeName="opacity" values="0.45;0.05;0.45" dur="2.4s" repeatCount="indefinite"/>
        </circle>
        <circle cx="0" cy="-18.5" r="1.7" fill="{t["sat_beacon"]}">
          <animate attributeName="opacity" values="1;0.15;1" dur="2.4s" repeatCount="indefinite"/>
        </circle>
      </g>
    </g>''')

    o.append(comet(1, -70, 34, 430, 208, 13, -3, 120, 1.7))
    o.append(comet(2, 560, -46, 1082, 190, 16, -9, 90, 1.4))

    o.append('    <ellipse cx="500" cy="152" rx="352" ry="104" fill="url(#tglow)"/>')
    o.append(f'    <rect width="{W}" height="{H}" fill="url(#vig)"/>')

    o.append(f'''
    <text x="500" y="96" text-anchor="middle" font-family="{FAM}"
          font-size="12" font-weight="600" letter-spacing="4.2" fill="{t["eyebrow"]}">ASSOCIATE DEVOPS ENGINEER</text>

    <text x="500" y="162" text-anchor="middle" font-family="{FAM}"
          font-size="54" font-weight="700" letter-spacing="-1.2" fill="{t["name"]}">Hein Sitt Tun</text>

    <g>
      <rect x="405" y="178" width="190" height="3" rx="1.5" fill="url(#rule)"/>
      <g clip-path="url(#ruleclip)">
        <rect x="345" y="177" width="70" height="6" fill="{t["glint"]}" fill-opacity="{t["glint_op"]}">
          <animate attributeName="x" values="330;600" dur="4.6s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0;0.9;0" dur="4.6s" repeatCount="indefinite"/>
        </rect>
      </g>
    </g>

    <text x="500" y="218" text-anchor="middle" font-family="{FAM}"
          font-size="15" font-weight="400" fill="{t["sub"]}">Cloud &amp; Automation · Infrastructure as Code · Observability</text>

    <text x="500" y="248" text-anchor="middle" font-family="{FAM}"
          font-size="12.5" font-weight="500" letter-spacing="0.7" fill="{t["loc"]}">Yangon, Myanmar</text>''')

    o.append('  </g>')
    o.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["border"]}"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def build_rule(t):
    star = "M0,-6 L1.4,-1.4 L6,0 L1.4,1.4 L0,6 L-1.4,1.4 L-6,0 L-1.4,-1.4 Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="24" viewBox="0 0 1000 24" role="img" aria-label="Section divider">
  <defs>
    <linearGradient id="rd" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['eyebrow']}" stop-opacity="0"/>
      <stop offset="0.2" stop-color="{t['eyebrow']}" stop-opacity="0.20"/>
      <stop offset="0.45" stop-color="{t['eyebrow']}" stop-opacity="0.40"/>
      <stop offset="0.62" stop-color="{t['orbit']}" stop-opacity="0.32"/>
      <stop offset="0.82" stop-color="{t['orbit']}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{t['orbit']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['glint']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['glint']}" stop-opacity="{t['glint_op']}"/>
      <stop offset="100%" stop-color="{t['glint']}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="lc"><rect x="0" y="10" width="1000" height="4"/></clipPath>
  </defs>
  <rect x="0" y="11.4" width="1000" height="1.2" fill="url(#rd)"/>
  <g clip-path="url(#lc)">
    <rect x="-120" y="10" width="120" height="4" fill="url(#glint)">
      <animate attributeName="x" values="-140;1010" dur="7.5s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g transform="translate(500 12)">
    <path d="{star}" fill="{t['eyebrow']}" opacity="0.9">
      <animate attributeName="opacity" values="0.9;0.3;0.9" dur="5s" repeatCount="indefinite"/>
    </path>
  </g>
  <g transform="translate(300 12)">
    <circle r="1.7" fill="{t['eyebrow']}" opacity="0.6">
      <animate attributeName="opacity" values="0.6;0.12;0.6" dur="3.6s" begin="-1.2s" repeatCount="indefinite"/>
    </circle>
  </g>
  <g transform="translate(700 12)">
    <circle r="1.7" fill="{t['orbit']}" opacity="0.55">
      <animate attributeName="opacity" values="0.55;0.1;0.55" dur="4.4s" begin="-2.1s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>
'''


def main():
    for theme, t in THEMES.items():
        with open(f"banner-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(build_banner(t))
        with open(f"rule-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(build_rule(t))
        print(f"wrote banner-{theme}.svg + rule-{theme}.svg")


if __name__ == "__main__":
    main()
