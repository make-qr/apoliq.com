#!/usr/bin/env python3
"""Attach a unique hero + inline image to every news article (no reuse)."""
from __future__ import annotations

import hashlib
import re
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parent
NEWS = ROOT / "tin-tuc"
IMG_DIR = ROOT / "images" / "tin-tuc"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Topic-tinted palettes (Apoliq cyan/green family + variants) — each article gets unique hue offset
BASE_PALETTES = [
    ((14, 122, 136), (8, 152, 72)),
    ((32, 184, 200), (10, 120, 90)),
    ((0, 144, 72), (20, 184, 200)),
    ((8, 90, 110), (40, 170, 120)),
    ((20, 100, 140), (0, 150, 100)),
    ((10, 130, 150), (60, 160, 80)),
    ((30, 80, 120), (20, 160, 140)),
    ((0, 110, 130), (80, 170, 90)),
]


def slug_of(path: Path) -> str:
    return path.stem


def unique_seed(slug: str, role: str) -> int:
    h = hashlib.sha256(f"{slug}|{role}|apoliq-news-v1".encode()).hexdigest()
    return int(h[:8], 16)


def make_unique_image(slug: str, role: str, width: int, height: int, title: str) -> Path:
    """Procedural unique image — guaranteed no file reuse across posts."""
    out = IMG_DIR / f"{slug}-{role}.jpg"
    seed = unique_seed(slug, role)
    rng_r = (seed >> 0) & 255
    rng_g = (seed >> 8) & 255
    rng_b = (seed >> 16) & 255
    idx = seed % len(BASE_PALETTES)
    c1, c2 = BASE_PALETTES[idx]
    # nudge colors by seed so every image differs
    c1 = tuple(max(0, min(255, c1[i] + ((seed >> (i * 5)) & 31) - 15)) for i in range(3))
    c2 = tuple(max(0, min(255, c2[i] + ((seed >> (i * 7 + 3)) & 31) - 10)) for i in range(3))

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    # gradient background
    for y in range(height):
        t = y / max(1, height - 1)
        # add horizontal wave variation from seed
        wave = 0.08 * (((seed % 97) / 97) * 2 - 1)
        tt = min(1.0, max(0.0, t + wave * (y % 40) / 40))
        col = tuple(int(c1[i] * (1 - tt) + c2[i] * tt) for i in range(3))
        draw.line([(0, y), (width, y)], fill=col)

    # unique geometric overlays
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    n_shapes = 5 + (seed % 6)
    for i in range(n_shapes):
        s2 = (seed * (i + 3) * 2654435761) & 0xFFFFFFFF
        x0 = s2 % width
        y0 = (s2 >> 9) % height
        w = 40 + (s2 >> 17) % (width // 3)
        h = 30 + (s2 >> 23) % (height // 3)
        alpha = 40 + (s2 % 70)
        fill = (rng_r, rng_g, rng_b, alpha) if i % 2 == 0 else (c2[0], c2[1], c2[2], alpha)
        shape = (s2 >> 3) % 4
        if shape == 0:
            od.ellipse([x0 - w // 2, y0 - h // 2, x0 + w // 2, y0 + h // 2], fill=fill)
        elif shape == 1:
            od.rectangle([x0, y0, x0 + w, y0 + h], fill=fill)
        elif shape == 2:
            od.polygon(
                [(x0, y0 + h), (x0 + w // 2, y0), (x0 + w, y0 + h)],
                fill=fill,
            )
        else:
            od.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=18, fill=fill)

    # soft light band unique position
    band_y = (seed % (height - 80)) + 20
    od.rectangle([0, band_y, width, band_y + 50], fill=(255, 255, 255, 28))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img = ImageEnhance.Contrast(img).enhance(1.08)

    # caption bar
    bar = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar)
    bd.rectangle([0, height - 90, width, height], fill=(8, 40, 48, 150))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28 if role == "hero" else 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        font_small = font
    label = (title[:70] + "…") if len(title) > 70 else title
    bd.text((24, height - 72), label, fill=(255, 255, 255, 235), font=font)
    bd.text((24, height - 36), f"Apoliq · {slug}", fill=(180, 230, 235, 220), font=font_small)
    img = Image.alpha_composite(img.convert("RGBA"), bar).convert("RGB")

    # tiny unique noise fingerprint (ensures byte uniqueness even if similar)
    px = img.load()
    for i in range(64):
        x = (seed + i * 17) % width
        y = (seed // 3 + i * 29) % height
        r, g, b = px[x, y]
        px[x, y] = ((r + i) % 256, (g + seed % 7) % 256, (b + i * 3) % 256)

    img.save(out, "JPEG", quality=88, optimize=True)
    return out


def extract_title(html: str, fallback: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if m:
        return re.sub(r"\s*\|\s*Apoliq.*$", "", m.group(1)).strip()
    return fallback


def inject_images(html: str, slug: str, title: str) -> str:
    hero_rel = f"../images/tin-tuc/{slug}-hero.jpg"
    inline_rel = f"../images/tin-tuc/{slug}-inline.jpg"

    featured = (
        f'\n<figure class="news-featured">\n'
        f'  <img src="{hero_rel}" alt="{title}" width="960" height="540" loading="eager">\n'
        f"</figure>\n"
    )
    inline = (
        f'\n<figure class="news-inline">\n'
        f'  <img src="{inline_rel}" alt="{title} — minh họa" width="960" height="540" loading="lazy">\n'
        f'  <figcaption>Hình minh họa chuyên đề — Apoliq</figcaption>\n'
        f"</figure>\n"
    )

    # remove old injected figures if re-run
    html = re.sub(r'<figure class="news-featured">[\s\S]*?</figure>\s*', "", html)
    html = re.sub(r'<figure class="news-inline">[\s\S]*?</figure>\s*', "", html)

    # insert featured after hero section / before first article body content
    if '<p class="news-lead">' in html:
        html = html.replace('<p class="news-lead">', featured + '<p class="news-lead">', 1)
    elif '<article class="news-article-body">' in html:
        html = html.replace(
            '<article class="news-article-body">',
            '<article class="news-article-body">' + featured,
            1,
        )
    else:
        html = html.replace("</section>", "</section>" + featured, 1)

    # insert inline after first </h2> block inside article if possible
    m = re.search(r"</h2>\s*(?:<[^>]+>\s*)*(?:<p>|<ol>|<ul>)", html)
    if m:
        pos = m.end()
        # find end of that first content block roughly — insert before second h2
        m2 = re.search(r"<h2>", html[pos:])
        if m2:
            insert_at = pos + m2.start()
            html = html[:insert_at] + inline + html[insert_at:]
        else:
            html = html[:pos] + inline + html[pos:]
    else:
        # fallback before CTA
        if 'class="news-cta-box"' in html:
            html = html.replace('<div class="news-cta-box">', inline + '<div class="news-cta-box">', 1)
        else:
            html = html.replace("</article>", inline + "</article>", 1)

    return html


def rebuild_index(articles: list[tuple[str, str]]):
    items = []
    for fn, title in articles:
        slug = Path(fn).stem
        items.append(
            f'''        <li class="news-item-card">
          <a class="news-item-link" href="{fn}">
            <img class="news-thumb-img" src="../images/tin-tuc/{slug}-hero.jpg" alt="{title}" width="160" height="100" loading="lazy">
            <span class="news-item-title">{title}</span>
          </a>
        </li>'''
        )
    body = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tin tức | Apoliq</title>
  <meta name="description" content="Tin tức và kiến thức kiểm nghiệm Apoliq — mỗi bài kèm hình minh họa riêng.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/news.css">
  <link rel="icon" href="../images/logo.png" type="image/png">
</head>
<body data-depth="1">
  <div id="site-header"></div>
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Tin tức</div>
      <h1>Tin tức – Kiến thức chuyên môn</h1>
      <p>Bài viết kỹ thuật và hướng dẫn — mỗi bài có hình ảnh riêng, không dùng chung một ảnh.</p>
    </div>
  </section>
  <section class="content">
    <div class="container">
      <ul class="news-list news-list-dense news-list-photos">
{chr(10).join(items)}
      </ul>
    </div>
  </section>
  <div id="site-footer"></div>
  <script src="../js/main.js"></script>
</body>
</html>
"""
    (NEWS / "index.html").write_text(body, encoding="utf-8")


def update_homepage(articles: list[tuple[str, str]]):
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")
    # replace feature card image if present
    if articles:
        fn, title = articles[0]
        slug = Path(fn).stem
        html = re.sub(
            r'(<div class="panel-body feature-card">\s*)(?:<img[^>]*>|<div class="visual"[\s\S]*?</div>)',
            rf'\1<img src="images/tin-tuc/{slug}-hero.jpg" alt="{title}" loading="lazy">',
            html,
            count=1,
        )
    # replace news-thumb placeholders in home lists with images where href tin-tuc/
    def repl_li(m):
        block = m.group(0)
        hm = re.search(r'href="tin-tuc/([^"]+)"', block)
        if not hm:
            return block
        slug = Path(hm.group(1)).stem
        return re.sub(
            r'<div class="news-thumb">[^<]*</div>',
            f'<img class="news-thumb-img" src="images/tin-tuc/{slug}-hero.jpg" alt="" width="72" height="72" loading="lazy">',
            block,
            count=1,
        )

    html = re.sub(r"<li>[\s\S]*?</li>", repl_li, html)
    index.write_text(html, encoding="utf-8")


def verify_unique(paths: list[Path]) -> None:
    hashes = {}
    for p in paths:
        h = hashlib.md5(p.read_bytes()).hexdigest()
        if h in hashes:
            raise SystemExit(f"DUPLICATE IMAGE HASH: {p.name} == {hashes[h]}")
        hashes[h] = p.name
    print(f"unique_ok count={len(hashes)}")


def main():
    articles = []
    image_paths: list[Path] = []
    for path in sorted(NEWS.glob("*.html")):
        if path.name == "index.html":
            continue
        slug = slug_of(path)
        html = path.read_text(encoding="utf-8")
        title = extract_title(html, slug.replace("-", " "))
        hero = make_unique_image(slug, "hero", 960, 540, title)
        inline = make_unique_image(slug, "inline", 960, 540, title)
        image_paths.extend([hero, inline])
        html2 = inject_images(html, slug, title)
        path.write_text(html2, encoding="utf-8")
        articles.append((path.name, title))
        print("ok", slug)

    verify_unique(image_paths)
    rebuild_index(articles)
    update_homepage(articles)
    print("articles", len(articles), "images", len(image_paths))


if __name__ == "__main__":
    main()
