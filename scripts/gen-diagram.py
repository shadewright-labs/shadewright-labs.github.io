"""Writes the wide and narrow product diagrams. Run from the repository root: python3 -I scripts/gen-diagram.py assets"""
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]

NIGHT, TILE, BONE, MUTED, EDGE = "#08060E", "#14111C", "#EFE9DC", "#BBB4C5", "#3A3447"
AMBER = "#F0B86A"
SW = {"stroke": "#A879FF", "text": "#A879FF"}
SC = {"stroke": "#2DD4BF", "text": "#2DD4BF"}
NL = {"stroke": "#8B3DFF", "text": "#B794FF"}

# Product glyphs: (viewBox tuple (x, y, w, h), list of (fill, fill_rule, d)).
# The paths are taken verbatim from each product's 64x64 glyph SVG.
GLYPHS = {
    "shadewright": (
        (0, 0, 64, 64),
        [
            ("#08060E", None,
             "M32 4C36.5 6.7 40.8 10.3 44 14.5L46 18.6 58 11.5C54.8 17.2 49.6 21.2 48 25.5L51.8 30.3"
             "Q53.3 32.4 50.8 34.2L48.2 36.2 56.5 39.1C51.4 41.6 51.6 46.8 47.2 50.6C42.7 54.7 37.1 55.8 32 60"
             "C26.9 55.8 21.3 54.7 16.8 50.6C12.4 46.8 12.6 41.6 7.5 39.1L15.8 36.2 13.2 34.2"
             "Q10.7 32.4 12.2 30.3L16 25.5C14.4 21.2 9.2 17.2 6 11.5L18 18.6 20 14.5C23.2 10.3 27.5 6.7 32 4Z"),
            ("#A879FF", "evenodd",
             "M32 4C36.5 6.7 40.8 10.3 44 14.5L46 18.6 58 11.5C54.8 17.2 49.6 21.2 48 25.5L51.8 30.3"
             "Q53.3 32.4 50.8 34.2L48.2 36.2 56.5 39.1C51.4 41.6 51.6 46.8 47.2 50.6C42.7 54.7 37.1 55.8 32 60"
             "C26.9 55.8 21.3 54.7 16.8 50.6C12.4 46.8 12.6 41.6 7.5 39.1L15.8 36.2 13.2 34.2"
             "Q10.7 32.4 12.2 30.3L16 25.5C14.4 21.2 9.2 17.2 6 11.5L18 18.6 20 14.5C23.2 10.3 27.5 6.7 32 4Z "
             "M32 7.2C28.2 9.5 25 12.3 22 15.8L18.4 24.9C22.6 19.7 27.2 15.2 32 12.8"
             "C36.8 15.2 41.4 19.7 45.6 24.9L42 15.8C39 12.3 35.8 9.5 32 7.2Z "
             "M9.3 14.9 17.5 20.8 16.9 24Z M54.7 14.9 46.5 20.8 47.1 24Z "
             "M32 17.4C26.4 19.8 20.6 26 14.7 31.5Q13.7 32.4 15.4 33.6C19.1 36.4 24.2 38.7 25.5 43.4"
             "C23.5 41.4 20.8 39.5 18.4 37.9L12.5 40C15.2 42.4 15.4 45.6 19.2 48.7C23 52 27.4 53.5 32 57"
             "C36.6 53.5 41 52 44.8 48.7C48.6 45.6 48.8 42.4 51.5 40L45.6 37.9C43.2 39.5 40.5 41.4 38.5 43.4"
             "C39.8 38.7 44.9 36.4 48.6 33.6Q50.3 32.4 49.3 31.5C43.4 26 37.6 19.8 32 17.4Z"),
            ("#A879FF", None,
             "M23.5 28C22.2 37 31.4 39.5 38.4 44.1C43.8 47.7 44 52.1 39.8 55.3"
             "C40.5 51.5 37.9 48.9 32.3 45.8C23.1 40.6 19.5 34.1 23.5 28Z "
             "M28.8 45C34.8 48.9 36.4 54 32 58L29.2 55.3C33 52.1 31.6 48.7 28.8 45Z"),
            ("#EFE9DC", None,
             "M23 24.9Q28.1 25.1 30.3 29.4Q25.1 29 23 24.9Z M41 24.9Q35.9 25.1 33.7 29.4Q38.9 29 41 24.9Z"),
        ],
    ),
    "sablecourt": (
        (0, 0, 64, 64),
        [
            ("#08060E", None,
             "M32 4 36.8 12.7 44 8.3 44.5 17.3 47 20.9 58 15.1 50 28.1 52.4 34.8 48 38 55 41.4 48 50.7 "
             "32 60 16 50.7 9 41.4 16 38 11.6 34.8 14 28.1 6 15.1 17 20.9 19.5 17.3 20 8.3 27.2 12.7Z"),
            ("#EFE9DC", "evenodd",
             "M32 4 36.8 12.7 44 8.3 44.5 17.3 47 20.9 58 15.1 50 28.1 52.4 34.8 48 38 55 41.4 48 50.7 "
             "32 60 16 50.7 9 41.4 16 38 11.6 34.8 14 28.1 6 15.1 17 20.9 19.5 17.3 20 8.3 27.2 12.7Z "
             "M32 10.2 29 16.3 23 13.6 23.2 18 32 15.6 40.8 18 41 13.6 35 16.3Z "
             "M9.9 17.7 17.5 23.1 15.8 26Z M54.1 17.7 46.5 23.1 48.2 26Z "
             "M32 19.4 22.2 22.3 18.3 27.5 15.5 33.7 23.1 39.4 32 44.9 40.9 39.4 48.5 33.7 45.7 27.5 41.8 22.3Z "
             "M17.9 40.2 13.6 42.3 17.8 48.4 28.7 54.8 24.2 47.2Z "
             "M46.1 40.2 50.4 42.3 46.2 48.4 35.3 54.8 39.8 47.2Z "
             "M27.3 45.6 32 54.6 36.7 45.6 32 48.1Z"),
            ("#2DD4BF", None,
             "M21.3 26.4 29.2 28.6 29.6 31.5 24.2 30.1Z M42.7 26.4 34.8 28.6 34.4 31.5 39.8 30.1Z "
             "M32 13.2 35.2 17.2 32 20.5 28.8 17.2Z"),
        ],
    ),
    "nightloom": (
        (0, 0, 64, 64),
        [
            ('#08060E', None,
             'M32 9C24 9 17 8 10 4Q8 11.5 11 18.5C8 25 6 30 6 35C6 44 12 51 19 54Q26.5 57 32 60Q37.5 57 45 54C52 51 58 44 58 35C58 30 56 25 53 18.5Q56 11.5 54 4C47 8 40 9 32 9Z'),
            ('#8B3DFF', 'evenodd',
             'M32 9C24 9 17 8 10 4Q8 11.5 11 18.5C8 25 6 30 6 35C6 44 12 51 19 54Q26.5 57 32 60Q37.5 57 45 54C52 51 58 44 58 35C58 30 56 25 53 18.5Q56 11.5 54 4C47 8 40 9 32 9Z M32 31.08Q28 26.35 22 26.35C17 26.35 12.7 27.4 10.45 28.95Q9.39 31.68 9.075 34.9C8.82 42 13.77 48.33 20.19 51.17Q26.5 53.75 32 56.58Q37.5 53.75 43.81 51.17C50.23 48.33 55.18 42 54.925 34.9Q54.61 31.68 53.55 28.95C51.3 27.4 47 26.35 42 26.35Q36 26.35 32 31.08Z M32 12.035Q26.9 12.055 23 11.465C23.7 16.25 26.65 20.65 28.05 23.28Q29.65 25.65 32 26.5Q34.35 25.65 35.95 23.28C37.35 20.65 40.3 16.25 41 11.465Q37.1 12.055 32 12.035Z M12.27 8.59Q15.23 9.76 19.65 10.97C19.99 16 22.49 20.6 24.62 23.31Q17.9 22.64 11.67 24.88C12.31 23.33 13.72 21.05 13.995 19.33Q14.27 18.3 13.94 17.64Q12.2 13.4 12.27 8.59Z M51.73 8.59Q48.77 9.76 44.35 10.97C44.01 16 41.51 20.6 39.38 23.31Q46.1 22.64 52.33 24.88C51.69 23.33 50.28 21.05 50.005 19.33Q49.73 18.3 50.06 17.64Q51.8 13.4 51.73 8.59Z M32 39.79Q29.28 41 28.84 43.5Q29.77 46.5 32 48.81Q34.23 46.5 35.16 43.5Q34.72 41 32 39.79Z'),
            ('#B794FF', None,
             'M16.9 33Q21 33 26.1 37.5L25.2 40.9Q19.6 40.9 16.9 37Z M47.1 33Q43 33 37.9 37.5L38.8 40.9Q44.4 40.9 47.1 37Z'),
        ],
    ),
}

OPS = [
    ("SHADEWRIGHT", SW, "Pull request review", [("d", "On the Git host, under branch rules"), ("p", "A person reviews and merges")]),
    ("SABLECOURT", SC, "sablectl and the web UI", [("d", "Workloads, Conclaves, approvals"), ("p", "A person approves gated actions")]),
    ("NIGHTLOOM", NL, "Nightloom view", [("d", "Sessions and waiting decisions"), ("d", "Not released")]),
]

PANELS = [
    ("Shadewright", "THE GUARDIAN · EARLY RELEASES", SW, [
        ("Analyzer", [("d", "Groups symptoms into incidents"), ("d", "Reads the cluster, no Git credential"), ("a", "A model's answer is only a proposal")]),
        ("Executor", [("d", "Checks each proposal against policy"), ("d", "Opens the pull request with the fix"), ("a", "Holds the Git App, reads no Secrets")]),
        ("GitOps repository and Flux", [("d", "Your branch rules decide what merges"), ("d", "Flux applies the merged change"), ("a", "The only path to a workload")]),
        ("Verifier", [("d", "Samples the pods of the rollout"), ("d", "Off by default for now"), ("a", "No model, no Git App, no Secrets")]),
    ], None),
    ("Sablecourt", "THE COURT · NOT RELEASED YET", SC, [
        ("Control plane", [("d", "Runs what the manifests declare"), ("d", "On a workstation or a cluster"), ("a", "Audit chain, not anchored yet")]),
        ("Conclaves (agent councils)", [("d", "Rooms where agents work together"), ("d", "and share redacted artifacts"), ("a", "Message limits stop runaway loops")]),
        ("Managed workloads", [("d", "Rootless containers or OS sandbox"), ("a", "No upstream API keys or Git tokens"), ("x", "gVisor or Kata on Kubernetes")]),
        ("Three gates", [("d", "Model gate: cost per task and day"), ("d", "Data and action gate: allowlists"), ("p", "Approval queue: a person confirms")]),
    ], None),
    ("Nightloom", "THE WATCHER · NOT RELEASED", NL, [
        ("One view", [("d", "Coding sessions across terminals"), ("d", "and machines"), ("a", "See what's running")]),
        ("Decisions waiting", [("d", "Decisions waiting for the operator"), ("d", "in the same view"), ("p", "Know what needs you")]),
    ], ("Not released.", "No public code yet.")),
]

LINKS = [
    ("1", AMBER, "Code-fault incident handoff, one way", ("p", "A person approves each send"),
     "Sablecourt intake: built", ("PLANNED", "Shadewright sender")),
    ("2", SC["stroke"], "Read-only observer feed", ("d", "Snapshot, live stream and task output"),
     "Sablecourt side: built", ("NOT BUILT", "Nightloom side")),
]

DESC = (
    "The operator uses each product through one surface: a pull request review for Shadewright, sablectl and the web UI "
    "for Sablecourt, and the Nightloom view, which is not released. Shadewright's analyzer, executor, GitOps repository "
    "with Flux, and verifier form one chain; Sablecourt's control plane, Conclaves, managed workloads and three gates "
    "form another; Nightloom has one view and the decisions waiting. Two connections join the products. One: a one-way "
    "code-fault incident handoff from Shadewright to Sablecourt, approved by a person for each send; Sablecourt's intake "
    "is built and Shadewright's sender is planned. Two: a read-only observer feed from Sablecourt to Nightloom; "
    "Sablecourt's side is built and Nightloom's is not. Solid lines are built, dashed lines and tags are not built yet, "
    "and amber marks what a person decides."
)


def style(small, title, head, sub):
    return f"""  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: {small}px; fill: {BONE}; }}
    .serif {{ font-family: "Iowan Old Style", Georgia, serif; font-size: {head}px; }}
    .caps {{ font-size: {sub}px; letter-spacing: 1.5px; }}
    .t {{ font-size: {title}px; font-weight: 600; }}
    .d {{ fill: {MUTED}; }}
    .p {{ fill: {AMBER}; }}
    .x {{ fill: {MUTED}; font-style: italic; }}
    .tag {{ font-size: {sub}px; letter-spacing: 1.2px; fill: {MUTED}; }}
    .tile {{ fill: {TILE}; }}
    .node {{ fill: {NIGHT}; stroke-width: 1.5; }}
    .ln {{ fill: none; stroke-width: 1.5; }}
    .dash {{ stroke-dasharray: 6 5; }}
  </style>"""


def markers():
    out = ["  <defs>"]
    for name, col in (("amber", AMBER), ("jade", SC["stroke"])):
        out.append(f'    <marker id="arrow-{name}" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{col}"/></marker>')
    return out


def framed(out, cid, x, y, w, h, stroke, bar, r=14):
    """A tile panel with a thick bar along its rounded top edge."""
    out.append(f'  <clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
    out.append(f'  <rect class="tile" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>')
    out.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{bar}" fill="{stroke}" clip-path="url(#{cid})"/>')
    out.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="{stroke}" stroke-width="1.5"/>')


def tag(out, x, base, word, size, x_text_size):
    """Dashed 'not built yet' tag; returns the x where following text starts."""
    w = round(len(word.replace(' ', '')) * size * 0.72 + word.count(' ') * size * 0.4 + 14)
    out.append(f'  <rect x="{x}" y="{base - size - 1}" width="{w}" height="{size + 7}" rx="{(size + 7) / 2}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    out.append(f'  <text class="tag" x="{x + 7}" y="{base}">{word}</text>')
    return x + w + 8


def line(out, kind, x, base, text, accent, size, tagsize):
    if kind == "x":
        nx = tag(out, x, base, "PLANNED", tagsize, size)
        out.append(f'  <text class="x" x="{nx}" y="{base}">{escape(text)}</text>')
    elif kind == "a":
        out.append(f'  <text x="{x}" y="{base}" fill="{accent}" style="fill:{accent}">{escape(text)}</text>')
    else:
        out.append(f'  <text class="{kind}" x="{x}" y="{base}">{escape(text)}</text>')


def glyph(out, key, x, y, height):
    """Draw a product glyph scaled to height while preserving aspect ratio; returns rendered width."""
    (vx, vy, vw, vh), paths = GLYPHS[key]
    scale = height / vh
    width = height * vw / vh
    tf = f"translate({x:g} {y:g}) scale({scale:.4f})"
    if vx or vy:
        tf += f" translate({-vx:g} {-vy:g})"
    out.append(f'  <g aria-hidden="true" transform="{tf}">')
    for fill, rule, d in paths:
        extra = f' fill-rule="{rule}"' if rule else ""
        out.append(f'    <path fill="{fill}"{extra} d="{d}"/>')
    out.append('  </g>')
    return width


def card(out, x, y, w, h, stroke, title, lines, accent, pad, steps, size, tagsize, label=None, glyph_key=None, title_size=16):
    out.append(f'  <rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" stroke="{stroke}"/>')
    b = y + steps[0]
    i = 0
    tx = x + pad
    head_tx = tx
    if glyph_key:
        cap_t = round(title_size * 0.72)
        gap = 10
        if label:
            # Align glyph with the two-line header (label + title) on the baseline grid; body lines stay full width.
            cap_l = round(tagsize * 0.72)
            gh = round(cap_t * 2.5)
            gy = round((y + steps[0] - cap_l + y + steps[1] - gh) / 2)
            gw = glyph(out, glyph_key, x + pad, gy, gh)
            head_tx = x + pad + round(gw) + gap
        else:
            # Align glyph with the title and first body line; shift all lines right for a clean text column.
            gh = round(cap_t * 2.5)
            gy = round((y + steps[0] - cap_t + y + steps[1] - gh) / 2)
            gw = glyph(out, glyph_key, x + pad, gy, gh)
            tx = x + pad + round(gw) + gap
            head_tx = tx
    if label:
        out.append(f'  <text class="caps" x="{head_tx}" y="{b}" style="fill:{label[1]}">{label[0]}</text>')
        i += 1
    out.append(f'  <text class="t" x="{head_tx}" y="{y + steps[i]}">{escape(title)}</text>')
    for k, (kind, text) in enumerate(lines):
        line(out, kind, tx, y + steps[i + 1 + k], text, accent, size, tagsize)


def legend(out, items_y, x0, size, tagsize, vertical=False, step=0):
    entries = []
    x, y = x0, items_y
    def next_pos(width):
        nonlocal x, y
        pos = (x, y)
        if vertical:
            y += step
        else:
            x += width
        return pos
    px, py = next_pos(140)
    out.append(f'  <path class="ln" d="M{px} {py - 5}H{px + 34}" stroke="{BONE}"/>')
    out.append(f'  <text class="d" x="{px + 44}" y="{py}">built</text>')
    px, py = next_pos(282)
    out.append(f'  <path class="ln dash" d="M{px} {py - 5}H{px + 34}" stroke="{BONE}"/>')
    nx = tag(out, px + 44, py, "PLANNED", tagsize, size)
    out.append(f'  <text class="d" x="{nx}" y="{py}">not built yet</text>')
    px, py = next_pos(212)
    out.append(f'  <path class="ln" d="M{px} {py - 5}H{px + 34}" stroke="{AMBER}"/>')
    out.append(f'  <text class="d" x="{px + 44}" y="{py}">a person decides</text>')
    px, py = next_pos(300)
    out.append(f'  <rect x="{px + 4}" y="{py - 17}" width="26" height="22" rx="11" fill="{NIGHT}" stroke="{BONE}" stroke-width="1.2"/>')
    out.append(f'  <text class="t" x="{px + 17}" y="{py - 1}" text-anchor="middle" style="font-size:{size}px">1</text>')
    out.append(f'  <text class="d" x="{px + 44}" y="{py}">contract between products</text>')


def pill(out, cx, cy, num, col, size):
    out.append(f'  <rect x="{cx - 15}" y="{cy - 12}" width="30" height="24" rx="12" fill="{NIGHT}" stroke="{col}" stroke-width="1.5"/>')
    out.append(f'  <text class="t" x="{cx}" y="{cy + 5}" text-anchor="middle" style="font-size:{size}px">{num}</text>')


def header(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">',
            '  <title id="t">How the Shadewright Labs products fit together</title>',
            f'  <desc id="d">{escape(DESC)}</desc>']


def wide():
    W, H = 1220, 1082
    S, T, HEAD, SUB = 14, 16, 24, 14
    out = header(W, H)
    out += markers() + ["  </defs>", style(S, T, HEAD, SUB), f'  <rect width="{W}" height="{H}" fill="#0B0810"/>']
    px = [1, 427, 853]
    pw = 366
    cw = 330
    centers = [p + pw / 2 for p in px]
    # Operator band
    framed(out, "c-op", 1, 1, 1218, 176, BONE, 6)
    out.append(f'  <text class="serif" x="26" y="44">The operator</text>')
    out.append(f'  <text class="caps d" x="190" y="43">ONE PERSON, THREE SURFACES</text>')
    for (lab, col, title, lines), c in zip(OPS, centers):
        x = c - cw / 2
        card(out, x, 62, cw, 92, BONE, title, lines, col["text"], 16, [31, 56, 78], S, SUB, glyph_key=lab.lower(), title_size=T)
        out.append(f'  <path class="ln" d="M{c} 154V222" stroke="{BONE}"/>')
    # Product panels
    PY, PH = 222, 650
    rows = [314, 454, 594, 734]
    CH = 116
    cap_head = round(HEAD * 0.72)
    panel_gh = round(cap_head * 2.35)
    panel_gap = 10
    for (name, sub, col, cards, note), x in zip(PANELS, px):
        framed(out, f"c-{name.lower()}", x, PY, pw, PH, col["stroke"], 7)
        cx = x + 18
        name_y, sub_y = PY + 46, PY + 72
        gy = round((name_y - cap_head + sub_y - panel_gh) / 2)
        gw = glyph(out, name.lower(), cx, gy, panel_gh)
        tx = cx + round(gw) + panel_gap
        out.append(f'  <text class="serif" x="{tx}" y="{name_y}">{name}</text>')
        out.append(f'  <text class="caps" x="{tx}" y="{sub_y}" style="fill:{col["text"]}">{sub}</text>')
        for i, (title, lines) in enumerate(cards):
            y = rows[i]
            if i:
                out.append(f'  <path class="ln" d="M{x + pw / 2} {rows[i - 1] + CH}V{y}" stroke="{col["stroke"]}"/>')
            card(out, cx, y, cw, CH, col["stroke"], title, lines, col["text"], 16, [31, 56, 78, 100], S, SUB)
        if note:
            ny = rows[len(cards)] + 40
            out.append(f'  <text class="d" x="{x + pw / 2}" y="{ny}" text-anchor="middle" style="font-size:15px">{note[0]}</text>')
            out.append(f'  <text class="d" x="{x + pw / 2}" y="{ny + 22}" text-anchor="middle" style="font-size:15px">{note[1]}</text>')
    # Connections in the gutters, at the middle of the first row
    my = rows[0] + CH / 2
    a_end = px[0] + 18 + cw
    b_start = px[1] + 18
    gm = (a_end + b_start) / 2
    out.append(f'  <path class="ln dash" d="M{a_end} {my}H{gm - 15}" stroke="{AMBER}"/>')
    out.append(f'  <path class="ln" d="M{gm + 15} {my}H{b_start}" stroke="{AMBER}" marker-end="url(#arrow-amber)"/>')
    pill(out, gm, my, "1", AMBER, S)
    b_end = px[1] + 18 + cw
    c_start = px[2] + 18
    gm2 = (b_end + c_start) / 2
    out.append(f'  <path class="ln" d="M{b_end} {my}H{gm2 - 15}" stroke="{SC["stroke"]}"/>')
    out.append(f'  <path class="ln dash" d="M{gm2 + 15} {my}H{c_start}" stroke="{SC["stroke"]}" marker-end="url(#arrow-jade)"/>')
    pill(out, gm2, my, "2", SC["stroke"], S)
    # Connection labels in their own row
    LY = PY + PH + 28
    for (num, col, title, l2, built, planned), x in zip(LINKS, [1, 617]):
        out.append(f'  <rect class="tile" x="{x}" y="{LY}" width="602" height="104" rx="12" stroke="{EDGE}" stroke-width="1.5"/>')
        pill(out, x + 36, LY + 30, num, col, S)
        out.append(f'  <text class="t" x="{x + 66}" y="{LY + 36}">{escape(title)}</text>')
        line(out, l2[0], x + 66, LY + 61, l2[1], col, S, SUB)
        out.append(f'  <text x="{x + 66}" y="{LY + 85}">{escape(built)}</text>')
        nx = tag(out, x + 270, LY + 85, planned[0], SUB, S)
        out.append(f'  <text class="x" x="{nx}" y="{LY + 85}">{escape(planned[1])}</text>')
    legend(out, LY + 104 + 44, 1, S, SUB)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def narrow():
    W = 360
    S, T, HEAD, SUB = 15, 16, 21, 14
    out = []
    body = []
    cw, cx, pad = 334, 13, 14
    # Operator band: three surface cards, each named for its product
    framed(body, "c-op", 1, 1, 358, 427, BONE, 6)
    body.append(f'  <text class="serif" x="16" y="38">The operator</text>')
    body.append(f'  <text class="caps d" x="16" y="62">ONE PERSON, THREE SURFACES</text>')
    for i, (lab, col, title, lines) in enumerate(OPS):
        y = 76 + i * 116
        card(body, cx, y, cw, 104, BONE, title, lines, col["text"], pad, [25, 49, 71, 93], S, SUB, label=(lab, col["text"]), glyph_key=lab.lower(), title_size=T)
    y = 456
    CH, GAP = 114, 24
    gaps = {0: LINKS[0], 1: LINKS[1]}
    cap_head = round(HEAD * 0.72)
    panel_gh = round(cap_head * 2.35)
    panel_gap = 10
    for k, (name, sub, col, cards, note) in enumerate(PANELS):
        n = len(cards)
        h = 84 + n * CH + (n - 1) * GAP + (88 if note else 18)
        framed(body, f"c-{name.lower()}", 1, y, 358, h, col["stroke"], 7)
        name_y, sub_y = y + 40, y + 64
        gy = round((name_y - cap_head + sub_y - panel_gh) / 2)
        gw = glyph(body, name.lower(), cx, gy, panel_gh)
        tx = cx + round(gw) + panel_gap
        body.append(f'  <text class="serif" x="{tx}" y="{name_y}">{name}</text>')
        body.append(f'  <text class="caps" x="{tx}" y="{sub_y}" style="fill:{col["text"]}">{sub}</text>')
        for i, (title, lines) in enumerate(cards):
            cy = y + 84 + i * (CH + GAP)
            if i:
                body.append(f'  <path class="ln" d="M180 {cy - GAP}V{cy}" stroke="{col["stroke"]}"/>')
            card(body, cx, cy, cw, CH, col["stroke"], title, lines, col["text"], pad, [30, 55, 77, 99], S, SUB)
        if note:
            ny = y + 84 + n * CH + (n - 1) * GAP + 42
            body.append(f'  <text class="d" x="180" y="{ny}" text-anchor="middle">{note[0]} {note[1]}</text>')
        y += h
        if k in gaps:
            num, lcol, title, l2, built, planned = gaps[k]
            top, bot = y, y + 132
            mid = top + 66
            if k == 0:  # planned sender above, built intake below
                body.append(f'  <path class="ln dash" d="M30 {top}V{mid - 12}" stroke="{lcol}"/>')
                body.append(f'  <path class="ln" d="M30 {mid + 12}V{bot}" stroke="{lcol}" marker-end="url(#arrow-amber)"/>')
            else:  # built side above, Nightloom side below
                body.append(f'  <path class="ln" d="M30 {top}V{mid - 12}" stroke="{lcol}"/>')
                body.append(f'  <path class="ln dash" d="M30 {mid + 12}V{bot}" stroke="{lcol}" marker-end="url(#arrow-jade)"/>')
            pill(body, 30, mid, num, lcol, S)
            body.append(f'  <text class="t" x="60" y="{top + 30}">{escape(title if k else "Code-fault incident handoff")}</text>')
            line(body, l2[0], 60, top + 53, l2[1] if k else "One way; a person approves each send", lcol, S, SUB)
            body.append(f'  <text x="60" y="{top + 76}">{escape(built)}</text>')
            nx = tag(body, 60, top + 101, planned[0], SUB, S)
            body.append(f'  <text class="x" x="{nx}" y="{top + 101}">{escape(planned[1])}</text>')
            y = bot
    ly = y + 44
    legend(body, ly, 16, S, SUB, vertical=True, step=34)
    H = ly + 3 * 34 + 24
    out = header(W, H) + markers() + ["  </defs>", style(S, T, HEAD, SUB), f'  <rect width="{W}" height="{H}" fill="#0B0810"/>'] + body + ["</svg>"]
    return "\n".join(out) + "\n"


open(f"{OUT}/products-diagram-wide.svg", "w").write(wide())
open(f"{OUT}/products-diagram-narrow.svg", "w").write(narrow())
