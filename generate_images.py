"""
generate_images.py
------------------
Reads posts.json and renders each quote as a 1080x1350 PNG quote card
in the Tommy Mello tweet-style: white card, black top/bottom bars,
green-glow circular avatar, verified badge, bold quote text.

Usage:
    python generate_images.py

Requires:
    pip install Pillow
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------- CONFIG ----------
ROOT = Path(__file__).parent
POSTS_FILE = ROOT / "posts.json"
OUT_DIR = ROOT / "output" / "images"
PHOTO_PATH = ROOT / "photo.png"

CARD_W, CARD_H = 1080, 1350
BAR_H = 70                        # top/bottom black bars
PADDING = 90                      # card content padding
AVATAR_SIZE = 200                 # avatar diameter
RING_THICKNESS = 10               # green glow ring
VERIFIED_SIZE = 56                # twitter-like verified badge

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_TEXT = (18, 18, 22)
GRAY = (100, 110, 125)
GREEN_RING_STOPS = [(10, 46, 10), (0, 204, 68), (10, 46, 10)]
TWITTER_BLUE = (29, 155, 240)


# ---------- FONT LOADING ----------
def load_font(size, bold=False):
    """Try a few common system fonts. Falls back to PIL default."""
    candidates_bold = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    candidates_regular = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in (candidates_bold if bold else candidates_regular):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ---------- HELPERS ----------
def make_avatar(photo_path: Path, size: int) -> Image.Image:
    """Circular avatar with a glowing green ring around it."""
    # Base transparent canvas for avatar + ring
    canvas_size = size + RING_THICKNESS * 4
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Green ring (gradient approximated by 3 concentric circles)
    ring_outer = canvas_size
    for i, color in enumerate(GREEN_RING_STOPS):
        inset = i * (RING_THICKNESS // 2)
        draw.ellipse(
            [inset, inset, ring_outer - inset, ring_outer - inset],
            fill=color,
        )

    # Glow: blur a bright copy, paste back under
    glow = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([0, 0, canvas_size, canvas_size], fill=(0, 255, 120, 180))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=20))

    out = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(canvas)

    # Photo itself
    if photo_path.exists():
        photo = Image.open(photo_path).convert("RGBA")
        photo = photo.resize((size, size), Image.LANCZOS)
    else:
        photo = Image.new("RGBA", (size, size), (60, 60, 60, 255))

    # Circular mask for photo
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    photo.putalpha(mask)

    offset = (canvas_size - size) // 2
    out.paste(photo, (offset, offset), photo)
    return out


def draw_verified_badge(draw: ImageDraw.ImageDraw, x: int, y: int, size: int):
    """Twitter-style blue verified checkmark."""
    draw.ellipse([x, y, x + size, y + size], fill=TWITTER_BLUE)
    # Checkmark
    cx, cy = x + size / 2, y + size / 2
    s = size * 0.28
    points = [
        (cx - s, cy),
        (cx - s * 0.2, cy + s * 0.75),
        (cx + s, cy - s * 0.6),
    ]
    draw.line([points[0], points[1]], fill=WHITE, width=max(4, size // 12))
    draw.line([points[1], points[2]], fill=WHITE, width=max(4, size // 12))


def wrap_text(text: str, font, max_width: int, draw: ImageDraw.ImageDraw):
    """Word-wrap preserving explicit \\n line breaks."""
    out_lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            w = draw.textlength(candidate, font=font)
            if w <= max_width:
                line = candidate
            else:
                if line:
                    out_lines.append(line)
                line = word
        if line:
            out_lines.append(line)
    return out_lines


def pick_quote_font_size(quote: str, max_width: int, max_height: int, draw: ImageDraw.ImageDraw):
    """Auto-shrink the quote font until it fits the content area."""
    for size in range(88, 40, -4):
        font = load_font(size, bold=True)
        lines = wrap_text(quote, font, max_width, draw)
        bbox = font.getbbox("Ag")
        line_h = (bbox[3] - bbox[1]) + 16
        total_h = line_h * len(lines)
        if total_h <= max_height:
            return font, lines, line_h
    font = load_font(40, bold=True)
    lines = wrap_text(quote, font, max_width, draw)
    bbox = font.getbbox("Ag")
    line_h = (bbox[3] - bbox[1]) + 16
    return font, lines, line_h


# ---------- MAIN RENDER ----------
def render_card(post: dict, author: dict, output_path: Path):
    card = Image.new("RGB", (CARD_W, CARD_H), WHITE)
    draw = ImageDraw.Draw(card)

    # Top + bottom black bars
    draw.rectangle([0, 0, CARD_W, BAR_H], fill=BLACK)
    draw.rectangle([0, CARD_H - BAR_H, CARD_W, CARD_H], fill=BLACK)

    # Avatar
    avatar = make_avatar(PHOTO_PATH, AVATAR_SIZE)
    avatar_x = PADDING
    avatar_y = BAR_H + 130
    card.paste(avatar, (avatar_x, avatar_y), avatar)

    # Name + handle block (to the right of avatar)
    name_font = load_font(48, bold=True)
    handle_font = load_font(34, bold=False)
    name_x = avatar_x + avatar.width + 24
    name_y = avatar_y + 40
    draw.text((name_x, name_y), author["name"], font=name_font, fill=DARK_TEXT)

    # Verified badge right after the name
    name_w = draw.textlength(author["name"], font=name_font)
    draw_verified_badge(
        draw,
        int(name_x + name_w + 14),
        int(name_y + 8),
        VERIFIED_SIZE,
    )

    # Handle
    draw.text(
        (name_x, name_y + 60),
        author["handle"],
        font=handle_font,
        fill=GRAY,
    )

    # Quote area
    quote_top = avatar_y + avatar.height + 80
    quote_bottom = CARD_H - BAR_H - 80
    quote_max_w = CARD_W - PADDING * 2
    quote_max_h = quote_bottom - quote_top

    font, lines, line_h = pick_quote_font_size(
        post["quote"], quote_max_w, quote_max_h, draw
    )

    total_h = line_h * len(lines)
    y = quote_top + (quote_max_h - total_h) // 2
    for line in lines:
        draw.text((PADDING, y), line, font=font, fill=DARK_TEXT)
        y += line_h

    output_path.parent.mkdir(parents=True, exist_ok=True)
    card.save(output_path, "PNG", optimize=True)
    print(f"Saved {output_path.name}")


def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    author = data["author"]
    for post in data["posts"]:
        filename = f"quote_{post['id']:02d}.png"
        render_card(post, author, OUT_DIR / filename)

    print(f"\nDone. {len(data['posts'])} cards in {OUT_DIR}")


if __name__ == "__main__":
    main()
