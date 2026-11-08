#!/usr/bin/env python3
"""Builds every image on the profile README, in light and dark.

Run: pip install fonttools brotli && python3 scripts/build_profile.py
Edit the copy below, then re-run. Output goes to assets/.

Fonts (SIL OFL): Fraunces (SOFT 100) for display, Hanken Grotesk for text.
They are subset and embedded, because GitHub serves README images
without access to outside fonts.

Motion runs once, when each image loads. Words sharpen from a blur on
cubic-bezier(.22,1,.36,1). In the hero, a recording pill listens, then
morphs into the card that holds the intro. Nothing loops.
"""
import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "fonts"
OUT = ROOT / "assets"
EASE = ".22 1 .36 1"
SANS = '-apple-system, "Segoe UI", Helvetica, Arial, sans-serif'

# ---------------------------------------------------------------- copy

LABEL = "Founder, Brand Bakery"
NAME = "Abhishek Kumar"
LINE = "I design brands and build quiet software."
FACTS = [("Studio", "Brand Bakery"), ("Product", "Brivi for Mac"), ("Based in", "India")]
INTRO = [
    "Brand Bakery is my design-first studio in India. We make brands, "
    "websites and AI employees that answer the phone.",
    "I also build Brivi, a private memory and voice typing app for the Mac.",
]

WORK = [
    # slug, name, what it is, kind, link
    ("brivi", "Brivi", "A private memory and voice typing for your Mac. Nothing leaves the device.", "Mac app", "https://brivi.app"),
    ("brand-bakery", "Brand Bakery", "Design-first studio. Brands, websites, stores and AI employees.", "Studio", "https://www.brandbakery.tech"),
    ("ombudy", "Ombudy", "Helps Indian consumers draft and send a formal complaint to a company.", "Web app", None),
    ("bitesquare", "BiteSquare", "A storefront and owner app for cloud kitchens.", "Web app", None),
    ("mcpbouncer", "MCPBouncer", "A directory of MCP servers with deterministic 0 to 100 safety scores.", "Directory", None),
    ("ember", "Ember", "A quiet companion for quitting smoking.", "Open source", "https://github.com/abhishek207/ember"),
]

LINKS = [
    ("brandbakery", "brandbakery.tech", "https://www.brandbakery.tech"),
    ("brivi", "brivi.app", "https://brivi.app"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/abhishek-kumar7/"),
    ("x", "X", "https://x.com/AbhisheKumarA7"),
]

WORK_LABEL = "Selected work"
CLIENTS = "Client work for Pure Prakriti, Mino Bowls, AccelHire, Social Road and Richa Jha."

# ------------------------------------------------------------- palettes

# The hero sits on its own ground. Everything else sits on GitHub's page.
HERO = {
    "light": dict(ground="#F3F3F0", edge="rgba(19,20,22,.08)", ink="#131416", ink2="#45474D",
                  ink3="#6B6E75", card="#FFFFFF", cardLine="rgba(19,20,22,.08)",
                  hud="#141518", onHud="#F3F3F0", rec="#FF453A"),
    "dark": dict(ground="#111214", edge="rgba(255,255,255,.07)", ink="#EEEFEF", ink2="#A8ABB2",
                 ink3="#868991", card="#1A1B1E", cardLine="rgba(255,255,255,.07)",
                 hud="#26272B", onHud="#EEEFEF", rec="#FF453A"),
}
PAGE = {
    "light": dict(ink="#1F2328", ink3="#59636E", line="#D8DEE4"),
    "dark": dict(ink="#F0F6FC", ink3="#9198A1", line="#30363D"),
}

# ---------------------------------------------------------------- fonts

_fonts = {n: TTFont(FONTS / f"{n}.woff2") for n in ("display", "italic", "ui")}


def face(name, family, text):
    font = TTFont(FONTS / f"{name}.woff2")
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    s = subset.Subsetter(opts)
    s.populate(text=text)
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return f'@font-face {{ font-family: {family}; src: url(data:font/woff2;base64,{data}) format("woff2"); }}'


def width(name, s, size):
    f = _fonts[name]
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    return sum(hmtx[cmap[ord(c)]][0] for c in s) * size / f["head"].unitsPerEm


def wrap(name, text, size, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        test = f"{cur} {word}".strip()
        if cur and width(name, test, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = test
    return lines + [cur]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- motion

def hold(delay, dur, a, b, spline=EASE):
    """Hold `a` until `delay`, then ease to `b` over `dur` and stay there."""
    total = delay + dur
    return (f'dur="{total:.3f}s" values="{a};{a};{b}" keyTimes="0;{delay / total:.4f};1" '
            f'calcMode="spline" keySplines="0 0 1 1;{spline}" fill="freeze"')


class Reveal:
    """Blur-to-sharp plus fade, once. The filter is dropped when done so text stays crisp."""

    def __init__(self):
        self.filters = []

    def __call__(self, delay, blur=4, dur=.4):
        fid = f"r{len(self.filters)}"
        self.filters.append(
            f'<filter id="{fid}" x="-10%" y="-60%" width="120%" height="220%">'
            f'<feGaussianBlur stdDeviation="0.01"><animate attributeName="stdDeviation" {hold(delay, dur, blur, 0.01)}/>'
            f"</feGaussianBlur></filter>")
        attr = f'filter="url(#{fid})"'
        inner = (f'<animate attributeName="opacity" {hold(delay, dur, 0, 1)}/>'
                 f'<set attributeName="filter" to="none" begin="{delay + dur:.3f}s"/>')
        return attr, inner

    def defs(self):
        return "\n".join(self.filters)


def svg(w, h, title, style, defs, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
{style}
</style>
<defs>
{defs}
</defs>
{body}
</svg>
"""


# ------------------------------------------------------------------ hero

def hero(mode):
    p = HERO[mode]
    W, H, X = 1200, 520, 76
    r = Reveal()

    # Left column: who.
    left = []
    a, i = r(0, blur=2, dur=.3)
    left.append(f'<text class="u label" x="{X + 2}" y="118" {a}>{esc(LABEL)}{i}</text>')
    x = X
    for n, word in enumerate(NAME.split(" ")):
        a, i = r(.08 + n * .03)
        left.append(f'<text class="d" x="{x:.1f}" y="214" {a}>{esc(word)}{i}</text>')
        x += width("display", word + " ", 92)
    x = X + 2
    for n, word in enumerate(LINE.split(" ")):
        a, i = r(.22 + n * .03, blur=3)
        left.append(f'<text class="i" x="{x:.1f}" y="270" {a}>{esc(word)}{i}</text>')
        x += width("italic", word + " ", 36)
    for n, (k, v) in enumerate(FACTS):
        y = 382 + n * 34
        a, i = r(.6 + n * .06, blur=2, dur=.3)
        left.append(f'<g {a}><text class="u fk" x="{X + 2}" y="{y}">{esc(k)}</text>'
                    f'<text class="u fv" x="{X + 112}" y="{y}">{esc(v)}</text>{i}</g>')
    left.append(f'<line x1="{X + 2}" x2="{X + 520}" y1="342" y2="342" stroke="{p["edge"]}"/>')

    # Right column: a recording pill listens, then morphs into the intro card.
    cx0, cw = 744, 380
    pad, lh, size = 30, 31, 19
    lines = []
    for para in INTRO:
        lines += wrap("ui", para, size, cw - pad * 2)
        lines.append("")
    lines = lines[:-1]
    ch = pad * 2 + lh * len(lines) - (lh - size)
    cy0 = (H - ch) / 2

    pw, ph = 228, 56
    px, py = cx0 + (cw - pw) / 2, cy0 + ch - ph - 24
    listen, morph = .5, 2.1  # pill appears, then morphs at `morph`
    md = .5  # morph length, with a small overshoot near the end

    def m(attr, a, b, over):
        total = morph + md
        k1, k2 = morph / total, (morph + md * .78) / total
        return (f'<animate attributeName="{attr}" dur="{total:.3f}s" values="{a};{a};{over};{b}" '
                f'keyTimes="0;{k1:.4f};{k2:.4f};1" calcMode="spline" '
                f'keySplines="0 0 1 1;{EASE};.4 0 .6 1" fill="freeze"/>')

    card = (
        f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="22" fill="{p["card"]}" stroke="{p["cardLine"]}">'
        + m("x", px, cx0, cx0 - 2) + m("y", py, cy0, cy0 - 3)
        + m("width", pw, cw, cw + 4) + m("height", ph, ch, ch + 5)
        + m("rx", ph / 2, 22, 22)
        + f'<animate attributeName="fill" dur="{morph + .3:.3f}s" values="{p["hud"]};{p["hud"]};{p["card"]}" keyTimes="0;{morph / (morph + .3):.4f};1" fill="freeze"/>'
        + f'<animate attributeName="stroke" dur="{morph + .3:.3f}s" values="{p["hud"]};{p["hud"]};{p["cardLine"]}" keyTimes="0;{morph / (morph + .3):.4f};1" fill="freeze"/>'
        + f'<animate attributeName="opacity" {hold(listen - .2, .2, 0, 1)}/>'
        + "</rect>"
    )

    # Pill contents: record dot and a waveform that settles before the morph.
    bars, n_bars, bw, gap = [], 11, 3, 5
    bx0 = px + 56
    peaks = [10, 18, 26, 14, 22, 30, 16, 24, 12, 20, 8]
    for b in range(n_bars):
        bx = bx0 + b * (bw + gap)
        mid = py + ph / 2
        seq = [4] + [peaks[(b + k * 3) % n_bars] for k in range(6)] + [4]
        hs = ";".join(str(s) for s in seq)
        ys = ";".join(f"{mid - s / 2:.1f}" for s in seq)
        kt = ";".join(f"{k / (len(seq) - 1):.3f}" for k in range(len(seq)))
        span = f'dur="1.4s" begin="{listen + .1:.2f}s" keyTimes="{kt}" calcMode="spline" keySplines="{";".join([".45 0 .55 1"] * (len(seq) - 1))}" fill="freeze"'
        bars.append(f'<rect x="{bx:.1f}" y="{mid - 2}" width="{bw}" height="4" rx="1.5" fill="{p["onHud"]}">'
                    f'<animate attributeName="height" values="{hs}" {span}/>'
                    f'<animate attributeName="y" values="{ys}" {span}/></rect>')
    pill_inner = (
        f'<g><animate attributeName="opacity" dur="{morph:.3f}s" values="0;0;1;1;0" '
        f'keyTimes="0;{listen / morph:.3f};{(listen + .2) / morph:.3f};{(morph - .15) / morph:.3f};1" fill="freeze"/>'
        f'<circle cx="{px + 30}" cy="{py + ph / 2}" r="6" fill="{p["rec"]}"/>'
        f'<text class="u t" x="{px + pw - 22}" y="{py + ph / 2 + 5}" text-anchor="end">0:04</text>'
        + "".join(bars) + "</g>"
    )

    text = []
    for n, ln in enumerate(lines):
        if not ln:
            continue
        a, i = r(morph + .32 + n * .04, blur=3)
        text.append(f'<text class="u intro" x="{cx0 + pad}" y="{cy0 + pad + size - 4 + n * lh}" {a}>{esc(ln)}{i}</text>')

    style = "\n".join([
        face("display", "PD", NAME),
        face("italic", "PI", LINE),
        face("ui", "PU", LABEL + "".join(k + v for k, v in FACTS) + "".join(INTRO) + "0:4"),
        f".d {{ font-family: PD, Georgia, serif; font-size: 92px; fill: {p['ink']}; }}",
        f".i {{ font-family: PI, Georgia, serif; font-style: italic; font-size: 36px; fill: {p['ink2']}; }}",
        f".u {{ font-family: PU, {SANS}; }}",
        f".label {{ font-size: 18px; fill: {p['ink3']}; }}",
        f".fk {{ font-size: 17px; fill: {p['ink3']}; }}",
        f".fv {{ font-size: 17px; fill: {p['ink']}; }}",
        f".intro {{ font-size: {size}px; fill: {p['ink']}; }}",
        f".t {{ font-size: 15px; fill: {p['onHud']}; opacity: .7; font-variant-numeric: tabular-nums; }}",
    ])
    body = f"""<clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{p["ground"]}"/>
{chr(10).join(left)}
{card}
{pill_inner}
{chr(10).join(text)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{p["edge"]}"/>"""
    alt = f"{NAME}. {LINE} {' '.join(INTRO)}"
    return svg(W, H, alt, style, r.defs(), body)


# ------------------------------------------------------------ work rows

def arrow(x, y, color):
    return (f'<path d="M{x} {y + 10}L{x + 10} {y}M{x + 2} {y}H{x + 10}V{y + 8}" fill="none" '
            f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')


def row(item, index, mode, last):
    _, name, what, kind, link = item
    p = PAGE[mode]
    W, H = 1200, 112
    r = Reveal()
    d = .06 * index
    a1, i1 = r(d)
    a2, i2 = r(d + .06, blur=3)
    a3, i3 = r(d + .1, blur=2, dur=.3)
    right = 1192 - (24 if link else 0)
    body = [f'<line x1="0" x2="{W}" y1=".5" y2=".5" stroke="{p["line"]}"/>']
    if last:
        body.append(f'<line x1="0" x2="{W}" y1="{H - .5}" y2="{H - .5}" stroke="{p["line"]}"/>')
    body.append(f'<text class="d" x="4" y="70" {a1}>{esc(name)}{i1}</text>')
    body.append(f'<text class="u w" x="340" y="64" {a2}>{esc(what)}{i2}</text>')
    body.append(f'<g {a3}><text class="u k" x="{right}" y="64" text-anchor="end">{esc(kind)}</text>'
                + (arrow(1180, 49, p["ink3"]) if link else "") + f"{i3}</g>")
    style = "\n".join([
        face("display", "PD", name),
        face("ui", "PU", what + kind),
        f".d {{ font-family: PD, Georgia, serif; font-size: 42px; fill: {p['ink']}; }}",
        f".u {{ font-family: PU, {SANS}; }}",
        f".w {{ font-size: 19px; fill: {p['ink3']}; }}",
        f".k {{ font-size: 17px; fill: {p['ink3']}; }}",
    ])
    return svg(W, H, f"{name}. {what}", style, r.defs(), "\n".join(body))


def label(text, mode, h=72):
    p = PAGE[mode]
    r = Reveal()
    a, i = r(0, blur=2, dur=.3)
    style = "\n".join([face("ui", "PU", text),
                       f".u {{ font-family: PU, {SANS}; font-size: 19px; fill: {p['ink3']}; }}"])
    return svg(1200, h, text, style, r.defs(), f'<text class="u" x="4" y="{h - 22}" {a}>{esc(text)}{i}</text>')


def link_pill(text, mode, index):
    p = PAGE[mode]
    h, size = 36, 15
    w = round(18 + width("ui", text, size) + 10 + 9 + 16)
    r = Reveal()
    a, i = r(.05 * index, blur=2, dur=.3)
    style = "\n".join([face("ui", "PU", text),
                       f".u {{ font-family: PU, {SANS}; font-size: {size}px; fill: {p['ink']}; }}"])
    body = (f'<g {a}><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{h / 2}" fill="none" stroke="{p["line"]}"/>'
            f'<text class="u" x="18" y="{h / 2 + 5}">{esc(text)}</text>'
            + arrow(w - 16 - 9, h / 2 - 4.5, p["ink3"]).replace("+ 10", "+ 9") + f"{i}</g>")
    return svg(w, h, text, style, r.defs(), body), w


# ------------------------------------------------------------- README

def picture(stem, alt, attrs='width="100%"'):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{stem}-dark.svg" />'
            f'<img src="./assets/{stem}-light.svg" {attrs} alt="{esc(alt)}" /></picture>')


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()

    def write(stem, mode, content):
        (OUT / f"{stem}-{mode}.svg").write_text(content)

    widths = {}
    for mode in ("light", "dark"):
        write("hero", mode, hero(mode))
        write("work", mode, label(WORK_LABEL, mode))
        write("clients", mode, label(CLIENTS, mode, h=64))
        for n, item in enumerate(WORK):
            write(f"work-{item[0]}", mode, row(item, n, mode, n == len(WORK) - 1))
        for n, (slug, text, _) in enumerate(LINKS):
            content, w = link_pill(text, mode, n)
            widths[slug] = w
            write(f"link-{slug}", mode, content)

    md = [picture("hero", f"{NAME}. {LINE} {' '.join(INTRO)}"), "", "<p>"]
    for slug, text, url in LINKS:
        attrs = 'height="36" width="%d"' % widths[slug]
        md.append(f'  <a href="{url}">{picture("link-" + slug, text, attrs)}</a>')
    md += ["</p>", "", picture("work", WORK_LABEL), ""]
    for slug, name, what, kind, link in WORK:
        img = picture(f"work-{slug}", f"{name}: {what}")
        md.append(f'<a href="{link}">{img}</a>' if link else img)
    md += ["", picture("clients", CLIENTS), ""]
    (ROOT / "README.md").write_text("\n".join(md))

    total = sum(f.stat().st_size for f in OUT.glob("*.svg"))
    print(f"{len(list(OUT.glob('*.svg')))} images, {total / 1024:.0f} KB, README.md written")


if __name__ == "__main__":
    main()
