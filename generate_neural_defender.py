#!/usr/bin/env python3
"""
Generates neural_defender.svg as a SELF-PLAYING loop using native SVG/SMIL
animation (<animate>, <animateTransform>, <animateMotion>) — no JavaScript.

Why SMIL and not JS: GitHub strips <script> tags from any SVG shown in a
README, so a JS game can never run inside the README itself. SMIL is plain
markup, not a script, so GitHub renders it — this is the same trick behind
things like animated "typing" SVGs and the contribution-snake animation.

Run: python3 generate_neural_defender.py
"""
import math
import pathlib

OUT = pathlib.Path(__file__).parent / "neural_defender.svg"

BG = "#0B0F14"
FRAME_BG = "#0D1117"
BORDER = "#274536"
MINT = "#3CE89A"
MINT_DIM = "#1C6B47"
TEXT = "#E6EDF3"
MUTED = "#7D8590"
RED = "#FF5C6C"
AMBER = "#F5B841"
VIOLET = "#8B8FF7"

THREATS = [
    ("diamond", RED,    "ADVERSARIAL ATTACK", 300),
    ("triangle", VIOLET, "BIAS DRIFT",          30),
    ("square", AMBER,   "OVERFITTING",          20),
    ("dot",    MINT,    "NOISE INJECTION",      10),
]

COLS = 10
ROW_Y0 = 96
ROW_GAP = 30
COL_X0 = 46
COL_GAP = 38

PLAYER_X, PLAYER_Y = 456, 470

# (row, col, cycle-start offset seconds) — enemies that periodically pop & respawn on a 5s loop
POP_ENEMIES = [(0, 2, 0.0), (1, 6, 1.3), (2, 4, 2.6), (3, 8, 3.9), (0, 7, 0.7)]


def shape(kind, cx, cy, fill, size=9, extra=""):
    if kind == "square":
        return f'<rect x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size}" height="{size}" rx="1.5" fill="{fill}">{extra}</rect>' if extra else \
               f'<rect x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size}" height="{size}" rx="1.5" fill="{fill}"/>'
    if kind == "diamond":
        p = f"{cx},{cy-size} {cx+size},{cy} {cx},{cy+size} {cx-size},{cy}"
        return f'<polygon points="{p}" fill="{fill}">{extra}</polygon>' if extra else f'<polygon points="{p}" fill="{fill}"/>'
    if kind == "triangle":
        p = f"{cx},{cy-size} {cx+size},{cy+size*0.8} {cx-size},{cy+size*0.8}"
        return f'<polygon points="{p}" fill="{fill}">{extra}</polygon>' if extra else f'<polygon points="{p}" fill="{fill}"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{size*0.55:.1f}" fill="{fill}">{extra}</circle>' if extra else \
           f'<circle cx="{cx}" cy="{cy}" r="{size*0.55:.1f}" fill="{fill}"/>'


def burst(cx, cy, color, begin):
    dots = []
    for i in range(6):
        ang = math.radians(i * 60)
        dx = round(14 * math.cos(ang), 1)
        dy = round(14 * math.sin(ang), 1)
        dots.append(f"""
      <circle cx="{cx}" cy="{cy}" r="2.2" fill="{color}">
        <animateTransform attributeName="transform" type="translate"
          values="0,0; {dx},{dy}; {dx*1.6},{dy*1.6}" keyTimes="0;0.5;1"
          dur="5s" begin="{begin}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.39;0.44;0.55;1"
          dur="5s" begin="{begin}s" repeatCount="indefinite"/>
      </circle>""")
    return "\n".join(dots)


def enemy_grid():
    out = []
    for r, (kind, fill, _, _) in enumerate(THREATS):
        y = ROW_Y0 + r * ROW_GAP
        for c in range(COLS):
            x = COL_X0 + c * COL_GAP
            pop = next((p for p in POP_ENEMIES if p[0] == r and p[1] == c), None)
            if pop:
                _, _, begin = pop
                anim = (f'<animate attributeName="opacity" '
                        f'values="1;1;0;0;1" keyTimes="0;0.39;0.42;0.55;1" '
                        f'dur="5s" begin="{begin}s" repeatCount="indefinite"/>')
                out.append(shape(kind, x, y, fill, size=7.5 if kind != "dot" else 6, extra=anim))
                out.append(burst(x, y, fill, begin))
            else:
                out.append(shape(kind, x, y, fill, size=7.5 if kind != "dot" else 6))
    return "\n    ".join(out)


def legend():
    out = []
    for i, (kind, fill, label, pts) in enumerate(THREATS):
        y = 134 + i * 26
        out.append(shape(kind, 924, y - 4, fill, size=7))
        out.append(f'<text x="944" y="{y}" fill="{TEXT}" font-size="11">{label}</text>')
        out.append(f'<text x="944" y="{y+13}" fill="{MUTED}" font-size="9.5">= {pts} PTS</text>')
    return "\n    ".join(out)


def bar(x, y, w, pct, fill, label):
    return f"""
    <text x="{x}" y="{y-6}" fill="{MUTED}" font-size="10">{label}</text>
    <rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="#1B2430"/>
    <rect x="{x}" y="{y}" width="{w*pct:.1f}" height="6" rx="3" fill="{fill}"/>
    """


def checkpoints():
    out = []
    for i in range(4):
        x = 66 + i * 200
        out.append(f'<rect x="{x}" y="392" width="150" height="38" rx="6" fill="none" stroke="{MINT_DIM}" stroke-width="1.5"/>')
        out.append(f'<text x="{x+75}" y="415" fill="{MINT_DIM}" font-size="10" text-anchor="middle" letter-spacing="1">CHECKPOINT</text>')
    return "\n    ".join(out)


def player_and_cannon():
    cx, cy = PLAYER_X, PLAYER_Y
    sweep = ('<animateTransform attributeName="transform" type="translate" '
             'values="-200,0; 220,0; -140,0; 200,0; -200,0" '
             'keyTimes="0;0.28;0.55;0.8;1" calcMode="spline" '
             'keySplines="0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1" '
             'dur="11s" repeatCount="indefinite"/>')
    return f"""
  <g id="player">
    {sweep}
    <g stroke="{MINT}" stroke-width="1.3" fill="{FRAME_BG}">
      <circle cx="{cx}" cy="{cy}" r="13"/>
      <circle cx="{cx-22}" cy="{cy+8}" r="7"/>
      <circle cx="{cx+22}" cy="{cy+8}" r="7"/>
      <circle cx="{cx}" cy="{cy-20}" r="7"/>
    </g>
    <g stroke="{MINT}" stroke-width="1" opacity="0.7">
      <line x1="{cx}" y1="{cy}" x2="{cx-22}" y2="{cy+8}"/>
      <line x1="{cx}" y1="{cy}" x2="{cx+22}" y2="{cy+8}"/>
      <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-20}"/>
    </g>
    <circle cx="{cx}" cy="{cy}" r="3" fill="{MINT}">
      <animate attributeName="r" values="3;4.4;3" dur="1.4s" repeatCount="indefinite"/>
    </circle>
    <line x1="{cx}" y1="{cy-13}" x2="{cx}" y2="{cy-46}" stroke="{MINT}" stroke-width="2" opacity="0.85"/>
  </g>
  <text x="{cx}" y="500" fill="{MUTED}" font-size="9.5" text-anchor="middle" letter-spacing="1">MODEL CORE</text>
"""


def bullets():
    """Backprop pulses: small bars whose *origin* travels along a path via
    animateMotion, from roughly the player toward the swarm, on a loop."""
    shots = []
    targets = [(656, 92), (456, 122), (276, 152), (596, 182)]
    for i, (tx, ty) in enumerate(targets):
        begin = round(i * 0.85, 2)
        shots.append(f"""
    <rect x="-1.5" y="-8" width="3" height="12" fill="{MINT}" opacity="0">
      <animateMotion path="M {PLAYER_X},{PLAYER_Y-40} L {tx},{ty}"
        keyTimes="0;1" calcMode="linear" dur="1.3s" begin="{begin}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.85;1"
        dur="1.3s" begin="{begin}s" repeatCount="indefinite"/>
    </rect>""")
    return "\n".join(shots)


def accuracy_ticker():
    values = ["0.5000", "0.6200", "0.7400", "0.8300", "0.9100", "0.9482"]
    out = []
    for i, v in enumerate(values):
        begin = i * 1.0
        out.append(f"""
    <text x="420" y="64" fill="{TEXT}" font-size="18" font-weight="700" opacity="0">{v}
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1"
        dur="6s" begin="{begin}s" repeatCount="indefinite"/>
    </text>""")
    return "\n".join(out)


def swarm_march():
    return ('<animateTransform attributeName="transform" type="translate" '
            'values="0,0; 40,0; 0,4; -14,0; 0,0" keyTimes="0;0.25;0.5;0.75;1" '
            'dur="6s" repeatCount="indefinite"/>')


def build():
    grid = enemy_grid()
    leg = legend()
    chk = checkpoints()
    player = player_and_cannon()
    shots = bullets()
    ticker = accuracy_ticker()
    march = swarm_march()
    bars = (
        bar(924, 322, 130, 0.94, MINT, "ACCURACY")
        + bar(924, 356, 130, 0.62, AMBER, "LEARNING RATE")
        + bar(924, 390, 130, 0.30, RED, "ROBUSTNESS")
    )

    svg = f"""<svg viewBox="0 0 1120 560" xmlns="http://www.w3.org/2000/svg" font-family="'Fira Code','JetBrains Mono',monospace">
  <defs>
    <linearGradient id="nd-edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0.6"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0.35"/>
    </linearGradient>
    <pattern id="nd-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{BORDER}" stroke-width="0.5" opacity="0.5"/>
    </pattern>
    <radialGradient id="nd-glow" cx="0.5" cy="0.5" r="0.6">
      <stop offset="0" stop-color="{MINT}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{MINT}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1120" height="560" fill="{BG}"/>
  <rect x="12" y="12" width="1096" height="536" rx="16" fill="{FRAME_BG}"/>
  <rect x="12" y="12" width="1096" height="536" rx="16" fill="url(#nd-grid)"/>
  <rect x="13" y="13" width="1094" height="534" rx="15" fill="none" stroke="url(#nd-edge)" stroke-width="1.5"/>
  <circle cx="{PLAYER_X}" cy="440" r="150" fill="url(#nd-glow)"/>

  <!-- header -->
  <text x="40" y="52" fill="{MINT}" font-size="19" font-weight="700" letter-spacing="1">NEURAL DEFENDER</text>
  <text x="420" y="46" fill="{MUTED}" font-size="11">ACCURACY</text>
  {ticker}
  <text x="600" y="46" fill="{MUTED}" font-size="11">BEST F1-SCORE</text>
  <text x="600" y="64" fill="{AMBER}" font-size="18" font-weight="700">0.9999</text>

  <g>
    <circle cx="808" cy="41" r="4" fill="{MINT}">
      <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="820" y="45" fill="{MUTED}" font-size="9.5" letter-spacing="1">AUTOPLAY DEMO</text>
  </g>

  <text x="1080" y="46" fill="{MUTED}" font-size="11" text-anchor="end">LIVES</text>
  <g>
    <circle cx="1042" cy="58" r="5" fill="{MINT}"/>
    <circle cx="1060" cy="58" r="5" fill="{MINT}"/>
    <circle cx="1078" cy="58" r="5" fill="{MINT_DIM}"/>
  </g>
  <line x1="24" y1="76" x2="880" y2="76" stroke="{BORDER}" stroke-width="1"/>
  <line x1="900" y1="30" x2="900" y2="76" stroke="{BORDER}" stroke-width="1"/>

  <!-- incoming attack banner -->
  <rect x="790" y="24" width="96" height="22" rx="11" fill="{RED}" opacity="0.18"/>
  <rect x="790" y="24" width="96" height="22" rx="11" fill="none" stroke="{RED}" stroke-width="1.3"/>
  <text x="838" y="39" fill="{RED}" font-size="9.5" text-anchor="middle" letter-spacing="0.5">DATA POISONING</text>

  <!-- enemy / threat swarm: marches together, individual units pop + respawn on a loop -->
  <g id="swarm">
    {march}
    {grid}
  </g>

  <!-- backprop pulses (bullets), auto-firing on a loop -->
  <g>
    {shots}
  </g>

  <!-- checkpoints -->
  <g>
    {chk}
  </g>

  <!-- model core + cannon, sweeping left/right on its own -->
  {player}

  <!-- side panel -->
  <line x1="900" y1="88" x2="900" y2="518" stroke="{BORDER}" stroke-width="1"/>
  <text x="1000" y="106" fill="{MUTED}" font-size="10.5" text-anchor="middle" letter-spacing="2">— THREAT LEGEND —</text>
  <g>
    {leg}
  </g>
  <line x1="912" y1="240" x2="1088" y2="240" stroke="{BORDER}" stroke-width="1"/>
  <text x="1000" y="262" fill="{MUTED}" font-size="10.5" text-anchor="middle" letter-spacing="2">— EPOCH 12 —</text>
  <text x="1000" y="278" fill="{TEXT}" font-size="10" text-anchor="middle">DIFFICULTY: MAX</text>
  <line x1="912" y1="298" x2="1088" y2="298" stroke="{BORDER}" stroke-width="1"/>
  {bars}
  <line x1="912" y1="416" x2="1088" y2="416" stroke="{BORDER}" stroke-width="1"/>
  <text x="1000" y="438" fill="{TEXT}" font-size="11" text-anchor="middle">AUTONOMOUS MODE</text>
  <text x="1000" y="454" fill="{MINT}" font-size="11" text-anchor="middle">SPACE: BACKPROP</text>
  <line x1="912" y1="470" x2="1088" y2="470" stroke="{BORDER}" stroke-width="1"/>
  <text x="1000" y="494" fill="{MUTED}" font-size="10" text-anchor="middle" opacity="0.8">▶ LOOPING</text>

  <!-- footer -->
  <line x1="24" y1="520" x2="1096" y2="520" stroke="{BORDER}" stroke-width="1"/>
  <text x="40" y="540" fill="{MUTED}" font-size="10">AUTO-DEFENSE ENGAGED</text>
  <text x="560" y="540" fill="{MUTED}" font-size="10" text-anchor="middle" opacity="0.8">© Fatima Zahra Moumene — AI ENGINEER</text>
  <text x="1080" y="540" fill="{MUTED}" font-size="10" text-anchor="end">zahra-mmn</text>
</svg>
"""
    OUT.write_text(svg)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
