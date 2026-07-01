#!/usr/bin/env python3
"""
Generates neural_defender.svg — a static "screenshot" mockup of an
AI-themed defense game, styled to match the profile's terminal / mint palette.

Run: python3 generate_neural_defender.py
"""
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

# threat rows, top -> bottom, (shape, fill, label, points)
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


def shape(kind, cx, cy, fill, size=9):
    if kind == "square":
        return f'<rect x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size}" height="{size}" rx="1.5" fill="{fill}"/>'
    if kind == "diamond":
        p = f"{cx},{cy-size} {cx+size},{cy} {cx},{cy+size} {cx-size},{cy}"
        return f'<polygon points="{p}" fill="{fill}"/>'
    if kind == "triangle":
        p = f"{cx},{cy-size} {cx+size},{cy+size*0.8} {cx-size},{cy+size*0.8}"
        return f'<polygon points="{p}" fill="{fill}"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{size*0.55:.1f}" fill="{fill}"/>'


def enemy_grid():
    out = []
    for r, (kind, fill, _, _) in enumerate(THREATS):
        y = ROW_Y0 + r * ROW_GAP
        for c in range(COLS):
            x = COL_X0 + c * COL_GAP
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


def model_core():
    # small hex-node cluster representing the defended model, plus a cannon
    cx, cy = 456, 470
    return f"""
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
    <circle cx="{cx}" cy="{cy}" r="3" fill="{MINT}"/>
    <line x1="{cx}" y1="{cy-13}" x2="{cx}" y2="{cy-46}" stroke="{MINT}" stroke-width="2" opacity="0.85"/>
    """


def build():
    grid = enemy_grid()
    leg = legend()
    chk = checkpoints()
    core = model_core()
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
  <circle cx="456" cy="440" r="150" fill="url(#nd-glow)"/>

  <!-- header -->
  <text x="40" y="52" fill="{MINT}" font-size="19" font-weight="700" letter-spacing="1">NEURAL DEFENDER</text>
  <text x="420" y="46" fill="{MUTED}" font-size="11">ACCURACY</text>
  <text x="420" y="64" fill="{TEXT}" font-size="18" font-weight="700">0.9482</text>
  <text x="600" y="46" fill="{MUTED}" font-size="11">BEST F1-SCORE</text>
  <text x="600" y="64" fill="{AMBER}" font-size="18" font-weight="700">0.9999</text>
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

  <!-- enemy / threat grid -->
  <g>
    {grid}
  </g>

  <!-- checkpoints -->
  <g>
    {chk}
  </g>

  <!-- model core + cannon (the thing being defended) -->
  <g>
    {core}
  </g>
  <text x="456" y="500" fill="{MUTED}" font-size="9.5" text-anchor="middle" letter-spacing="1">MODEL CORE</text>

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
  <text x="1000" y="438" fill="{TEXT}" font-size="11" text-anchor="middle">← → MOVE</text>
  <text x="1000" y="454" fill="{MINT}" font-size="11" text-anchor="middle">SPACE: BACKPROP</text>
  <line x1="912" y1="470" x2="1088" y2="470" stroke="{BORDER}" stroke-width="1"/>
  <text x="1000" y="494" fill="{MUTED}" font-size="10" text-anchor="middle" opacity="0.8">▶ PRESS ENTER</text>

  <!-- footer -->
  <line x1="24" y1="520" x2="1096" y2="520" stroke="{BORDER}" stroke-width="1"/>
  <text x="40" y="540" fill="{MUTED}" font-size="10">← → MOVE  SPACE: BACKPROP</text>
  <text x="560" y="540" fill="{MUTED}" font-size="10" text-anchor="middle" opacity="0.8">© Fatima Zahra Moumene — AI ENGINEER</text>
  <text x="1080" y="540" fill="{MUTED}" font-size="10" text-anchor="end">zahra-mmn</text>
</svg>
"""
    OUT.write_text(svg)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
