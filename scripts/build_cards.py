#!/usr/bin/env python3
"""Builds the profile SVG cards in ../assets from data.json.

Run: python3 scripts/build_cards.py
Numbers live in data.json; update them there and re-run.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "scripts" / "data.json").read_text())
OUT = ROOT / "assets"

# Brand Bakery palette (from brandbakery.tech tokens)
NOIR, SURFACE, IVORY, CLAY = "#06060f", "#0d0b1f", "#fff4e6", "#b7afc4"
OCHRE, ROSE, LAVENDER, MINT, ORANGE = "#ffb347", "#ff3d8a", "#7b61ff", "#5cf5c8", "#ff7a1a"
SERIES = [OCHRE, ROSE, LAVENDER, MINT, ORANGE, "#8a8499"]
FONT = "'Space Grotesk','Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w, h, body, title, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{OCHRE}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{ROSE}" stop-opacity=".18"/>
    <stop offset="1" stop-color="{LAVENDER}" stop-opacity=".5"/>
  </linearGradient>
  <radialGradient id="glow" cx=".1" cy="0" r="1">
    <stop offset="0" stop-color="{LAVENDER}" stop-opacity=".22"/>
    <stop offset="1" stop-color="{SURFACE}" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  text {{ font-family: {FONT}; fill: {IVORY}; }}
  .eyebrow {{ font-family: {MONO}; font-size: 11px; letter-spacing: 2px; fill: {OCHRE}; }}
  .h {{ font-size: 20px; font-weight: 700; }}
  .muted {{ fill: {CLAY}; font-size: 12px; }}
  .fade {{ opacity: 0; animation: fade .7s ease-out forwards; }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}
  {extra_css}
</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="{SURFACE}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="url(#edge)"/>
{body}
</svg>
"""


def hero():
    w, h = 1200, 420
    pills = ["Brand Bakery Hub", "BB Studio", "AI Employees", "Arzi", "Kosh"]
    x, pill_svg = 72, []
    for i, p in enumerate(pills):
        pw = 22 + len(p) * 8.6
        pill_svg.append(
            f'<g class="fade" style="animation-delay:{1.1 + i * .12:.2f}s">'
            f'<rect x="{x}" y="318" width="{pw:.0f}" height="34" rx="17" fill="{IVORY}" fill-opacity=".06" stroke="{IVORY}" stroke-opacity=".16"/>'
            f'<text x="{x + pw / 2:.0f}" y="340" text-anchor="middle" font-size="14" fill-opacity=".9">{esc(p)}</text></g>')
        x += pw + 10
    body = f"""
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{IVORY}" stroke-opacity=".045"/>
  </pattern>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{IVORY}"/>
    <stop offset=".55" stop-color="{OCHRE}"/>
    <stop offset="1" stop-color="{ROSE}"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{NOIR}"/>
  <g filter="url(#blur)">
    <circle class="orb a" cx="930" cy="120" r="150" fill="{ROSE}" fill-opacity=".55"/>
    <circle class="orb b" cx="1060" cy="300" r="130" fill="{OCHRE}" fill-opacity=".5"/>
    <circle class="orb c" cx="820" cy="330" r="120" fill="{LAVENDER}" fill-opacity=".6"/>
  </g>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <g transform="translate(905 210)" class="spin">
    <circle r="118" fill="none" stroke="{IVORY}" stroke-opacity=".14" stroke-dasharray="2 10"/>
    <circle r="78" fill="none" stroke="{IVORY}" stroke-opacity=".12"/>
    <circle cx="118" r="5" fill="{OCHRE}"/>
    <circle cx="-55" cy="-55" r="4" fill="{MINT}"/>
  </g>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="url(#edge)"/>
<text x="72" y="96" class="eyebrow fade">FOUNDER · BRAND BAKERY · INDIA</text>
<text x="68" y="182" font-size="78" font-weight="700" letter-spacing="-2.5" fill="url(#name)" class="fade" style="animation-delay:.2s">Abhishek Kumar</text>
<text x="72" y="232" font-size="23" fill-opacity=".92" class="fade" style="animation-delay:.45s">I run a design-first digital agency and build the products,</text>
<text x="72" y="264" font-size="23" fill-opacity=".92" class="fade" style="animation-delay:.6s">AI agents and systems behind it.</text>
<g class="fade" style="animation-delay:.85s"><circle cx="78" cy="293" r="4" fill="{MINT}" class="pulse"/>
<text x="92" y="298" class="muted" font-size="14">Currently shipping the new brandbakery.tech</text></g>
{''.join(pill_svg)}
"""
    css = f"""
  .orb {{ transform-box: fill-box; transform-origin: center; animation: drift 14s ease-in-out infinite alternate; }}
  .b {{ animation-duration: 17s; animation-delay: -4s; }}
  .c {{ animation-duration: 20s; animation-delay: -9s; }}
  @keyframes drift {{ 0% {{ transform: translate(0,0) scale(1); }} 50% {{ transform: translate(-60px,30px) scale(1.15); }} 100% {{ transform: translate(40px,-25px) scale(.9); }} }}
  .spin {{ animation: spin 40s linear infinite; transform-origin: 0 0; }}
  @keyframes spin {{ from {{ transform: translate(905px,210px) rotate(0deg); }} to {{ transform: translate(905px,210px) rotate(360deg); }} }}
  .pulse {{ animation: pulse 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes pulse {{ 50% {{ opacity: .35; transform: scale(1.6); }} }}
"""
    return frame(w, h, body, "Abhishek Kumar, founder of Brand Bakery", css)


def kpis():
    w, h = 1200, 168
    items, cw = DATA["kpis"], (1200 - 48 * 2) / len(DATA["kpis"])
    out = []
    for i, k in enumerate(items):
        x = 48 + i * cw
        col = SERIES[i]
        if i:
            out.append(f'<line x1="{x:.0f}" y1="40" x2="{x:.0f}" y2="128" stroke="{IVORY}" stroke-opacity=".1"/>')
        out.append(
            f'<g class="fade" style="animation-delay:{i * .12:.2f}s">'
            f'<circle cx="{x + 28:.0f}" cy="52" r="4" fill="{col}"/>'
            f'<text x="{x + 40:.0f}" y="57" class="eyebrow" style="fill:{col}">{esc(k["label"].upper())}</text>'
            f'<text x="{x + 24:.0f}" y="108" font-size="46" font-weight="700" letter-spacing="-1.5">{esc(k["value"])}</text>'
            f'<text x="{x + 26:.0f}" y="134" class="muted" font-size="13">{esc(k["sub"])}</text></g>')
    return frame(w, h, "\n".join(out), "Key numbers from GitHub")


def donut(items, title, eyebrow, note, centre_value, centre_label, unit=""):
    w, h = 580, 356
    cx, cy, r, sw = 150, 206, 88, 26
    circ = 2 * math.pi * r
    total = sum(v for _, v in items)
    arcs, legend, acc = [], [], 0.0
    gap = 3
    for i, (name, v) in enumerate(items):
        frac = v / total
        seg = max(frac * circ - gap, 0.5)
        col = SERIES[i % len(SERIES)]
        arcs.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-dasharray="{seg:.2f} {circ:.2f}" stroke-dashoffset="{-acc * circ:.2f}" '
            f'transform="rotate(-90 {cx} {cy})" class="arc" style="animation-delay:{.15 + i * .1:.2f}s; --len:{seg:.2f}"/>')
        acc += frac
        ly = 136 + i * 34
        shown = f"{v:g}{unit}"
        legend.append(
            f'<g class="fade" style="animation-delay:{.3 + i * .1:.2f}s">'
            f'<rect x="300" y="{ly - 12}" width="13" height="13" rx="3" fill="{col}"/>'
            f'<text x="322" y="{ly}" font-size="16">{esc(name)}</text>'
            f'<text x="540" y="{ly}" font-size="15" text-anchor="end" font-family="{MONO}" fill="{CLAY}">{esc(shown)}</text></g>')
    body = f"""
<text x="32" y="44" class="eyebrow">{esc(eyebrow)}</text>
<text x="32" y="72" class="h">{esc(title)}</text>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{IVORY}" stroke-opacity=".06" stroke-width="{sw}"/>
{''.join(arcs)}
<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="34" font-weight="700" letter-spacing="-1">{esc(centre_value)}</text>
<text x="{cx}" y="{cy + 28}" text-anchor="middle" class="muted">{esc(centre_label)}</text>
{''.join(legend)}
<text x="32" y="{h - 22}" class="muted" font-size="11">{esc(note)} · as of {esc(DATA['asOf'])}</text>
"""
    css = """
  .arc { animation: draw 1s cubic-bezier(.2,.7,.2,1) both; }
  @keyframes draw { from { stroke-dasharray: 0 1000; } }
"""
    return frame(w, h, body, title, css)


def activity():
    w, h = 1200, 330
    rows = DATA["activity"]
    left, right, top, bottom = 64, 40, 100, 270
    peak = max(v for _, v in rows)
    nice = math.ceil(peak / 100) * 100
    bw = (w - left - right) / len(rows)
    bars, grid = [], []
    for g in range(0, nice + 1, nice // 4):
        y = bottom - (g / nice) * (bottom - top)
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{w - right}" y2="{y:.1f}" stroke="{IVORY}" stroke-opacity="{.14 if g == 0 else .06}"/>'
                    f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" class="muted" font-size="11" font-family="{MONO}">{g}</text>')
    for i, (m, v) in enumerate(rows):
        bh = max((v / nice) * (bottom - top), 2)
        x = left + i * bw + bw * .2
        last = i == len(rows) - 1
        fill = "url(#bar-hot)" if last else "url(#bar)"
        bars.append(
            f'<g class="grow" style="animation-delay:{i * .06:.2f}s">'
            f'<rect x="{x:.1f}" y="{bottom - bh:.1f}" width="{bw * .6:.1f}" height="{bh:.1f}" rx="6" fill="{fill}"/></g>'
            f'<text x="{x + bw * .3:.1f}" y="{bottom - bh - 8:.1f}" text-anchor="middle" font-size="12" font-family="{MONO}" fill="{IVORY if last else CLAY}" class="fade" style="animation-delay:{.4 + i * .06:.2f}s">{v}</text>'
            f'<text x="{x + bw * .3:.1f}" y="{bottom + 22}" text-anchor="middle" class="muted">{m}</text>')
    total = sum(v for _, v in rows)
    body = f"""
<defs>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAVENDER}"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity=".35"/></linearGradient>
  <linearGradient id="bar-hot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OCHRE}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
</defs>
<text x="32" y="44" class="eyebrow">SHIPPING RHYTHM</text>
<text x="32" y="72" class="h">{total:,} commits in the last 12 months</text>
<text x="{w - 32}" y="72" text-anchor="end" class="muted">{esc(DATA['activityNote'])}</text>
{''.join(grid)}
{''.join(bars)}
"""
    css = """
  .grow { transform-box: fill-box; transform-origin: bottom; animation: grow .8s cubic-bezier(.2,.7,.2,1) both; }
  @keyframes grow { from { transform: scaleY(0); } }
"""
    return frame(w, h, body, "Commits per month", css)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    (OUT / "numbers.svg").write_text(kpis())
    (OUT / "activity.svg").write_text(activity())
    langs = DATA["languages"]
    (OUT / "languages.svg").write_text(donut(
        langs, "What I write", "LANGUAGES", DATA["languagesNote"],
        f"{langs[0][1]:g}%", langs[0][0], unit="%"))
    port = DATA["portfolio"]
    (OUT / "portfolio.svg").write_text(donut(
        port, "Where the repos go", "PORTFOLIO", DATA["portfolioNote"],
        str(sum(v for _, v in port)), "repositories"))
    print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
