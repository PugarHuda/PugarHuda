"""Generate a pixel-art SVG banner for the GitHub profile README."""
import random
import sys

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    " ": ["....."] * 7,
}

TROPHY = [
    "..########..",
    "##.######.##",
    "#..######..#",
    "#..######..#",
    ".#.######.#.",
    "..########..",
    "...######...",
    ".....##.....",
    ".....##.....",
    "....####....",
    "...######...",
    "...######...",
]

# PICO-8 palette
BG, NAVY, PURPLE = "#1d2b53", "#0b1229", "#7e2553"
WHITE, YELLOW, ORANGE = "#fff1e8", "#ffec27", "#ffa300"
GREEN, BLUE, PINK = "#00e436", "#29adff", "#ff77a8"

W, H = 900, 260


def text_width(text, scale):
    return (len(text) * 6 - 1) * scale


def bitmap_path(rows, x0, y0, s):
    """One path of s-sized squares for every '#' cell (keeps the SVG small)."""
    return "".join(
        f"M{x0 + c * s} {y0 + r * s}h{s}v{s}h-{s}z"
        for r, row in enumerate(rows)
        for c, ch in enumerate(row)
        if ch == "#"
    )


def text_path(text, x0, y0, s):
    return "".join(bitmap_path(FONT[ch], x0 + i * 6 * s, y0, s) for i, ch in enumerate(text))


def centered(text, s):
    return (W - text_width(text, s)) // 2


def colored_sprite(rows, palette, x0, y0, s):
    """Multi-colour sprite: one path per palette letter."""
    return "".join(
        f'<path fill="{color}" d="{bitmap_path(["".join("#" if ch == k else "." for ch in r) for r in rows], x0, y0, s)}"/>'
        for k, color in palette.items()
    )


RUNNER_TOP = [
    "...BBBB...",
    "..BBBBBB..",
    "..BSSSSB..",
    "..BSKSKB..",
    "..BSSSSB..",
    "...BBBB...",
    ".BBBBBBBB.",
    "S.BBBBBB.S",
    "..BBBBBB..",
]
RUNNER_LEGS = (
    ["..NN..NN..", ".NN....NN.", "KK......KK"],
    ["...NNNN...", "...NNNN...", "...KKKK..."],
)


def divider(out):
    w, h, s = 900, 64, 4
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'shape-rendering="crispEdges" role="img" aria-label="Pixel runner collecting coins">',
        "<style>"
        "@keyframes run{from{transform:translateX(-40px)}to{transform:translateX(940px)}}"
        "@keyframes f1{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes f2{0%,49%{opacity:0}50%,100%{opacity:1}}"
        "@keyframes coin{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
        ".r{animation:run 9s linear infinite}"
        ".a{animation:f1 .3s infinite}.b{animation:f2 .3s infinite}"
        ".k{animation:coin 1s steps(2) infinite}"
        "</style>",
    ]
    ground = h - 12
    for x in range(0, w, 12):
        p.append(f'<rect x="{x}" y="{ground}" width="12" height="4" fill="{GREEN if x % 24 else "#008751"}"/>')
        p.append(f'<rect x="{x}" y="{ground + 4}" width="12" height="8" fill="#ab5236"/>')
    for i, x in enumerate(range(90, w, 150)):
        p.append(
            f'<g class="k" style="animation-delay:{i * 0.2:.1f}s">'
            f'<rect x="{x}" y="{ground - 30}" width="12" height="16" fill="{YELLOW}"/>'
            f'<rect x="{x + 4}" y="{ground - 26}" width="4" height="8" fill="{ORANGE}"/></g>'
        )
    pal = {"B": BLUE, "S": "#ffccaa", "K": "#000000", "N": NAVY}
    top_y = ground - 12 * s
    body = colored_sprite(RUNNER_TOP, pal, 0, top_y, s)
    legs = [colored_sprite(l, pal, 0, top_y + 9 * s, s) for l in RUNNER_LEGS]
    p.append(f'<g class="r">{body}<g class="a">{legs[0]}</g><g class="b">{legs[1]}</g></g>')
    p.append("</svg>")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(p))


def cabinet(out):
    w, h, s = 900, 190, 4
    tiers = [  # (count, main, shade) by rank: gold, silver, bronze, other wins
        (2, YELLOW, ORANGE),
        (3, "#c2c3c7", "#83769c"),
        (3, "#e08a3c", "#ab5236"),
        (6, BLUE, "#065ab5"),
    ]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'shape-rendering="crispEdges" role="img" '
        'aria-label="Trophy cabinet: 2 gold, 3 silver, 3 bronze and 6 other wins. Level 14">',
        "<style>@keyframes sp{0%,70%,100%{opacity:0}80%{opacity:1}}.g{animation:sp 2s infinite}</style>",
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>',
        f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" fill="{BG}"/>',
        f'<path fill="{YELLOW}" d="{text_path("TROPHY CABINET", 32, 26, 3)}"/>',
        f'<path fill="{GREEN}" d="{text_path("LV 14", w - 32 - text_width("LV 14", 3), 26, 3)}"/>',
    ]
    shelf_y = 150
    p.append(f'<rect x="24" y="{shelf_y}" width="{w - 48}" height="10" fill="#ab5236"/>')
    p.append(f'<rect x="24" y="{shelf_y + 10}" width="{w - 48}" height="6" fill="#7e2553"/>')
    x, step = 36, 60
    for count, main, shade in tiers:
        for _ in range(count):
            y = shelf_y - 12 * s
            p.append(f'<path fill="{main}" d="{bitmap_path(TROPHY, x, y, s)}"/>')
            p.append(f'<path fill="{shade}" d="{bitmap_path([r[:3] for r in TROPHY], x, y, s)}"/>')
            if main == YELLOW:
                p.append(f'<rect class="g" x="{x + 6 * s}" y="{y + 1 * s}" width="{s}" height="{s}" fill="{WHITE}"/>')
            x += step
    p.append("</svg>")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(p))


def main(out):
    random.seed(14)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        'shape-rendering="crispEdges" role="img" aria-label="HUDA, 14x hackathon winner">',
        "<style>"
        "@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}"
        "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
        ".s{animation:tw 2.4s steps(2) infinite}"
        ".c{animation:bl 1s infinite}"
        ".t{animation:bob 1.6s steps(2) infinite}"
        "</style>",
        f'<rect width="{W}" height="{H}" fill="{NAVY}"/>',
        f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="{BG}"/>',
    ]

    # twinkling stars, kept away from the text block
    for i in range(40):
        x, y = random.randrange(16, W - 20, 4), random.randrange(16, H - 20, 4)
        if 120 < x < 780 and 30 < y < 230:
            continue
        size = random.choice((4, 4, 8))
        color = random.choice((WHITE, BLUE, PINK, YELLOW))
        delay = random.random() * 2.4
        parts.append(
            f'<rect class="s" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" '
            f'width="{size}" height="{size}" fill="{color}"/>'
        )

    title, ts = "HUDA", 14
    tx, ty = centered(title, ts), 34
    parts.append(f'<path fill="{PURPLE}" d="{text_path(title, tx + ts // 2 + 3, ty + ts // 2 + 3, ts)}"/>')
    parts.append(f'<path fill="{WHITE}" d="{text_path(title, tx, ty, ts)}"/>')

    # bobbing trophies either side of the title
    tsz = 6
    for x in (tx - 12 * tsz - 50, tx + text_width(title, ts) + 50):
        parts.append(
            f'<g class="t"><path fill="{YELLOW}" d="{bitmap_path(TROPHY, x, ty + 10, tsz)}"/>'
            f'<path fill="{ORANGE}" d="{bitmap_path([r[:3] for r in TROPHY], x, ty + 10, tsz)}"/></g>'
        )

    sub, ss = "14X HACKATHON WINNER", 4
    sx, sy = centered(sub, ss), 160
    parts.append(f'<path fill="{YELLOW}" d="{text_path(sub, sx, sy, ss)}"/>')

    tag, gs = "AI AGENTS / WEB3 / ZK", 3
    gx, gy = centered(tag, gs), 206
    parts.append(f'<path fill="{GREEN}" d="{text_path(tag, gx, gy, gs)}"/>')
    parts.append(
        f'<rect class="c" x="{gx + text_width(tag, gs) + 2 * gs}" y="{gy}" '
        f'width="{4 * gs}" height="{7 * gs}" fill="{GREEN}"/>'
    )

    parts.append("</svg>")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


HEART = [".#.#.", "#####", ".###.", "..#.."]
FACE = {"front": "..BKSSKB..", "right": "..BSKSKB..", "left": "..BKSKSB.."}
SPECTATOR_COLORS = (PINK, GREEN, ORANGE, "#ff004d", "#83769c", YELLOW, "#ab5236", "#c2c3c7")
SLOTS = (60, 150, 240, 330, 570, 660, 750, 840)  # centre x of each spectator


def person(look, colors, cx, ground, s):
    """A standing pixel person whose eyes look left, right or straight ahead."""
    top = [FACE[look] if i == 3 else row for i, row in enumerate(RUNNER_TOP)]
    rows = top + RUNNER_LEGS[1]
    x0 = cx - 5 * s
    return colored_sprite(rows, colors, x0, ground - len(rows) * s, s)


def label(text, cx, y, s, color):
    return f'<path fill="{color}" d="{text_path(text, cx - text_width(text, s) // 2, y, s)}"/>'


def guestbook(logins, out):
    """Spectators: the latest visitors who signed the guestbook, all looking at HUDA."""
    w, h, ground = 900, 230, 170
    total = len(logins)
    shown = logins[:len(SLOTS)]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{total} spectators watching HUDA">',
        "<style>"
        "@keyframes hb{0%,100%{transform:translateY(0);opacity:1}50%{transform:translateY(-6px);opacity:.4}}"
        "@keyframes hop{0%,80%,100%{transform:translateY(0)}90%{transform:translateY(-6px)}}"
        ".h{animation:hb 1.4s steps(3) infinite}.p{animation:hop 2s steps(2) infinite}"
        "</style>",
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>',
        f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" fill="{BG}"/>',
        f'<path fill="{YELLOW}" d="{text_path("SPECTATORS", 32, 26, 3)}"/>',
    ]
    count = f"{total} WATCHING"
    p.append(f'<path fill="{GREEN}" d="{text_path(count, w - 32 - text_width(count, 3), 26, 3)}"/>')
    p.append(f'<rect x="16" y="{ground}" width="{w - 32}" height="6" fill="#008751"/>')

    # HUDA in the middle, bigger, under a trophy
    huda = {"B": BLUE, "S": "#ffccaa", "K": "#000000", "N": NAVY}
    p.append(person("front", huda, w // 2, ground, 5))
    p.append(f'<path fill="{YELLOW}" d="{bitmap_path(TROPHY, w // 2 - 18, ground - 12 * 5 - 48, 3)}"/>')
    p.append(label("HUDA", w // 2, ground + 14, 3, WHITE))

    if not shown:
        p.append(label("BE THE FIRST SPECTATOR", w // 2, 44, 2, PINK))
    for i, login in enumerate(shown):
        cx = SLOTS[i]
        color = SPECTATOR_COLORS[sum(map(ord, login)) % len(SPECTATOR_COLORS)]
        look = "right" if cx < w // 2 else "left"
        delay = (i * 0.25) % 2
        colors = {"B": color, "S": "#ffccaa", "K": "#000000", "N": NAVY}
        p.append(f'<g class="p" style="animation-delay:{delay:.2f}s">{person(look, colors, cx, ground, 4)}</g>')
        p.append(
            f'<g class="h" style="animation-delay:{delay:.2f}s">'
            f'<path fill="{PINK}" d="{bitmap_path(HEART, cx - 5, ground - 12 * 4 - 18, 2)}"/></g>'
        )
        name = "".join(ch for ch in login.upper() if ch in FONT)[:6]
        p.append(label(name, cx, ground + 16, 2, WHITE))

    p.append("</svg>")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(p))


if __name__ == "__main__":
    if sys.argv[1] == "guestbook":
        # newest first, one entry per login; logins are GitHub usernames (A-Z, 0-9, '-')
        with open(sys.argv[2], encoding="utf-8") as f:
            names = list(dict.fromkeys(line.strip() for line in f if line.strip()))
        guestbook(names, sys.argv[3])
    else:
        d = sys.argv[1]
        main(f"{d}/banner.svg")
        divider(f"{d}/divider.svg")
        cabinet(f"{d}/cabinet.svg")
