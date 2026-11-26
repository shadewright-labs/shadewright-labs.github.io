"""Writes the wide and narrow product diagrams. Run from the repository root: python3 -I scripts/gen-diagram.py assets"""
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]

NIGHT, TILE, BONE, MUTED, EDGE = "#08060E", "#14111C", "#EFE9DC", "#BBB4C5", "#3A3447"
AMBER = "#F0B86A"
SW = {"stroke": "#A879FF", "text": "#A879FF"}
SC = {"stroke": "#2DD4BF", "text": "#2DD4BF"}
NL = {"stroke": "#8B3DFF", "text": "#B794FF"}

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


def card(out, x, y, w, h, stroke, title, lines, accent, pad, steps, size, tagsize, label=None):
    out.append(f'  <rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" stroke="{stroke}"/>')
    b = y + steps[0]
    i = 0
    if label:
        out.append(f'  <text class="caps" x="{x + pad}" y="{b}" style="fill:{label[1]}">{label[0]}</text>')
        i += 1
    out.append(f'  <text class="t" x="{x + pad}" y="{y + steps[i]}">{escape(title)}</text>')
    for k, (kind, text) in enumerate(lines):
        line(out, kind, x + pad, y + steps[i + 1 + k], text, accent, size, tagsize)


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
        card(out, x, 62, cw, 92, BONE, title, lines, col["text"], 16, [31, 56, 78], S, SUB)
        out.append(f'  <path class="ln" d="M{c} 154V222" stroke="{BONE}"/>')
    # Product panels
    PY, PH = 222, 650
    rows = [314, 454, 594, 734]
    CH = 116
    for (name, sub, col, cards, note), x in zip(PANELS, px):
        framed(out, f"c-{name.lower()}", x, PY, pw, PH, col["stroke"], 7)
        out.append(f'  <text class="serif" x="{x + 22}" y="{PY + 46}">{name}</text>')
        out.append(f'  <text class="caps" x="{x + 22}" y="{PY + 72}" style="fill:{col["text"]}">{sub}</text>')
        cx = x + 18
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
        card(body, cx, y, cw, 104, BONE, title, lines, col["text"], pad, [25, 49, 71, 93], S, SUB, label=(lab, col["text"]))
    y = 456
    CH, GAP = 114, 24
    gaps = {0: LINKS[0], 1: LINKS[1]}
    for k, (name, sub, col, cards, note) in enumerate(PANELS):
        n = len(cards)
        h = 84 + n * CH + (n - 1) * GAP + (88 if note else 18)
        framed(body, f"c-{name.lower()}", 1, y, 358, h, col["stroke"], 7)
        body.append(f'  <text class="serif" x="16" y="{y + 40}">{name}</text>')
        body.append(f'  <text class="caps" x="16" y="{y + 64}" style="fill:{col["text"]}">{sub}</text>')
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
