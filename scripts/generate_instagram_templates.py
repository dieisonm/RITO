from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "social-assets" / "templates"
LOGO = ROOT / "logos" / "rito_monogram_r_clean_2048.png"
WORDMARK = ROOT / "logos" / "rito_sistemas_wordmark_02.png"

W, H = 1080, 1350

BRAND = "#173847"
BRAND_STRONG = "#0D2430"
BRAND_MID = "#315161"
INK = "#152733"
CREAM = "#FBF7F1"
WARM = "#F4F0E9"
ACCENT = "#B89163"
WHITE = "#FFFFFF"


def font(path_options, size):
    for p in path_options:
        path = Path(p)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_HEAD = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    74,
)
FONT_SUB = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    34,
)
FONT_META = font(
    [
        "/System/Library/Fonts/Avenir.ttc",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ],
    24,
)
FONT_LABEL = font(
    [
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
        "/System/Library/Fonts/Avenir.ttc",
    ],
    22,
)


def wrap_text(draw, text, font_obj, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        width = draw.textbbox((0, 0), trial, font=font_obj)[2]
        if width <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def center_x(total_width, item_width):
    return int((total_width - item_width) / 2)


def vertical_gradient(size, start_alpha, end_alpha, color=INK):
    w, h = size
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        alpha = int(start_alpha + (end_alpha - start_alpha) * (y / max(1, h - 1)))
        draw.line((0, y, w, y), fill=rgb + (alpha,))
    return overlay


def add_grain(canvas, opacity=16):
    noise = Image.effect_noise(canvas.size, 12).convert("L")
    alpha = noise.point(lambda px: int(px * opacity / 255))
    overlay = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    overlay.putalpha(alpha)
    canvas.alpha_composite(overlay)


def add_monogram(canvas, x, y, width, opacity=255):
    logo = Image.open(LOGO).convert("RGBA")
    ratio = width / logo.size[0]
    logo = logo.resize((int(logo.size[0] * ratio), int(logo.size[1] * ratio)), Image.Resampling.LANCZOS)
    if opacity < 255:
        alpha = logo.getchannel("A").point(lambda px: int(px * opacity / 255))
        logo.putalpha(alpha)
    canvas.alpha_composite(logo, (x, y))


def add_wordmark(canvas, x, y, width, opacity=255, fill=None):
    logo = Image.open(WORDMARK).convert("RGBA")
    ratio = width / logo.size[0]
    logo = logo.resize((int(logo.size[0] * ratio), int(logo.size[1] * ratio)), Image.Resampling.LANCZOS)
    if fill is not None:
        rgb = tuple(int(fill[i : i + 2], 16) for i in (1, 3, 5))
        mask = logo.getchannel("A")
        tinted = Image.new("RGBA", logo.size, rgb + (0,))
        tinted.putalpha(mask)
        logo = tinted
    if opacity < 255:
        alpha = logo.getchannel("A").point(lambda px: int(px * opacity / 255))
        logo.putalpha(alpha)
    canvas.alpha_composite(logo, (x, y))


def save(canvas, filename):
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / filename, quality=95)


def make_institutional_template():
    canvas = Image.new("RGBA", (W, H), BRAND)
    canvas.alpha_composite(vertical_gradient((W, H), 0, 56, color=BRAND_STRONG), (0, 0))
    ambient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ambient_draw = ImageDraw.Draw(ambient)
    ambient_draw.ellipse((620, -100, 1220, 350), fill=(184, 145, 99, 72))
    ambient_draw.ellipse((-140, 980, 320, 1460), fill=(95, 129, 146, 48))
    ambient = ambient.filter(ImageFilter.GaussianBlur(radius=46))
    canvas.alpha_composite(ambient)
    add_grain(canvas, 12)

    add_monogram(canvas, center_x(W, 620), 136, 620, opacity=68)

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((center_x(W, 150), 760, center_x(W, 150) + 150, 770), radius=5, fill=ACCENT)

    headline = "Headline curta aqui"
    bbox = draw.textbbox((0, 0), headline, font=FONT_HEAD)
    draw.text((center_x(W, bbox[2] - bbox[0]), 830), headline, font=FONT_HEAD, fill=CREAM)

    support = "Linha de apoio com benefício claro."
    lines = wrap_text(draw, support, FONT_SUB, 760)
    y = 940
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=FONT_SUB)
        draw.text((center_x(W, bbox[2] - bbox[0]), y), line, font=FONT_SUB, fill=(244, 240, 233, 228))
        y += 44

    draw.text((92, 92), "Template institucional", font=FONT_META, fill=(244, 240, 233, 208))
    add_wordmark(canvas, center_x(W, 250), 1176, 250, opacity=235, fill=CREAM)
    save(canvas, "instagram-template-institucional.png")


def make_problem_result_template():
    canvas = Image.new("RGBA", (W, H), WARM)
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((72, 72, W - 72, 760), radius=34, fill=CREAM, outline=(184, 145, 99, 120), width=2)
    draw.rounded_rectangle((72, 72, W - 72, 760), radius=34, outline=(255, 255, 255, 120), width=1)

    pattern = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pattern)
    for x in range(120, W - 120, 70):
        pdraw.line((x, 140, x + 110, 680), fill=(95, 129, 146, 24), width=2)
    pattern = pattern.filter(ImageFilter.GaussianBlur(radius=2))
    canvas.alpha_composite(pattern)

    draw.rounded_rectangle((92, 102, 238, 112), radius=5, fill=ACCENT)
    draw.text((92, 132), "Espaço para foto ou detalhe da rotina", font=FONT_LABEL, fill=(93, 107, 114, 220))

    draw.text((92, 840), "DOR OU RESULTADO", font=FONT_META, fill=(93, 107, 114, 220))
    headline = "Headline principal"
    bbox = draw.textbbox((0, 0), headline, font=FONT_HEAD)
    draw.text((92, 900), headline, font=FONT_HEAD, fill=INK)

    support = "Linha de apoio com contexto curto e objetivo."
    for line in wrap_text(draw, support, FONT_SUB, 760):
        draw.text((92, 1010), line, font=FONT_SUB, fill=(21, 39, 51, 220))
        break

    draw.rounded_rectangle((92, 1148, 222, 1156), radius=4, fill=ACCENT)
    add_wordmark(canvas, 92, 1182, 220, opacity=255)
    draw.text((W - 360, 1190), "Trocar imagem e texto mantendo a hierarquia", font=FONT_LABEL, fill=(93, 107, 114, 220))

    save(canvas, "instagram-template-dor-resultado.png")


def main():
    make_institutional_template()
    make_problem_result_template()


if __name__ == "__main__":
    main()
