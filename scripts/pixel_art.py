"""Pixel-art SVGs for the GitHub profile README.

  python pixel_art.py <dir>                        static art: divider, world map, dialog
  python pixel_art.py live <repos.json> <weather.json> <dir>
                                                   hourly: day/night/weather/holiday banner + current quest
  python pixel_art.py guestbook <logins.txt> <out> spectators
"""
import json
import random
import sys
from datetime import datetime, timedelta, timezone

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
    ",": [".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    " ": ["....."] * 7,
}


def clean(text):
    """Uppercase and drop anything the pixel font can't draw."""
    return " ".join("".join(ch if ch in FONT else " " for ch in text.upper()).split())

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


SUN = ["..####..", ".######.", "########", "########", "########", "########", ".######.", "..####.."]
MOON = ["..####..", ".###....", "###.....", "###.....", "###.....", "###.....", ".###....", "..####.."]
CLOUD = ["...####.....", ".########...", "############"]

# Sky per time of day in WIB: (outer frame, sky, title shadow, subtitle, tagline, stars)
SKIES = {
    "day": ("#065ab5", BLUE, NAVY, NAVY, WHITE, 0),
    "dusk": (NAVY, PURPLE, NAVY, YELLOW, "#ffccaa", 12),
    "night": (NAVY, BG, PURPLE, YELLOW, GREEN, 40),
}


def sky_for(hour):
    return "day" if 6 <= hour < 17 else "dusk" if 17 <= hour < 19 else "night"


def weather_kind(code):
    """WMO weather code (Open-Meteo) -> clear / cloudy / rain / storm."""
    if code is None or code <= 1:
        return "clear"
    if code >= 95:
        return "storm"
    if 51 <= code <= 67 or 80 <= code <= 82:
        return "rain"
    return "cloudy"


# ponytail: Lebaran dates are approximate (sidang isbat decides the real day); add years as they come
LEBARAN = {(2027, 3, 10), (2028, 2, 27), (2029, 2, 14), (2030, 2, 4)}


def event_for(day):
    if day.month == 8 and 10 <= day.day <= 20:
        return "merdeka"
    if (day.month, day.day) in ((12, 31), (1, 1)):
        return "newyear"
    if any(abs((day - datetime(*d).date()).days) <= 2 for d in LEBARAN):
        return "lebaran"
    return None


KETUPAT = ["...GG...", "..GYYG..", ".GYGGYG.", "GYGYYGYG", "GYGYYGYG", ".GYGGYG.", "..GYYG..", "...GG..."]
SPARK = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def decorations(event):
    """Seasonal extras drawn along the banner's edges."""
    if event == "merdeka":  # red-and-white bunting for Independence Day
        return [
            f'<path fill="{"#ff004d" if i % 2 == 0 else WHITE}" d="M{x} 8h20l-10 16z"/>'
            for i, x in enumerate(range(12, W - 30, 26))
        ]
    if event == "lebaran":  # hanging ketupat
        out = []
        for x in (112, 800):
            out.append(f'<rect x="{x + 22}" y="8" width="3" height="30" fill="{WHITE}"/>')
            out.append(colored_sprite(KETUPAT, {"G": "#008751", "Y": YELLOW}, x, 38, 6))
        return out
    if event == "newyear":  # fireworks
        out = []
        for i, (cx, cy, color) in enumerate(((120, 70, PINK), (790, 64, YELLOW), (830, 196, GREEN), (70, 200, BLUE))):
            dots = "".join(f'<rect x="{cx + dx * 22 - 3}" y="{cy + dy * 22 - 3}" width="6" height="6"/>' for dx, dy in SPARK)
            out.append(f'<g class="fw" style="animation-delay:{i * 0.4:.1f}s;transform-origin:{cx}px {cy}px" fill="{color}">{dots}</g>')
        return out
    return []


def main(out, sky="night", weather="clear", temp=None, event=None):
    random.seed(14)
    frame, bg, shadow, sub_color, tag_color, stars = SKIES[sky]
    wet = weather in ("rain", "storm")
    if wet and sky == "day":
        frame, bg, sub_color = "#5f574f", "#83769c", YELLOW
    if weather != "clear":
        stars = 0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'shape-rendering="crispEdges" role="img" '
        f'aria-label="HUDA, 14x hackathon winner ({sky}, {weather} in Jakarta)">',
        "<style>"
        "@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}"
        "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
        "@keyframes drift{0%,100%{transform:translateX(0)}50%{transform:translateX(16px)}}"
        "@keyframes fall{from{transform:translateY(0)}to{transform:translateY(290px)}}"
        "@keyframes flash{0%,90%,94%,100%{opacity:0}91%{opacity:.7}95%{opacity:.4}}"
        "@keyframes boom{0%{transform:scale(.2);opacity:1}80%{opacity:1}100%{transform:scale(1.3);opacity:0}}"
        ".s{animation:tw 2.4s steps(2) infinite}"
        ".c{animation:bl 1s infinite}"
        ".t{animation:bob 1.6s steps(2) infinite}"
        ".d{animation:drift 6s steps(4) infinite}"
        ".r{animation:fall .9s linear infinite}"
        ".l{animation:flash 6s infinite}"
        ".fw{animation:boom 1.6s steps(6) infinite}"
        "</style>",
        f'<rect width="{W}" height="{H}" fill="{frame}"/>',
        f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="{bg}"/>',
    ]

    if weather == "clear":
        if sky == "night":
            parts.append(f'<path fill="{WHITE}" d="{bitmap_path(MOON, 40, 28, 6)}"/>')
        else:
            sun_y = 28 if sky == "day" else 190
            parts.append(f'<path fill="{YELLOW if sky == "day" else ORANGE}" d="{bitmap_path(SUN, 40, sun_y, 6)}"/>')
    clouds = ((740, 36), (60, 196), (790, 200))
    if weather != "clear":
        clouds += ((30, 30), (130, 14), (650, 12), (690, 224))
    if sky == "day" or weather != "clear":
        cloud_color = WHITE if weather == "clear" else "#c2c3c7"
        for x, y in clouds:
            parts.append(f'<g class="d"><path fill="{cloud_color}" d="{bitmap_path(CLOUD, x, y, 6)}"/></g>')
    if wet:
        for _ in range(45):
            x, y0 = random.randrange(12, W - 12, 4), random.randrange(-280, -10, 4)
            delay = random.random() * 0.9
            parts.append(
                f'<rect class="r" style="animation-delay:{delay:.2f}s" x="{x}" y="{y0}" width="3" height="12" fill="#c2c3c7"/>'
            )
    if weather == "storm":
        parts.append(f'<rect class="l" x="8" y="8" width="{W - 16}" height="{H - 16}" fill="{WHITE}"/>')
    parts += decorations(event)

    # twinkling stars, kept away from the text block and the moon
    for i in range(stars):
        x, y = random.randrange(16, W - 20, 4), random.randrange(16, H - 20, 4)
        if (120 < x < 780 and 30 < y < 230) or (x < 100 and y < 90):
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
    parts.append(f'<path fill="{shadow}" d="{text_path(title, tx + ts // 2 + 3, ty + ts // 2 + 3, ts)}"/>')
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
    parts.append(f'<path fill="{sub_color}" d="{text_path(sub, sx, sy, ss)}"/>')

    tag, gs = "AI AGENTS / WEB3 / ZK", 3
    gx, gy = centered(tag, gs), 206
    parts.append(f'<path fill="{tag_color}" d="{text_path(tag, gx, gy, gs)}"/>')
    parts.append(
        f'<rect class="c" x="{gx + text_width(tag, gs) + 2 * gs}" y="{gy}" '
        f'width="{4 * gs}" height="{7 * gs}" fill="{tag_color}"/>'
    )
    if temp is not None:
        hud = f"JKT {round(temp)}C"
        parts.append(f'<path fill="{WHITE}" d="{text_path(hud, W - 24 - text_width(hud, 2), 228, 2)}"/>')

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


def svg_open(w, h, label_text, style=""):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{label_text}">',
        f"<style>{style}</style>",
    ]


def write(out, parts):
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts + ["</svg>"]))


# Stage colours follow the High Scores table order: 2 gold, 3 silver, 3 bronze, 6 other wins
STAGE_COLORS = [(YELLOW, ORANGE)] * 2 + [("#c2c3c7", "#83769c")] * 3 + [("#e08a3c", "#ab5236")] * 3 + [(BLUE, "#065ab5")] * 6
TREE = ["..##..", ".####.", "######", ".####.", "..##..", "..##.."]
CASTLE = [
    "#.#.#..#.#.#",
    "############",
    "############",
    "####....####",
    "###......###",
    "###......###",
]


def worldmap(out):
    """Overworld map: every win is a cleared stage, HUDA walks the road to the castle."""
    w, h = 900, 320
    rows = (100, 180, 260)
    road = f"M60 {rows[0]}H840V{rows[1]}H60V{rows[2]}H760"
    stages = [(x, rows[0]) for x in (120, 270, 420, 570, 720)]
    stages += [(x, rows[1]) for x in (780, 630, 480, 330, 180)]
    stages += [(x, rows[2]) for x in (120, 270, 420, 570)]
    p = svg_open(
        w, h, "World map: 14 cleared hackathon stages, HUDA walking to the castle",
        "@keyframes f1{0%,49%{opacity:1}50%,100%{opacity:0}}@keyframes f2{0%,49%{opacity:0}50%,100%{opacity:1}}"
        ".a{animation:f1 .4s infinite}.b{animation:f2 .4s infinite}",
    )
    p += [
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>',
        f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" fill="#008751"/>',
        f'<path fill="{YELLOW}" d="{text_path("WORLD 1: HACKATHON TOUR", 32, 26, 3)}"/>',
        f'<path fill="{WHITE}" d="{text_path("14/14 CLEARED", w - 32 - text_width("14/14 CLEARED", 3), 26, 3)}"/>',
    ]
    random.seed(7)
    for band in (140, 220):
        for x in range(40, 860, 70):
            x += random.randrange(0, 30, 3)
            p.append(f'<path fill="#00e436" d="{bitmap_path(TREE, x, band - 9, 3)}"/>')
    p.append(f'<path d="{road}" fill="none" stroke="#ffccaa" stroke-width="14" stroke-linejoin="miter"/>')
    p.append(f'<path d="{road}" fill="none" stroke="#ab5236" stroke-width="2" stroke-dasharray="6 10"/>')

    for i, ((x, y), (main_c, shade)) in enumerate(zip(stages, STAGE_COLORS), 1):
        p.append(f'<rect x="{x - 16}" y="{y - 16}" width="32" height="32" fill="{shade}"/>')
        p.append(f'<rect x="{x - 13}" y="{y - 13}" width="26" height="26" fill="{main_c}"/>')
        p.append(label(str(i), x, y - 7, 2, NAVY))
        p.append(f'<rect x="{x + 12}" y="{y - 36}" width="3" height="22" fill="{WHITE}"/>')
        p.append(f'<rect x="{x + 15}" y="{y - 36}" width="12" height="8" fill="#ff004d"/>')

    cx, cy = 790, rows[2]
    p.append(f'<path fill="#c2c3c7" d="{bitmap_path(CASTLE, cx, cy - 24, 4)}"/>')
    p.append(f'<rect x="{cx + 22}" y="{cy - 44}" width="3" height="20" fill="{WHITE}"/>')
    p.append(f'<rect x="{cx + 25}" y="{cy - 44}" width="14" height="9" fill="{YELLOW}"/>')

    pal = {"B": BLUE, "S": "#ffccaa", "K": "#000000", "N": NAVY}
    body = colored_sprite(RUNNER_TOP, pal, -10, -24, 2)
    legs = [colored_sprite(l, pal, -10, -6, 2) for l in RUNNER_LEGS]
    p.append(
        f'<g>{body}<g class="a">{legs[0]}</g><g class="b">{legs[1]}</g>'
        f'<animateMotion path="{road}" dur="18s" repeatCount="indefinite"/></g>'
    )
    write(out, p)


DIALOG = ("WELCOME, TRAVELER! I'M HUDA.", "I BUILD ZK, WEB3 AND AI AGENTS,", "SOLO, AGAINST THE HACKATHON CLOCK.")


def dialog(out):
    """RPG text box: HUDA's portrait, and the lines typed out one character at a time."""
    w, h, s = 900, 172, 3
    p = svg_open(
        w, h, "HUDA: " + " ".join(DIALOG).capitalize(),
        "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.c{animation:bl .8s infinite}",
    )
    p += [
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>',
        f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" fill="{WHITE}"/>',
        f'<rect x="18" y="18" width="{w - 36}" height="{h - 36}" fill="{BG}"/>',
        f'<rect x="32" y="32" width="108" height="108" fill="{PURPLE}"/>',
        person("front", {"B": BLUE, "S": "#ffccaa", "K": "#000000", "N": NAVY}, 86, 132, 8),
        f'<path fill="{YELLOW}" d="{text_path("HUDA", 164, 34, s)}"/>',
    ]
    cw, dur, end = 6 * s, 10, 0.92
    for i, line in enumerate(DIALOG):
        y = 68 + i * 30
        a, b = 0.03 + i * 0.25, 0.03 + (i + 1) * 0.25
        n = len(line)
        times = ["0"] + [f"{a + (b - a) * k / n:.4f}" for k in range(1, n + 1)] + [f"{end}"]
        widths = ["0"] + [str(k * cw) for k in range(1, n + 1)] + ["0"]
        p.append(
            f'<clipPath id="l{i}"><rect x="164" y="{y}" width="0" height="{7 * s}">'
            f'<animate attributeName="width" calcMode="discrete" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(times)}" values="{";".join(widths)}"/></rect></clipPath>'
        )
        p.append(f'<path clip-path="url(#l{i})" fill="{WHITE}" d="{text_path(line, 164, y, s)}"/>')
    p.append(f'<path class="c" fill="{YELLOW}" d="M{w - 52} {h - 46}h18l-9 10z"/>')
    write(out, p)


def ago(iso, now):
    mins = int((now - datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() // 60)
    if mins < 60:
        return f"{max(mins, 1)}M AGO"
    return f"{mins // 60}H AGO" if mins < 1440 else f"{mins // 1440}D AGO"


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = word[:width]
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def quest(repos, out, now):
    """CURRENT QUEST panel from the most recently pushed public repo."""
    w, h = 900, 172
    repo = next((r for r in repos if not r["fork"] and r["name"].lower() != "pugarhuda"), None)
    p = svg_open(
        w, h, f"Current quest: {repo['name'] if repo else 'none'}",
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}.q{animation:bob 1s steps(2) infinite}",
    )
    p += [
        f'<rect width="{w}" height="{h}" fill="{NAVY}"/>',
        f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" fill="{BG}"/>',
        f'<g class="q"><path fill="{YELLOW}" d="{text_path("!", 24, 26, 3)}"/></g>',
        f'<path fill="{YELLOW}" d="{text_path("CURRENT QUEST", 50, 26, 3)}"/>',
    ]
    if repo:
        save = "LAST SAVE " + ago(repo["pushed_at"], now)
        p.append(f'<path fill="{GREEN}" d="{text_path(save, w - 32 - text_width(save, 2), 30, 2)}"/>')
        p.append(f'<path fill="{WHITE}" d="{text_path(clean(repo["name"])[:34], 32, 62, 4)}"/>')
        for i, line in enumerate(wrap(clean(repo["description"] or ""), 68)[:2]):
            p.append(f'<path fill="#c2c3c7" d="{text_path(line[:68], 32, 104 + i * 20, 2)}"/>')
        if repo.get("language"):
            lang = "LANG: " + clean(repo["language"])
            p.append(f'<path fill="{PINK}" d="{text_path(lang, w - 32 - text_width(lang, 2), 140, 2)}"/>')
    write(out, p)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "guestbook":
        # newest first, one entry per login; logins are GitHub usernames (A-Z, 0-9, '-')
        with open(sys.argv[2], encoding="utf-8") as f:
            names = list(dict.fromkeys(line.strip() for line in f if line.strip()))
        guestbook(names, sys.argv[3])
    elif cmd == "live":
        # hourly: banner follows the time, weather and holidays in Jakarta; quest follows the latest push
        now = datetime.now(timezone.utc)
        local = now + timedelta(hours=7)
        d = sys.argv[4]
        try:
            with open(sys.argv[3], encoding="utf-8") as f:
                current = json.load(f)["current"]
            code, temp = current["weather_code"], current["temperature_2m"]
        except (OSError, ValueError, KeyError, TypeError):
            code, temp = None, None  # weather API down: clear sky, no temperature
        main(f"{d}/banner.svg", sky_for(local.hour), weather_kind(code), temp, event_for(local.date()))
        with open(sys.argv[2], encoding="utf-8") as f:
            quest(json.load(f), f"{d}/quest.svg", now)
    else:
        d = sys.argv[1]
        divider(f"{d}/divider.svg")
        worldmap(f"{d}/worldmap.svg")
        dialog(f"{d}/dialog.svg")
