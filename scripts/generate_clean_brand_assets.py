from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "brand" / "logos" / "site" / "rito_monogram_r_01.png"
SVG_OUT = ROOT / "assets" / "brand" / "logos" / "site" / "rito_monogram_r_clean.svg"
PNG_OUT = ROOT / "assets" / "brand" / "logos" / "site" / "rito_monogram_r_clean_2048.png"

BRAND = "#173847"


def marching_squares_loops(mask: np.ndarray):
    h, w = mask.shape
    segments = []

    # Edge midpoints use doubled integer coordinates to avoid float joins.
    lookup = {
        1: ("L", "B"),
        2: ("B", "R"),
        3: ("L", "R"),
        4: ("T", "R"),
        5: (("T", "L"), ("B", "R")),
        6: ("T", "B"),
        7: ("T", "L"),
        8: ("T", "L"),
        9: ("T", "B"),
        10: (("T", "R"), ("L", "B")),
        11: ("T", "R"),
        12: ("L", "R"),
        13: ("B", "R"),
        14: ("L", "B"),
    }

    def point(name, x, y):
        pts = {
            "T": (2 * x + 1, 2 * y),
            "R": (2 * x + 2, 2 * y + 1),
            "B": (2 * x + 1, 2 * y + 2),
            "L": (2 * x, 2 * y + 1),
        }
        return pts[name]

    for y in range(h - 1):
        for x in range(w - 1):
            tl = 1 if mask[y, x] else 0
            tr = 1 if mask[y, x + 1] else 0
            br = 1 if mask[y + 1, x + 1] else 0
            bl = 1 if mask[y + 1, x] else 0
            case = (tl << 3) | (tr << 2) | (br << 1) | bl
            if case in (0, 15):
                continue
            entry = lookup[case]
            if isinstance(entry[0], tuple):
                pairs = entry
            else:
                pairs = (entry,)
            for a_name, b_name in pairs:
                segments.append((point(a_name, x, y), point(b_name, x, y)))

    from collections import defaultdict

    adjacency = defaultdict(list)
    for a, b in segments:
        adjacency[a].append(b)
        adjacency[b].append(a)

    loops = []
    visited = set()

    for a, b in segments:
        edge = tuple(sorted((a, b)))
        if edge in visited:
            continue
        loop = [a, b]
        visited.add(edge)
        prev, cur = a, b

        while True:
            nxts = [n for n in adjacency[cur] if n != prev]
            if not nxts:
                break
            nxt = None
            for candidate in nxts:
                candidate_edge = tuple(sorted((cur, candidate)))
                if candidate_edge not in visited:
                    nxt = candidate
                    break
            if nxt is None:
                nxt = nxts[0]
            candidate_edge = tuple(sorted((cur, nxt)))
            if candidate_edge in visited and nxt == loop[0]:
                loop.append(nxt)
                break
            visited.add(candidate_edge)
            prev, cur = cur, nxt
            if cur == loop[0]:
                loop.append(cur)
                break
            loop.append(cur)
            if len(loop) > 30000:
                break

        if len(loop) > 10 and loop[0] == loop[-1]:
            loops.append(loop[:-1])

    unique = []
    for loop in loops:
        points = set(loop)
        if any(len(points & set(other)) > 5 for other in unique):
            continue
        unique.append(loop)
    return unique


def polygon_area(loop):
    pts = np.array(loop, dtype=float) / 2.0
    x = pts[:, 0]
    y = pts[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def rdp(points, epsilon):
    if len(points) < 3:
        return points

    p0 = np.array(points[0], dtype=float)
    p1 = np.array(points[-1], dtype=float)
    line = p1 - p0
    norm = np.linalg.norm(line)

    if norm == 0:
        distances = np.linalg.norm(np.array(points) - p0, axis=1)
    else:
        pts = np.array(points, dtype=float)
        line_x, line_y = line
        distances = np.abs(line_x * (p0[1] - pts[:, 1]) - (p0[0] - pts[:, 0]) * line_y) / norm

    idx = int(np.argmax(distances))
    if distances[idx] > epsilon:
        left = rdp(points[: idx + 1], epsilon)
        right = rdp(points[idx:], epsilon)
        return left[:-1] + right
    return [points[0], points[-1]]


def chaikin(loop, rounds=2):
    pts = [np.array(point, dtype=float) for point in loop]
    for _ in range(rounds):
        new_pts = []
        for i in range(len(pts)):
            p = pts[i]
            q = pts[(i + 1) % len(pts)]
            new_pts.append(0.75 * p + 0.25 * q)
            new_pts.append(0.25 * p + 0.75 * q)
        pts = new_pts
    return [tuple(point) for point in pts]


def clean_loops(mask: np.ndarray):
    raw_loops = marching_squares_loops(mask)
    processed = []
    for loop in raw_loops:
        simplified = rdp(loop + [loop[0]], epsilon=2.5)[:-1]
        smoothed = chaikin(simplified, rounds=2)
        processed.append((polygon_area(loop), smoothed))
    return processed


def write_svg(size, loops):
    width, height = size
    path_parts = []
    for _, loop in loops:
        coords = [(x / 2.0, y / 2.0) for x, y in loop]
        path_parts.append("M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in coords) + " Z")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<path d="{" ".join(path_parts)}" fill="{BRAND}" fill-rule="evenodd"/></svg>'
    )
    SVG_OUT.write_text(svg)


def render_png(size, loops, target_width=2048):
    width, height = size
    scale = target_width / width
    out_size = (int(width * scale), int(height * scale))
    mask_img = Image.new("L", out_size, 0)
    draw = ImageDraw.Draw(mask_img)

    signs = [area for area, _ in loops]
    dominant = max(signs, key=lambda value: abs(value))
    outer_sign = 1 if dominant > 0 else -1

    for area, loop in loops:
        pts = [(x / 2.0 * scale, y / 2.0 * scale) for x, y in loop]
        if area * outer_sign > 0:
            draw.polygon(pts, fill=255)
    for area, loop in loops:
        pts = [(x / 2.0 * scale, y / 2.0 * scale) for x, y in loop]
        if area * outer_sign < 0:
            draw.polygon(pts, fill=0)

    image = Image.new("RGBA", out_size, (23, 56, 71, 0))
    fill = Image.new("RGBA", out_size, (23, 56, 71, 255))
    fill.putalpha(mask_img)
    image.alpha_composite(fill)
    image.save(PNG_OUT)


def main():
    source = Image.open(SOURCE).convert("RGBA")
    alpha = np.array(source.getchannel("A")) > 32
    loops = clean_loops(alpha)
    write_svg(source.size, loops)
    render_png(source.size, loops)


if __name__ == "__main__":
    main()
