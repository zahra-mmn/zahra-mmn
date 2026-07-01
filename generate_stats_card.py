#!/usr/bin/env python3
"""
Regenerates contribution_stats.svg from stats_config.json.

Usage:
    1. Open stats_config.json
    2. Update the numbers (total_contributions, current_streak, etc.)
    3. Run:  python3 generate_stats_card.py
    4. Commit contribution_stats.svg (and the edited config) to your repo

No external dependencies — pure Python standard library.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CONFIG_PATH = HERE / "stats_config.json"
OUT_PATH = HERE / "contribution_stats.svg"

BG = "#0D1117"
PANEL = "#111826"
BORDER = "#1E2A22"
MINT = "#3CE89A"
MINT_DIM = "#1F5C42"
TEXT = "#E6EDF3"
MUTED = "#7D8590"
VIOLET = "#8B8FF7"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def pulse_path(seed_len=40, seed=7):
    """Deterministic little waveform, evokes an activity / neural signal trace."""
    import math
    pts = []
    x0, width = 40, 820
    for i in range(seed_len):
        x = x0 + (width / (seed_len - 1)) * i
        # a few sharp spikes among gentle noise, like a contribution graph pulse
        base = math.sin(i * 0.7 + seed) * 4
        spike = 14 if i % 9 == 0 else (9 if i % 5 == 0 else 0)
        y = 40 - base - spike
        pts.append((round(x, 1), round(y, 1)))
    d = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {x} {y}" for x, y in pts[1:])
    return d


def build_svg(cfg):
    pulse_d = pulse_path()

    svg = f"""<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" font-family="'Fira Code','JetBrains Mono',monospace">
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="pulseFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0"/>
      <stop offset="0.15" stop-color="{MINT}" stop-opacity="1"/>
      <stop offset="0.85" stop-color="{MINT}" stop-opacity="1"/>
      <stop offset="1" stop-color="{MINT}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M 18 0 L 0 0 0 18" fill="none" stroke="{BORDER}" stroke-width="0.6" opacity="0.5"/>
    </pattern>
  </defs>

  <rect x="1" y="1" width="898" height="298" rx="14" fill="{BG}"/>
  <rect x="1" y="1" width="898" height="298" rx="14" fill="url(#grid)"/>
  <rect x="1.5" y="1.5" width="897" height="297" rx="13.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>

  <!-- title bar -->
  <circle cx="26" cy="28" r="4.5" fill="#FF5F56"/>
  <circle cx="42" cy="28" r="4.5" fill="#FFBD2E"/>
  <circle cx="58" cy="28" r="4.5" fill="#27C93F"/>
  <text x="80" y="32" fill="{MUTED}" font-size="12">contribution_stats.sh — activity report</text>
  <text x="874" y="32" fill="{MUTED}" font-size="11" text-anchor="end">updated {cfg['last_updated']}</text>
  <line x1="0" y1="48" x2="900" y2="48" stroke="{BORDER}" stroke-width="1"/>

  <!-- three metric columns -->
  <g font-size="34" font-weight="700" fill="{TEXT}">
    <text x="70" y="120">{cfg['total_contributions']}</text>
    <text x="370" y="120" fill="{MINT}">{cfg['current_streak']}</text>
    <text x="670" y="120">{cfg['longest_streak']}</text>
  </g>
  <g font-size="12.5" fill="{MUTED}" letter-spacing="0.5">
    <text x="70" y="145">TOTAL CONTRIBUTIONS</text>
    <text x="370" y="145" fill="{MINT}">CURRENT STREAK</text>
    <text x="670" y="145">LONGEST STREAK</text>
  </g>
  <g font-size="11" fill="{MUTED}" opacity="0.75">
    <text x="70" y="163">{cfg['contributions_since']} → present</text>
    <text x="370" y="163" fill="{MINT}" opacity="0.85">day tracked: {cfg['current_streak_day']}</text>
    <text x="670" y="163">{cfg['longest_streak_range']}</text>
  </g>

  <line x1="300" y1="78" x2="300" y2="172" stroke="{BORDER}" stroke-width="1"/>
  <line x1="600" y1="78" x2="600" y2="172" stroke="{BORDER}" stroke-width="1"/>

  <!-- signature: activity pulse line -->
  <line x1="0" y1="196" x2="900" y2="196" stroke="{BORDER}" stroke-width="1"/>
  <text x="40" y="222" fill="{MUTED}" font-size="11" letter-spacing="0.5">ACTIVITY SIGNAL</text>
  <path d="{pulse_d}" transform="translate(0,220)" fill="none" stroke="url(#pulseFade)" stroke-width="2"/>

  <!-- footer tags -->
  <line x1="0" y1="256" x2="900" y2="256" stroke="{BORDER}" stroke-width="1"/>
  <text x="40" y="280" fill="{VIOLET}" font-size="11.5">{cfg['public_repos']} public repos</text>
  <text x="220" y="280" fill="{TEXT}" font-size="11.5" opacity="0.85">{cfg['primary_stack']}</text>
  <text x="874" y="280" fill="{MINT}" font-size="11.5" text-anchor="end">focus: {cfg['focus_area']}</text>
</svg>
"""
    return svg


def main():
    cfg = load_config()
    svg = build_svg(cfg)
    OUT_PATH.write_text(svg)
    print(f"Wrote {OUT_PATH} — total={cfg['total_contributions']} "
          f"current_streak={cfg['current_streak']} longest_streak={cfg['longest_streak']}")


if __name__ == "__main__":
    main()
