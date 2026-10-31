from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "social-assets" / "instagram-launch"
SRC = ROOT / "deliverables" / "social-assets" / "source-images" / "instagram-launch"
LOGO = ROOT / "logos" / "rito_monogram_r_clean_2048.png"
WORDMARK = ROOT / "logos" / "rito_sistemas_wordmark_01.png"

W, H = 1080, 1350

BRAND = "#173847"
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
    94,
)
FONT_HEAD_POSTER = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    76,
)
FONT_SUB = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    40,
)
FONT_SUB_SMALL = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    34,
)
FONT_TAG = font(
    [
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
        "/System/Library/Fonts/Avenir.ttc",
    ],
    25,
)
FONT_LABEL = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    30,
)
FONT_META = font(
    [
        "/System/Library/Fonts/Avenir.ttc",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ],
    26,
)
FONT_META_SMALL = font(
    [
        "/System/Library/Fonts/Avenir.ttc",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ],
    22,
)
FONT_BRAND_MAIN = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    88,
)
FONT_BRAND_SECOND = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    48,
)
FONT_BRAND_SMALL = font(
    [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    ],
    36,
)


def crop_cover(image, size, focus=(0.5, 0.5)):
    src_w, src_h = image.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = image.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    res_w, res_h = resized.size

    left = int((res_w - dst_w) * focus[0])
    top = int((res_h - dst_h) * focus[1])
    left = max(0, min(left, res_w - dst_w))
    top = max(0, min(top, res_h - dst_h))
    return resized.crop((left, top, left + dst_w, top + dst_h))


def warm_grade(image):
    image = ImageEnhance.Color(image).enhance(0.92)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Brightness(image).enhance(0.97)
    warm = Image.new("RGB", image.size, WARM)
    return Image.blend(image, warm, 0.08)


def vertical_gradient(size, start_alpha, end_alpha, color=INK):
    w, h = size
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        alpha = int(start_alpha + (end_alpha - start_alpha) * (y / max(1, h - 1)))
        draw.line((0, y, w, y), fill=rgb + (alpha,))
    return overlay


def horizontal_gradient(size, start_alpha, end_alpha, reverse=False, color=INK):
    w, h = size
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    for x in range(w):
        ratio = x / max(1, w - 1)
        if reverse:
            ratio = 1 - ratio
        alpha = int(start_alpha + (end_alpha - start_alpha) * ratio)
        draw.line((x, 0, x, h), fill=rgb + (alpha,))
    return overlay


def add_texture(image):
    blur = image.filter(ImageFilter.GaussianBlur(radius=22))
    return Image.blend(image, blur, 0.06)


def add_monogram(canvas, x, y, width, opacity=255, fill=None):
    logo = Image.open(LOGO).convert("RGBA")
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


def add_wordmark(canvas, x, y, width, opacity=255):
    logo = Image.open(WORDMARK).convert("RGBA")
    ratio = width / logo.size[0]
    logo = logo.resize((int(logo.size[0] * ratio), int(logo.size[1] * ratio)), Image.Resampling.LANCZOS)
    if opacity < 255:
        alpha = logo.getchannel("A").point(lambda px: int(px * opacity / 255))
        logo.putalpha(alpha)
    canvas.alpha_composite(logo, (x, y))


def center_x(total_width, item_width):
    return int((total_width - item_width) / 2)


def add_grain(canvas, opacity=20):
    noise = Image.effect_noise(canvas.size, 12).convert("L")
    alpha = noise.point(lambda px: int(px * opacity / 255))
    overlay = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    overlay.putalpha(alpha)
    canvas.alpha_composite(overlay)


def add_plain_label(draw, x, y, text, fill=ACCENT):
    draw.text((x, y), text.upper(), font=FONT_LABEL, fill=fill)


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


def draw_text_block(draw, x, y, headline, support=None, max_width=760, headline_fill=WHITE, support_fill=(251, 247, 241, 235)):
    headline_lines = wrap_text(draw, headline, FONT_HEAD, max_width)
    for line in headline_lines:
        draw.text((x, y), line, font=FONT_HEAD, fill=headline_fill)
        bbox = draw.textbbox((x, y), line, font=FONT_HEAD)
        y = bbox[3] + 6
    if support:
        y += 14
        support_lines = wrap_text(draw, support, FONT_SUB, max_width)
        for line in support_lines:
            draw.text((x, y), line, font=FONT_SUB, fill=support_fill)
            bbox = draw.textbbox((x, y), line, font=FONT_SUB)
            y = bbox[3] + 5
    return y


def save_canvas(canvas, filename):
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / filename, quality=95)


def add_soft_shadow(panel, blur=30, offset=(0, 16), alpha=90):
    shadow = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    alpha_channel = panel.getchannel("A").point(lambda px: min(255, int(px * alpha / 255)))
    shadow.putalpha(alpha_channel)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
    out = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    out.alpha_composite(shadow, offset)
    return out


def add_top_meta(draw, left_text, right_text=None, fill=(251, 247, 241, 218)):
    draw.text((88, 86), left_text, font=FONT_META_SMALL, fill=fill)
    if right_text:
        bbox = draw.textbbox((0, 0), right_text, font=FONT_META_SMALL)
        draw.text((W - 88 - (bbox[2] - bbox[0]), 86), right_text, font=FONT_META_SMALL, fill=fill)


def draw_right_monogram(canvas, width=300, opacity=46, y=138, fill=CREAM):
    x = W - 130 - width
    add_monogram(canvas, x, y, width, opacity=opacity, fill=fill)


def make_post_01():
    canvas = Image.new("RGBA", (W, H), BRAND)
    canvas.alpha_composite(vertical_gradient((W, H), 0, 58, color="#0D2430"), (0, 0))
    canvas.alpha_composite(horizontal_gradient((W, H), 46, 0, reverse=True, color="#315161"), (0, 0))

    ambient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ambient_draw = ImageDraw.Draw(ambient)
    ambient_draw.ellipse((660, -120, 1230, 350), fill=(184, 145, 99, 68))
    ambient_draw.ellipse((-180, 880, 360, 1460), fill=(95, 129, 146, 42))
    ambient_draw.ellipse((120, 30, 470, 330), fill=(255, 255, 255, 18))
    ambient_draw.ellipse((210, 120, 890, 760), fill=(255, 255, 255, 12))
    ambient = ambient.filter(ImageFilter.GaussianBlur(radius=44))
    canvas.alpha_composite(ambient)
    add_grain(canvas, opacity=12)

    draw = ImageDraw.Draw(canvas)
    add_monogram(canvas, center_x(W, 610), 132, 610, opacity=48, fill="#0D2430")
    add_monogram(canvas, center_x(W, 610), 118, 610, opacity=255, fill=CREAM)

    line_width = 140
    line_x = center_x(W, line_width)
    draw.rounded_rectangle((line_x, 760, line_x + line_width, 770), radius=5, fill=ACCENT)

    title = "RITO Sistemas"
    bbox = draw.textbbox((0, 0), title, font=FONT_BRAND_MAIN)
    draw.text((center_x(W, bbox[2] - bbox[0]), 826), title, font=FONT_BRAND_MAIN, fill=CREAM)

    tagline = "Software sob medida para a rotina da sua empresa"
    tag_lines = wrap_text(draw, tagline, FONT_SUB_SMALL, 740)
    y = 950
    for line in tag_lines:
        bbox = draw.textbbox((0, 0), line, font=FONT_SUB_SMALL)
        draw.text((center_x(W, bbox[2] - bbox[0]), y), line, font=FONT_SUB_SMALL, fill=(244, 240, 233, 232))
        y += 48

    footer = "Rotinas Inteligentes de Tecnologia e Operação"
    bbox = draw.textbbox((0, 0), footer, font=FONT_META)
    draw.text((center_x(W, bbox[2] - bbox[0]), 1168), footer, font=FONT_META, fill=(184, 145, 99, 230))
    save_canvas(canvas, "01-rito-apresentacao-static.png")


def make_post_02():
    photo = Image.open(SRC / "post02-calculator-report.jpg").convert("RGB")
    photo = crop_cover(photo, (W, H), focus=(0.68, 0.34))
    photo = add_texture(warm_grade(photo))

    canvas = photo.convert("RGBA")
    canvas.alpha_composite(vertical_gradient((W, H), 0, 150), (0, 0))
    draw = ImageDraw.Draw(canvas)

    add_top_meta(draw, "RITO Sistemas")
    draw.rounded_rectangle((96, 912, 246, 920), radius=4, fill=ACCENT)
    y = draw_text_block(
        draw,
        96,
        950,
        "Planilha para tudo?",
        "Quando a rotina cresce, o retrabalho aparece.",
        max_width=620,
        headline_fill=WHITE,
        support_fill=(251, 247, 241, 228),
    )
    draw.text((96, y + 34), "Orçamento grátis e sem compromisso", font=FONT_META, fill=(244, 240, 233, 228))
    save_canvas(canvas, "02-rito-dor-planilhas-static.png")


def make_carousel_slide_01():
    photo = Image.open(SRC / "post02-chaos.jpg").convert("RGB")
    photo = crop_cover(photo, (W, H), focus=(0.46, 0.32))
    photo = add_texture(warm_grade(photo))

    canvas = photo.convert("RGBA")
    canvas.alpha_composite(vertical_gradient((W, H), 0, 56), (0, 0))
    draw = ImageDraw.Draw(canvas)

    add_top_meta(draw, "ANTES", "1/3", fill=(21, 39, 51, 176))
    draw.rounded_rectangle((244, 808, 378, 816), radius=4, fill=ACCENT)
    draw_text_block(
        draw,
        238,
        854,
        "Tudo espalhado.",
        "Pedido chega. O status some.",
        max_width=360,
        headline_fill=INK,
        support_fill=(21, 39, 51, 208),
    )
    save_canvas(canvas, "03-rito-carrossel-slide-01.png")


def make_carousel_slide_02():
    photo = Image.open(SRC / "carousel-after.jpg").convert("RGB")
    photo = crop_cover(photo, (W, H), focus=(0.82, 0.4))
    photo = add_texture(warm_grade(photo))

    canvas = photo.convert("RGBA")
    canvas.alpha_composite(vertical_gradient((W, H), 0, 54, color="#F4F0E9"), (0, 0))
    canvas.alpha_composite(vertical_gradient((W, H), 0, 72), (0, 0))
    canvas.alpha_composite(horizontal_gradient((W, H), 78, 0, reverse=True, color="#F4F0E9"), (0, 0))
    draw = ImageDraw.Draw(canvas)

    add_top_meta(draw, "DEPOIS", "2/3", fill=(21, 39, 51, 176))
    draw.rounded_rectangle((92, 916, 212, 924), radius=4, fill=ACCENT)
    draw_text_block(
        draw,
        92,
        958,
        "Mais clareza.",
        "Menos retrabalho na operação.",
        max_width=540,
        headline_fill=INK,
        support_fill=(21, 39, 51, 210),
    )
    save_canvas(canvas, "03-rito-carrossel-slide-02.png")


def make_carousel_slide_03():
    canvas = Image.new("RGBA", (W, H), BRAND)
    canvas.alpha_composite(vertical_gradient((W, H), 0, 54, color="#0E2430"), (0, 0))
    ambient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ambient_draw = ImageDraw.Draw(ambient)
    ambient_draw.ellipse((560, -120, 1140, 360), fill=(184, 145, 99, 56))
    ambient_draw.ellipse((-160, 920, 420, 1460), fill=(95, 129, 146, 38))
    ambient = ambient.filter(ImageFilter.GaussianBlur(radius=42))
    canvas.alpha_composite(ambient)
    add_grain(canvas, opacity=14)
    draw = ImageDraw.Draw(canvas)

    add_top_meta(draw, "RITO Sistemas", "3/3")
    draw_right_monogram(canvas, width=420, opacity=42, y=110, fill=CREAM)
    line_width = 120
    line_x = 92
    draw.rounded_rectangle((line_x, 860, line_x + line_width, 868), radius=4, fill=ACCENT)
    y = draw_text_block(
        draw,
        92,
        916,
        "A RITO organiza sua rotina.",
        "Chame no WhatsApp e conte seu desafio.",
        max_width=620,
        headline_fill=WHITE,
        support_fill=(251, 247, 241, 228),
    )
    draw.text((92, y + 36), "Análise inicial sem compromisso", font=FONT_BRAND_SMALL, fill=(244, 240, 233, 226))
    save_canvas(canvas, "03-rito-carrossel-slide-03.png")


def main():
    make_post_01()
    make_post_02()
    make_carousel_slide_01()
    make_carousel_slide_02()
    make_carousel_slide_03()


if __name__ == "__main__":
    main()
