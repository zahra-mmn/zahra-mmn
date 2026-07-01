#!/usr/bin/env python3
"""
Generates philosophy_quotes.svg — a self-playing quote carousel using
native SVG/SMIL animation (no JavaScript), matching the profile's palette.

Like neural_defender.svg, this must be embedded via a jsDelivr CDN URL in
the README (not a local relative path) or GitHub's renderer will strip the
animation tags and only show a static first frame. See the README comment
next to where this image is embedded for the exact URL + purge instructions.

Run: python3 generate_philosophy_card.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CONFIG_PATH = HERE / "quotes_config.json"
OUT_PATH = HERE / "philosophy_quotes.svg"

BG = "#0B0F14"
FRAME_BG = "#0D1117"
BORDER = "#274536"
MINT = "#3CE89A"
MINT_DIM = "#22493A"
DOT_OFF = "#2A3A32"
TEXT = "#E9F1EC"
MUTED = "#7D8590"
VIOLET = "#8B8FF7"

W, H = 1120, 300
CENTER_Y = 128
LINE_HEIGHT = 30
FONT_SIZE = 21


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def quote_block(lines, index, total, dur, per_quote, fade):
    n = len(lines)
    start_y = CENTER_Y - (n - 1) * LINE_HEIGHT / 2
    tspans = "".join(
        f'<tspan x="{W/2}" y="{start_y + i*LINE_HEIGHT:.1f}">{ln}</tspan>'
        for i, ln in enumerate(lines)
    )
    begin = index * per_quote
    f0 = 0
    f1 = fade / dur
    f2 = (per_quote - fade) / dur
    f3 = per_quote / dur
    anim = (f'<animate attributeName="opacity" values="0;1;1;0;0" '
            f'keyTimes="{f0};{f1:.4f};{f2:.4f};{f3:.4f};1" '
            f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    return f'''
    <text font-family="Georgia, 'Times New Roman', serif" font-style="italic"
          font-size="{FONT_SIZE}" fill="{TEXT}" text-anchor="middle" opacity="0">
      {tspans}
      {anim}
    </text>'''


def progress_dots(total, dur, per_quote, fade):
    spacing = 22
    start_x = W / 2 - (total - 1) * spacing / 2
    out = []
    for i in range(total):
        x = start_x + i * spacing
        out.append(f'<circle cx="{x:.1f}" cy="246" r="3" fill="{DOT_OFF}"/>')
        begin = i * per_quote
        f1 = fade / dur
        f2 = (per_quote - fade) / dur
        f3 = per_quote / dur
        out.append(f'''
    <circle cx="{x:.1f}" cy="246" r="3.6" fill="{MINT}" opacity="0">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{f1:.4f};{f2:.4f};{f3:.4f};1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    </circle>''')
    return "\n    ".join(out)


def build():
    cfg = load_config()
    quotes = cfg["quotes"]
    total = len(quotes)
    per_quote = cfg.get("seconds_per_quote", 5)
    dur = per_quote * total
    fade = min(0.8, per_quote * 0.15)

    quote_blocks = "\n".join(
        quote_block(q["lines"], i, total, dur, per_quote, fade)
        for i, q in enumerate(quotes)
    )
    dots = progress_dots(total, dur, per_quote, fade)

    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Fira Code','JetBrains Mono',monospace">
  <defs>
    <radialGradient id="ph-glow" cx="0.5" cy="0.32" r="0.75">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0.10"/>
      <stop offset="0.55" stop-color="{VIOLET}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{FRAME_BG}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ph-edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0.3"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="16" fill="{FRAME_BG}"/>
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="16" fill="url(#ph-glow)"/>
  <rect x="10.5" y="10.5" width="{W-21}" height="{H-21}" rx="15.5" fill="none" stroke="url(#ph-edge)" stroke-width="1.3"/>

  <!-- decorative mark -->
  <text x="66" y="90" font-family="Georgia, serif" font-size="86" fill="{MINT_DIM}" opacity="0.55">&#8220;</text>

  <!-- rotating quotes -->
  <g>
    {quote_blocks}
  </g>

  <!-- progress dots -->
  <g>
    {dots}
  </g>

  <!-- divider + attribution -->
  <line x1="{W/2-26}" y1="196" x2="{W/2+26}" y2="196" stroke="{MINT}" stroke-width="1.5" opacity="0.7"/>
  <text x="{W/2}" y="221" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="0.5">— {cfg['name']}</text>
</svg>
'''
    OUT_PATH.write_text(svg)
    print(f"Wrote {OUT_PATH} — {total} quotes, {per_quote}s each, {dur}s full loop")


if __name__ == "__main__":
    build()
