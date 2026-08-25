#!/usr/bin/env python3
"""Build full Apoliq site: NIFC-style portal + thick TechLAB service/news content."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TL = Path("/home/vananh/huong-dan/he-thong-du-an/03_KiemNghiem/kiemnghiem-techlab")

PHONE_D = "0917 333 965"
PHONE_T = "+84917333965"
EMAIL = "info@apoliq.com"
ADDR = "K2-15 Võ Nguyên Giáp, P. Hưng Phú, TP. Cần Thơ"
BRAND = "Apoliq"
BRAND_FULL = "APOLIQ SCIENCE AND TECHNOLOGY JOINT STOCK COMPANY"
BRAND_VI = "Công ty Cổ phần Khoa học và Công nghệ Apoliq"
SITE = "https://make-qr.github.io/apoliq.com"

SERVICE_MAP = {
    "kiem-nghiem-thuc-pham.html": ("dich-vu/kiem-nghiem", "thuc-pham.html", 3),
    "kiem-nghiem-banh-keo.html": ("dich-vu/kiem-nghiem", "banh-keo.html", 3),
    "kiem-nghiem-nuoc-giai-khat.html": ("dich-vu/kiem-nghiem", "nuoc-uong.html", 3),
    "kiem-nghiem-duoc-pham.html": ("dich-vu/kiem-nghiem", "duoc-pham.html", 3),
    "kiem-nghiem-my-pham.html": ("dich-vu/kiem-nghiem", "my-pham.html", 3),
    "kiem-nghiem-thuc-an-chan-nuoi.html": ("dich-vu/kiem-nghiem", "thuc-an-chan-nuoi.html", 3),
    "kiem-nghiem-dinh-duong.html": ("dich-vu/kiem-nghiem", "dinh-duong.html", 3),
    "dich-vu-kiem-nghiem-khac.html": ("dich-vu/kiem-nghiem", "khac.html", 3),
    "chung-nhan-haccp.html": ("dich-vu/chung-nhan", "haccp.html", 3),
    "chung-nhan-iso-22000.html": ("dich-vu/chung-nhan", "iso-22000.html", 3),
    "chung-nhan-vietgap.html": ("dich-vu/chung-nhan", "vietgap.html", 3),
    "chung-nhan-organic.html": ("dich-vu/chung-nhan", "organic.html", 3),
    "chung-nhan-halal.html": ("dich-vu/chung-nhan", "halal.html", 3),
    "chung-nhan-smeta-sedex.html": ("dich-vu/chung-nhan", "smeta-sedex.html", 3),
    "quan-trac-moi-truong.html": ("dich-vu/moi-truong", "quan-trac.html", 3),
    "tu-van-moi-truong.html": ("dich-vu/moi-truong", "tu-van.html", 3),
}

# Internal link rewrites inside ported HTML
LINK_REWRITES = [
    (r'href="kiem-nghiem-thuc-pham\.html"', 'href="thuc-pham.html"'),
    (r'href="kiem-nghiem-banh-keo\.html"', 'href="banh-keo.html"'),
    (r'href="kiem-nghiem-nuoc-giai-khat\.html"', 'href="nuoc-uong.html"'),
    (r'href="kiem-nghiem-duoc-pham\.html"', 'href="duoc-pham.html"'),
    (r'href="kiem-nghiem-my-pham\.html"', 'href="my-pham.html"'),
    (r'href="kiem-nghiem-thuc-an-chan-nuoi\.html"', 'href="thuc-an-chan-nuoi.html"'),
    (r'href="kiem-nghiem-dinh-duong\.html"', 'href="dinh-duong.html"'),
    (r'href="dich-vu-kiem-nghiem-khac\.html"', 'href="khac.html"'),
    (r'href="chung-nhan-haccp\.html"', 'href="../chung-nhan/haccp.html"'),
    (r'href="chung-nhan-iso-22000\.html"', 'href="../chung-nhan/iso-22000.html"'),
    (r'href="chung-nhan-vietgap\.html"', 'href="../chung-nhan/vietgap.html"'),
    (r'href="chung-nhan-organic\.html"', 'href="../chung-nhan/organic.html"'),
    (r'href="chung-nhan-halal\.html"', 'href="../chung-nhan/halal.html"'),
    (r'href="chung-nhan-smeta-sedex\.html"', 'href="../chung-nhan/smeta-sedex.html"'),
    (r'href="quan-trac-moi-truong\.html"', 'href="../moi-truong/quan-trac.html"'),
    (r'href="tu-van-moi-truong\.html"', 'href="../moi-truong/tu-van.html"'),
    (r'href="\.\./ho-so-nang-luc\.html"', 'href="../../nang-luc/index.html"'),
    (r'href="\.\./index\.html"', 'href="../../index.html"'),
    (r'href="\.\./tin-tuc/"', 'href="../../tin-tuc/"'),
    (r'href="\.\./tin-tuc/index\.html"', 'href="../../tin-tuc/index.html"'),
    (r'src="\.\./images/', 'src="../../images/'),
    (r"url\('\.\./images/", "url('../../images/"),
    (r'href="\.\./css/', 'href="../../css/'),
    (r'src="\.\./js/', 'src="../../js/'),
]


def rebrand(text: str) -> str:
    reps = [
        ("TechLAB Global", BRAND),
        ("TechLAB", BRAND),
        ("TechLab", BRAND),
        ("techlabglobal.com.vn", "apoliq.com"),
        ("kiemnghiem.techlabglobal.com.vn", "make-qr.github.io/apoliq.com"),
        ("0899.551.228", PHONE_D),
        ("0899551228", PHONE_T.replace("+", "")),
        ("tel:0899551228", f"tel:{PHONE_T}"),
        ("0907.61.69.69", PHONE_D),
        ("tel:0907616969", f"tel:{PHONE_T}"),
        ("0907616969", PHONE_T.replace("+", "")),
        ("0901 339 669", PHONE_D),
        ("+84901339669", PHONE_T),
        ("84901339669", PHONE_T.replace("+", "")),
        ("info@techlabglobal.com.vn", EMAIL),
        ("contact@techlabglobal.com.vn", EMAIL),
        ("VALAS 217", "ISO/IEC 17025"),
        ("(VALAS 217)", ""),
        ("VACI - ISO/IEC 17025", "ISO/IEC 17025"),
        ("VACI", "tổ chức công nhận"),
        ("mã VALAS 217", "tiêu chuẩn ISO/IEC 17025"),
        ("mã số VALAS 217", "tiêu chuẩn ISO/IEC 17025"),
        ("Công ty Cổ phần Khoa học và Công nghệ TechLAB Global", BRAND_VI),
        ("https://zalo.me/2097486021894945291", f"mailto:{EMAIL}"),
        ("https://m.me/61555675322896", f"tel:{PHONE_T}"),
        ("https://www.facebook.com/profile.php?id=61555675322896&locale=vi_VN", f"mailto:{EMAIL}"),
        ("https://formsubmit.co/cc4dea94548699c59cc882053a7052fe", f"mailto:{EMAIL}"),
        ("Hà Nội: Tòa nhà 9 tầng, Km11, Quốc Lộ 21", f"Cần Thơ: {ADDR}"),
        ("Cần Thơ: Số CC-15, đường số 12, KDC công ty 8, KV2, P. Hưng Thạnh", f"Trụ sở: {ADDR}"),
        ("HCM: Lô II-1, Đường số 1, KCN Tân Bình, P. Tây Thạnh", "Nhận mẫu CT · HN · HCM qua hotline / email"),
        ("Nhận mẫu CT · HN · HCM", "Nhận mẫu CT · HN · HCM"),
        ("Nhận mẫu HN·CT·HCM", "Nhận mẫu CT · HN · HCM"),
        ("Hà Nội, Cần Thơ, Hồ Chí Minh", "Cần Thơ (trụ sở) · Hà Nội · Hồ Chí Minh"),
        ("Chat Zalo", "Gửi email"),
        ("Chat với chúng tôi qua Zalo", "Liên hệ email"),
        ("Chat với chúng tôi qua Messenger", "Gọi hotline"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    # soften remaining VALAS mentions
    text = re.sub(r"\s*\(ISO/IEC 17025\)\s*\(ISO/IEC 17025\)", " (ISO/IEC 17025)", text)
    return text


def extract_main(html: str) -> tuple[str, str, str]:
    """Return title, description, main body (hero..before footer)."""
    title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "Apoliq").strip()
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    desc = desc_m.group(1) if desc_m else ""

    # cut from first service-hero / page content after season-banner
    start = None
    for pat in (
        r'<section class="service-hero"',
        r'<section class="news-article-hero"',
        r'<section class="hero"',
        r'<section class="page-hero"',
        r'<main',
        r'<article',
    ):
        m = re.search(pat, html, re.I)
        if m:
            start = m.start()
            break
    if start is None:
        # news articles often use .article-wrap or similar
        m = re.search(r'<div class="(?:article|news|post)[^"]*"', html, re.I)
        start = m.start() if m else html.find("<body")

    end_candidates = [
        html.lower().find("<footer"),
        html.lower().find("chat-widget-container"),
        html.lower().find("sticky-cta-bar"),
    ]
    ends = [e for e in end_candidates if e > 0]
    end = min(ends) if ends else len(html)
    body = html[start:end]
    # remove remaining tracking / GTM
    body = re.sub(r"<!-- Google Tag Manager[\s\S]*?<!-- End Google Tag Manager -->", "", body, flags=re.I)
    body = re.sub(r"<noscript>[\s\S]*?</noscript>", "", body, flags=re.I)
    body = re.sub(r'<script[\s\S]*?</script>', "", body, flags=re.I)
    # remove season-banner / hub-strip if still present
    body = re.sub(r'<div class="season-banner"[\s\S]*?</div>', "", body, count=1)
    body = re.sub(r'<div class="hub-strip"[\s\S]*?</div>\s*</div>', "", body, count=1)
    # simplify form to mailto
    body = re.sub(
        r'<form class="quote-form"[^>]*>',
        f'<form class="quote-form" action="mailto:{EMAIL}" method="post" enctype="text/plain">',
        body,
        count=1,
    )
    body = re.sub(r'<input type="hidden"[^>]*>\s*', "", body)
    body = re.sub(r'<input type="text" name="_honey"[^>]*>\s*', "", body)
    # remove chat widget leftovers inside body
    body = re.sub(r'<div class="chat-widget-container"[\s\S]*$', "", body)
    body = re.sub(r'<div class="sticky-cta-bar"[\s\S]*$', "", body)
    # remove client logos claiming big brands falsely for Apoliq? soften section title only via rebrand
    # remove Zalo icon images that 404
    body = re.sub(r'<img[^>]*Logo-zalo[^>]*>', "", body, flags=re.I)
    body = re.sub(r'<a[^>]*btn-hero-zalo[^>]*>[\s\S]*?</a>', "", body, flags=re.I)
    # never keep TechLAB page chrome — portal shell already mounts header/footer
    body = re.sub(r"<body[^>]*>\s*", "", body, flags=re.I)
    body = re.sub(r"</body>\s*", "", body, flags=re.I)
    body = re.sub(r"<header\b[^>]*>[\s\S]*?</header>\s*", "", body, flags=re.I)
    body = re.sub(r"<footer\b[^>]*>[\s\S]*?</footer>\s*", "", body, flags=re.I)
    return title, desc, body


def shell(title: str, description: str, depth: int, body: str, extra_css: str = "", extra_js: str = "") -> str:
    root = "../" * depth
    css_extra = "\n".join(f'  <link rel="stylesheet" href="{root}css/{c}">' for c in extra_css.split() if c)
    js_extra = "\n".join(f'  <script src="{root}js/{j}"></script>' for j in extra_js.split() if j)
    title = rebrand(title).replace("| Apoliq", "").strip()
    if "Apoliq" not in title:
        title = f"{title} | Apoliq"
    description = rebrand(description)
    body = rebrand(body)
    for pat, rep in LINK_REWRITES:
        body = re.sub(pat, rep, body)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="{root}css/style.css">
{css_extra}
  <link rel="icon" href="{root}images/logo.png" type="image/png">
</head>
<body data-depth="{depth}" class="service-page">
  <div id="site-header"></div>
{body}
  <div id="site-footer"></div>
  <script src="{root}js/main.js"></script>
{js_extra}
</body>
</html>
"""


def port_services():
    for src_name, (outdir, dest_name, depth) in SERVICE_MAP.items():
        src = TL / "pages" / src_name
        if not src.exists():
            print("missing", src)
            continue
        html = src.read_text(encoding="utf-8", errors="ignore")
        title, desc, body = extract_main(html)
        # Fix sibling links for same folder vs cross folder
        if "chung-nhan" in outdir:
            body = body.replace('href="../chung-nhan/', 'href="')
        if "moi-truong" in outdir:
            body = body.replace('href="../moi-truong/', 'href="')
        if "kiem-nghiem" in outdir:
            # chung-nhan links already ../chung-nhan/
            pass
        page = shell(title, desc, depth, body, extra_css="service-page.css", extra_js="site.js")
        dest = ROOT / outdir / dest_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8")
        print("service", dest.relative_to(ROOT))


def port_news():
    news_dir = TL / "tin-tuc"
    out = ROOT / "tin-tuc"
    out.mkdir(parents=True, exist_ok=True)
    items = []
    for src in sorted(news_dir.glob("*.html")):
        if src.name in {"index.html"}:
            continue
        # skip VALAS-branded article or rebrand it
        html = src.read_text(encoding="utf-8", errors="ignore")
        title, desc, body = extract_main(html)
        # news pages: adjust image paths depth 1
        body = body.replace('src="../images/', 'src="../images/')
        body = body.replace("url('../images/", "url('../images/")
        body = re.sub(r'href="(?!https?:|#|mailto:|tel:)([^"]+\.html)"', r'href="\1"', body)
        # relative service links from tin-tuc
        body = body.replace('href="../pages/', 'href="../dich-vu/')
        for old, new in [
            ("kiem-nghiem-thuc-pham.html", "kiem-nghiem/thuc-pham.html"),
            ("kiem-nghiem-banh-keo.html", "kiem-nghiem/banh-keo.html"),
            ("kiem-nghiem-nuoc-giai-khat.html", "kiem-nghiem/nuoc-uong.html"),
            ("kiem-nghiem-duoc-pham.html", "kiem-nghiem/duoc-pham.html"),
            ("kiem-nghiem-my-pham.html", "kiem-nghiem/my-pham.html"),
            ("kiem-nghiem-thuc-an-chan-nuoi.html", "kiem-nghiem/thuc-an-chan-nuoi.html"),
            ("kiem-nghiem-dinh-duong.html", "kiem-nghiem/dinh-duong.html"),
            ("dich-vu-kiem-nghiem-khac.html", "kiem-nghiem/khac.html"),
            ("chung-nhan-haccp.html", "chung-nhan/haccp.html"),
            ("chung-nhan-iso-22000.html", "chung-nhan/iso-22000.html"),
            ("chung-nhan-vietgap.html", "chung-nhan/vietgap.html"),
            ("chung-nhan-organic.html", "chung-nhan/organic.html"),
            ("chung-nhan-halal.html", "chung-nhan/halal.html"),
            ("chung-nhan-smeta-sedex.html", "chung-nhan/smeta-sedex.html"),
            ("quan-trac-moi-truong.html", "moi-truong/quan-trac.html"),
            ("tu-van-moi-truong.html", "moi-truong/tu-van.html"),
            ("../ho-so-nang-luc.html", "../nang-luc/index.html"),
        ]:
            body = body.replace(old, new)

        # For news, LINK_REWRITES used ../../ which is wrong — re-fix after shell
        page = shell(title, desc, 1, body, extra_css="service-page.css news.css", extra_js="site.js")
        # undo wrong ../../ from LINK_REWRITES for depth-1 pages inside body only — shell already applied
        page = page.replace('src="../../images/', 'src="../images/')
        page = page.replace("url('../../images/", "url('../images/")
        page = page.replace('href="../../index.html"', 'href="../index.html"')
        page = page.replace('href="../../tin-tuc/"', 'href="./"')
        page = page.replace('href="../../nang-luc/index.html"', 'href="../nang-luc/index.html"')
        page = page.replace('href="../../dich-vu/', 'href="../dich-vu/')
        # wrong ../chung-nhan from service rewrite inside news
        page = page.replace('href="../chung-nhan/', 'href="../dich-vu/chung-nhan/')
        page = page.replace('href="../moi-truong/', 'href="../dich-vu/moi-truong/')

        dest = out / src.name
        dest.write_text(page, encoding="utf-8")
        clean_title = re.sub(r"\s*\|\s*Apoliq.*$", "", rebrand(title)).strip()
        items.append((src.name, clean_title))
        print("news", src.name)

    # news index
    cards = "\n".join(
        f'        <li><div class="news-thumb">TIN</div><div><a href="{fn}">{title}</a></div></li>'
        for fn, title in items
    )
    index_body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Tin tức</div>
      <h1>Tin tức – Kiến thức chuyên môn</h1>
      <p>Bài viết kỹ thuật và hướng dẫn kiểm nghiệm, chứng nhận, môi trường dành cho doanh nghiệp.</p>
    </div>
  </section>
  <section class="content">
    <div class="container">
      <ul class="news-list news-list-dense">
{cards}
      </ul>
    </div>
  </section>
"""
    (out / "index.html").write_text(
        shell("Tin tức | Apoliq", "Tin tức và kiến thức kiểm nghiệm Apoliq", 1, index_body),
        encoding="utf-8",
    )
    return items


def copy_assets():
    img = ROOT / "images"
    img.mkdir(exist_ok=True)
    # banners
    src_b = TL / "images" / "banners"
    dst_b = img / "banners"
    if src_b.exists():
        if dst_b.exists():
            shutil.rmtree(dst_b)
        shutil.copytree(src_b, dst_b)
    # hero if exists
    for name in ("hero-banner.jpg", "hero-banner-trang-chu.png"):
        s = TL / "images" / name
        if s.exists():
            shutil.copy2(s, img / name)
    # copy techlab service CSS adapted
    sp = (TL / "css" / "service-page.css").read_text(encoding="utf-8")
    # remap CSS variables to Apoliq tokens
    sp = sp.replace("var(--primary-color)", "var(--cyan-deep)")
    sp = sp.replace("var(--primary-dark)", "var(--cyan-deep)")
    sp = sp.replace("var(--accent-color)", "var(--green)")
    sp = sp.replace("var(--white)", "#fff")
    # soften red hover
    sp = sp.replace("#c41820", "#067a38")
    (ROOT / "css" / "service-page.css").write_text(sp, encoding="utf-8")

    news_css = """
.article-body, .news-article, .post-content, .article-content { max-width: 820px; margin: 0 auto; padding: 1.5rem 0 2.5rem; }
.article-body h1, .news-article h1 { color: var(--cyan-deep); }
.article-body h2, .news-article h2 { color: var(--cyan-deep); margin-top: 1.6rem; }
.article-body img, .news-article img { border-radius: 10px; margin: 1rem 0; }
.news-list-dense li { padding: .85rem 0; }
.page-hero { margin-bottom: 0; }
"""
    (ROOT / "css" / "news.css").write_text(news_css, encoding="utf-8")
    print("assets copied")


def write_portal_pages(news_items: list[tuple[str, str]]):
    def page(path, title, desc, depth, body):
        p = ROOT / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(shell(title, desc, depth, body), encoding="utf-8")
        print("portal", path)

    # Giới thiệu pages (NIFC structure, Apoliq content — not government claims)
    page(
        "gioi-thieu/index.html",
        "Giới thiệu chung | Apoliq",
        "Giới thiệu APOLIQ SCIENCE AND TECHNOLOGY JOINT STOCK COMPANY",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Giới thiệu</div>
    <h1>Giới thiệu chung</h1>
    <p>{BRAND_FULL} — đồng hành cùng doanh nghiệp kiểm soát chất lượng, chứng nhận và tuân thủ môi trường.</p>
  </div></section>
  <section class="content"><div class="container content-grid">
    <article class="prose">
      <p><strong>{BRAND_FULL}</strong> ({BRAND_VI}) cung cấp dịch vụ kiểm nghiệm sản phẩm, tư vấn chứng nhận hệ thống/tiêu chuẩn và hỗ trợ hồ sơ môi trường.</p>
      <p>Định hướng của Apoliq là xây dựng cổng thông tin rõ ràng theo từng nhóm dịch vụ đang triển khai — doanh nghiệp dễ chọn đúng nhu cầu, nhận báo giá nhanh và theo dõi quy trình minh bạch.</p>
      <h2>Trụ sở</h2>
      <p>{ADDR}</p>
      <p>Hotline: <a href="tel:{PHONE_T}">{PHONE_D}</a><br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <h2>Lĩnh vực tập trung</h2>
      <ul>
        <li>Kiểm nghiệm thực phẩm, nước uống, mỹ phẩm, dược/TPCN, thức ăn chăn nuôi, dinh dưỡng và yêu cầu đặc thù</li>
        <li>Tư vấn chứng nhận HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX</li>
        <li>Quan trắc và tư vấn môi trường cho cơ sở sản xuất</li>
      </ul>
      <p><a class="btn btn-primary" href="../lien-he/index.html">Liên hệ tư vấn</a></p>
    </article>
    <aside class="side-card">
      <h3>Trong mục Giới thiệu</h3>
      <a href="index.html">Giới thiệu chung</a>
      <a href="chinh-sach-chat-luong.html">Chính sách chất lượng</a>
      <a href="co-cau-to-chuc.html">Cơ cấu tổ chức</a>
      <a href="chuc-nang.html">Chức năng – Nhiệm vụ</a>
      <a href="thanh-tich.html">Thành tích – Định hướng</a>
      <a href="../nang-luc/index.html">Năng lực</a>
    </aside>
  </div></section>
""",
    )

    page(
        "gioi-thieu/chinh-sach-chat-luong.html",
        "Chính sách chất lượng | Apoliq",
        "Chính sách chất lượng dịch vụ của Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Giới thiệu</a> / Chính sách chất lượng</div>
    <h1>Chính sách chất lượng</h1>
    <p>Cam kết về độ tin cậy, minh bạch và đúng phạm vi dịch vụ.</p>
  </div></section>
  <section class="content"><div class="container prose">
    <h2>Cam kết của Apoliq</h2>
    <ul>
      <li><strong>Chính xác:</strong> Tư vấn chỉ tiêu / phạm vi công việc phù hợp mục đích sử dụng (công bố, QC, chứng nhận, môi trường).</li>
      <li><strong>Minh bạch:</strong> Báo giá rõ ràng theo hạng mục; không đẩy dịch vụ ngoài nhu cầu.</li>
      <li><strong>Đúng menu:</strong> Chỉ nhận và hiển thị các dịch vụ đang triển khai (kiểm nghiệm, chứng nhận, môi trường).</li>
      <li><strong>Bảo mật:</strong> Thông tin khách hàng và hồ sơ được bảo vệ, chỉ dùng cho mục đích thực hiện dịch vụ.</li>
      <li><strong>Cải tiến:</strong> Cập nhật quy trình và tài liệu hướng dẫn theo phản hồi thực tế từ doanh nghiệp.</li>
    </ul>
    <p>Mọi góp ý về chất lượng dịch vụ gửi về <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div></section>
""",
    )

    page(
        "gioi-thieu/co-cau-to-chuc.html",
        "Cơ cấu tổ chức | Apoliq",
        "Cơ cấu tổ chức Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Giới thiệu</a> / Cơ cấu tổ chức</div>
    <h1>Cơ cấu tổ chức</h1>
    <p>Các khối chức năng phục vụ khách hàng doanh nghiệp.</p>
  </div></section>
  <section class="content"><div class="container card-grid">
    <div class="info-card"><h3>Ban điều hành</h3><p>Định hướng chiến lược, chất lượng dịch vụ và quan hệ khách hàng.</p></div>
    <div class="info-card"><h3>Khối Kiểm nghiệm</h3><p>Tiếp nhận yêu cầu, tư vấn chỉ tiêu, điều phối phân tích và trả kết quả.</p></div>
    <div class="info-card"><h3>Khối Chứng nhận &amp; tư vấn</h3><p>HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</p></div>
    <div class="info-card"><h3>Khối Môi trường</h3><p>Quan trắc và tư vấn hồ sơ pháp lý môi trường.</p></div>
    <div class="info-card"><h3>Chăm sóc khách hàng</h3><p>Hotline {PHONE_D} · {EMAIL}</p></div>
    <div class="info-card"><h3>Trụ sở</h3><p>{ADDR}</p></div>
  </div></section>
""",
    )

    page(
        "gioi-thieu/chuc-nang.html",
        "Chức năng – Nhiệm vụ | Apoliq",
        "Chức năng nhiệm vụ Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Giới thiệu</a> / Chức năng</div>
    <h1>Chức năng – Nhiệm vụ</h1>
  </div></section>
  <section class="content"><div class="container prose">
    <h2>1. Chức năng</h2>
    <p>Apoliq thực hiện dịch vụ kỹ thuật hỗ trợ doanh nghiệp trong kiểm soát chất lượng sản phẩm, tư vấn chứng nhận và tuân thủ môi trường — theo phạm vi dịch vụ công bố trên website.</p>
    <h2>2. Nhiệm vụ chính</h2>
    <h3>2.1. Kiểm nghiệm</h3>
    <ul>
      <li>Tư vấn gói chỉ tiêu theo loại sản phẩm và mục đích (công bố / QC / đối tác).</li>
      <li>Tiếp nhận mẫu, thực hiện phân tích và trả kết quả.</li>
      <li>Hỗ trợ doanh nghiệp hiểu cách dùng kết quả trong hồ sơ liên quan.</li>
    </ul>
    <h3>2.2. Chứng nhận &amp; tư vấn hệ thống</h3>
    <ul>
      <li>Tư vấn lộ trình HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</li>
      <li>Hỗ trợ rà soát hồ sơ, thực hành và chuẩn bị đánh giá.</li>
    </ul>
    <h3>2.3. Môi trường</h3>
    <ul>
      <li>Quan trắc môi trường theo nhu cầu cơ sở.</li>
      <li>Tư vấn hồ sơ pháp lý môi trường (ĐTM, đăng ký…).</li>
    </ul>
    <h3>2.4. Thông tin – hướng dẫn</h3>
    <ul>
      <li>Cung cấp tài liệu hướng dẫn gửi mẫu, checklist và bài viết chuyên môn trên chuyên mục Tin tức.</li>
    </ul>
  </div></section>
""",
    )

    page(
        "gioi-thieu/thanh-tich.html",
        "Thành tích – Định hướng | Apoliq",
        "Định hướng phát triển Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Giới thiệu</a> / Thành tích</div>
    <h1>Thành tích – Định hướng</h1>
  </div></section>
  <section class="content"><div class="container prose">
    <p>Apoliq xây dựng cổng dịch vụ theo hướng <strong>đủ việc đang làm, không liệt kê việc chưa nhận</strong> — giúp doanh nghiệp tránh nhầm phạm vi.</p>
    <h2>Định hướng gần</h2>
    <ul>
      <li>Mở rộng thư viện bài viết kỹ thuật – chuyên môn (kiểm nghiệm, chứng nhận, môi trường).</li>
      <li>Chuẩn hóa quy trình báo giá và hướng dẫn gửi mẫu.</li>
      <li>Nâng trải nghiệm website (tra cứu dịch vụ, FAQ, liên hệ nhanh).</li>
    </ul>
    <p>Liên hệ hợp tác: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_T}">{PHONE_D}</a></p>
  </div></section>
""",
    )

    # Năng lực
    page(
        "nang-luc/index.html",
        "Năng lực | Apoliq",
        "Danh mục năng lực dịch vụ Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Năng lực</div>
    <h1>Danh mục năng lực</h1>
    <p>Chỉ các nhóm năng lực Apoliq đang cung cấp — tương ứng menu Dịch vụ.</p>
  </div></section>
  <section class="section"><div class="container">
    <h2 class="section-title">Kiểm nghiệm</h2>
    <div class="card-grid">
      <a class="info-card" href="../dich-vu/kiem-nghiem/thuc-pham.html"><h3>Thực phẩm</h3><p>Vi sinh, hóa lý, phụ gia, kim loại nặng…</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/banh-keo.html"><h3>Bánh kẹo</h3><p>Gói mùa vụ, công bố TCCS.</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/nuoc-uong.html"><h3>Nước uống</h3><p>Theo QCVN / nhu cầu QC.</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/duoc-pham.html"><h3>Dược / TPCN</h3><p>Hóa lý, vi sinh, hồ sơ liên quan.</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/my-pham.html"><h3>Mỹ phẩm</h3><p>Chỉ tiêu phổ biến theo loại SP.</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/thuc-an-chan-nuoi.html"><h3>Thức ăn chăn nuôi</h3><p>Protein, aflatoxin, vi sinh…</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/dinh-duong.html"><h3>Dinh dưỡng / nhãn</h3><p>Đối soát thông tin dinh dưỡng.</p></a>
      <a class="info-card" href="../dich-vu/kiem-nghiem/khac.html"><h3>Khác / R&amp;D</h3><p>Yêu cầu đặc thù, bao bì FCM…</p></a>
    </div>
    <h2 class="section-title" style="margin-top:2rem">Chứng nhận</h2>
    <div class="card-grid">
      <a class="info-card" href="../dich-vu/chung-nhan/haccp.html"><h3>HACCP</h3><p>Xưởng thực phẩm, đồ uống.</p></a>
      <a class="info-card" href="../dich-vu/chung-nhan/iso-22000.html"><h3>ISO 22000</h3><p>Hệ thống ATTP.</p></a>
      <a class="info-card" href="../dich-vu/chung-nhan/vietgap.html"><h3>VietGAP</h3><p>Sản xuất nông nghiệp.</p></a>
      <a class="info-card" href="../dich-vu/chung-nhan/organic.html"><h3>Organic</h3><p>Hữu cơ.</p></a>
      <a class="info-card" href="../dich-vu/chung-nhan/halal.html"><h3>Halal</h3><p>Thị trường Halal.</p></a>
      <a class="info-card" href="../dich-vu/chung-nhan/smeta-sedex.html"><h3>SMETA / SEDEX</h3><p>Audit chuỗi cung ứng.</p></a>
    </div>
    <h2 class="section-title" style="margin-top:2rem">Môi trường</h2>
    <div class="card-grid">
      <a class="info-card" href="../dich-vu/moi-truong/quan-trac.html"><h3>Quan trắc</h3><p>Nước thải, khí, đất…</p></a>
      <a class="info-card" href="../dich-vu/moi-truong/tu-van.html"><h3>Tư vấn hồ sơ</h3><p>ĐTM, đăng ký môi trường…</p></a>
    </div>
    <p style="margin-top:1.5rem"><a class="btn btn-primary" href="../dich-vu/kiem-nghiem/huong-dan-gui-mau.html">Hướng dẫn gửi mẫu</a></p>
  </div></section>
""",
    )

    page(
        "nang-luc/trang-thiet-bi.html",
        "Trang thiết bị | Apoliq",
        "Hướng trang thiết bị phục vụ kiểm nghiệm tại Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Năng lực</a> / Trang thiết bị</div>
    <h1>Trang thiết bị</h1>
    <p>Hạ tầng phục vụ các phép thử hóa học và sinh học theo nhu cầu dịch vụ đang triển khai.</p>
  </div></section>
  <section class="content"><div class="container card-grid">
    <div class="info-card"><h3>Lĩnh vực hóa học</h3><p>Phân tích thành phần, kim loại nặng, phụ gia, chỉ tiêu hóa lý trên nền mẫu thực phẩm và liên quan.</p></div>
    <div class="info-card"><h3>Lĩnh vực sinh học</h3><p>Vi sinh thực phẩm, nước uống và các chỉ tiêu sinh học phục vụ QC / công bố.</p></div>
    <div class="info-card"><h3>Hỗ trợ chứng nhận</h3><p>Dữ liệu kiểm nghiệm định kỳ hỗ trợ duy trì hệ thống HACCP / ISO 22000.</p></div>
    <div class="info-card"><h3>Liên hệ khảo sát năng lực</h3><p>Gửi chỉ tiêu cần kiểm: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  </div></section>
""",
    )

    # Hướng dẫn gửi mẫu
    page(
        "dich-vu/kiem-nghiem/huong-dan-gui-mau.html",
        "Hướng dẫn gửi mẫu kiểm nghiệm | Apoliq",
        "Hướng dẫn chuẩn bị và gửi mẫu kiểm nghiệm tới Apoliq",
        2,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../../index.html">Trang chủ</a> / <a href="index.html">Kiểm nghiệm</a> / Hướng dẫn gửi mẫu</div>
    <h1>Hướng dẫn gửi mẫu kiểm nghiệm</h1>
    <p>Chuẩn bị đúng thông tin giúp báo giá nhanh và tránh phải lấy lại mẫu.</p>
  </div></section>
  <section class="content"><div class="container prose">
    <h2>1. Thông tin cần gửi khi liên hệ</h2>
    <ul>
      <li>Tên sản phẩm / loại mẫu</li>
      <li>Mục đích: công bố, QC định kỳ, đối soát đối tác, R&amp;D…</li>
      <li>Số lượng mẫu dự kiến</li>
      <li>Chỉ tiêu đã biết (nếu có) hoặc yêu cầu tư vấn gói</li>
      <li>Thời gian cần kết quả</li>
    </ul>
    <h2>2. Cách gửi yêu cầu</h2>
    <ul>
      <li>Hotline: <a href="tel:{PHONE_T}">{PHONE_D}</a></li>
      <li>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>Form: <a href="../../lien-he/index.html">Trang Liên hệ</a></li>
    </ul>
    <h2>3. Lưu ý bảo quản mẫu</h2>
    <ul>
      <li>Đóng gói kín, ghi nhãn rõ ràng (tên mẫu, ngày lấy).</li>
      <li>Mẫu cần lạnh: giữ nhiệt độ phù hợp trong quá trình vận chuyển.</li>
      <li>Không gửi mẫu thiếu thông tin — dễ chậm báo giá.</li>
    </ul>
    <p><a class="btn btn-primary" href="../../lien-he/index.html">Gửi yêu cầu ngay</a></p>
  </div></section>
""",
    )

    # Category indexes thick
    for cat, title, blurb, links in [
        (
            "kiem-nghiem",
            "Dịch vụ Kiểm nghiệm",
            "Danh mục kiểm nghiệm đang triển khai tại Apoliq.",
            [
                ("thuc-pham.html", "Kiểm nghiệm Thực phẩm"),
                ("banh-keo.html", "Kiểm nghiệm Bánh kẹo"),
                ("nuoc-uong.html", "Kiểm nghiệm Nước uống"),
                ("duoc-pham.html", "Kiểm nghiệm Dược / TPCN"),
                ("my-pham.html", "Kiểm nghiệm Mỹ phẩm"),
                ("thuc-an-chan-nuoi.html", "Kiểm nghiệm Thức ăn chăn nuôi"),
                ("dinh-duong.html", "Phân tích dinh dưỡng / ghi nhãn"),
                ("khac.html", "Dịch vụ kiểm nghiệm khác"),
                ("huong-dan-gui-mau.html", "Hướng dẫn gửi mẫu"),
            ],
        ),
        (
            "chung-nhan",
            "Dịch vụ Chứng nhận",
            "Tư vấn chứng nhận hệ thống và tiêu chuẩn.",
            [
                ("haccp.html", "HACCP"),
                ("iso-22000.html", "ISO 22000"),
                ("vietgap.html", "VietGAP"),
                ("organic.html", "Organic"),
                ("halal.html", "Halal"),
                ("smeta-sedex.html", "SMETA / SEDEX"),
            ],
        ),
        (
            "moi-truong",
            "Dịch vụ Môi trường",
            "Quan trắc và tư vấn hồ sơ môi trường.",
            [
                ("quan-trac.html", "Quan trắc môi trường"),
                ("tu-van.html", "Tư vấn môi trường"),
            ],
        ),
    ]:
        cards = "\n".join(
            (
                f'<a class="service-tile" href="{href}">'
                f'<div class="visual"><img src="../../images/dich-vu/{Path(href).stem}.jpg?v=1" alt="{label}" width="480" height="320" loading="lazy"></div>'
                f'<div class="body"><h3>{label}</h3><span class="btn btn-outline">Xem chi tiết</span></div></a>'
            )
            for href, label in links
        )
        page(
            f"dich-vu/{cat}/index.html",
            f"{title} | Apoliq",
            blurb,
            2,
            f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../../index.html">Trang chủ</a> / {title}</div>
    <h1>{title}</h1>
    <p>{blurb}</p>
  </div></section>
  <section class="section"><div class="container service-grid">{cards}</div></section>
""",
        )

    # Văn bản
    page(
        "van-ban/index.html",
        "Văn bản – Tài liệu | Apoliq",
        "Tài liệu hướng dẫn Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Văn bản</div>
    <h1>Văn bản – Tài liệu</h1>
  </div></section>
  <section class="content"><div class="container card-grid">
    <a class="info-card" href="../dich-vu/kiem-nghiem/huong-dan-gui-mau.html"><h3>Hướng dẫn gửi mẫu</h3><p>Chuẩn bị thông tin và bảo quản mẫu.</p></a>
    <a class="info-card" href="../tin-tuc/gui-mau-kiem-nghiem-can-chuan-bi-gi.html"><h3>Checklist gửi mẫu</h3><p>Bài viết chi tiết.</p></a>
    <a class="info-card" href="../tin-tuc/bao-gia-kiem-nghiem-gom-nhung-gi.html"><h3>Báo giá gồm những gì</h3><p>Hiểu cấu phần báo giá.</p></a>
    <a class="info-card" href="../tin-tuc/haccp-va-iso-22000-khac-nhau.html"><h3>HACCP vs ISO 22000</h3><p>Phân biệt nhanh.</p></a>
    <a class="info-card" href="../tin-tuc/chung-nhan-vietgap-quy-trinh.html"><h3>Quy trình VietGAP</h3><p>Các bước phổ biến.</p></a>
    <a class="info-card" href="../lien-he/index.html"><h3>Yêu cầu tài liệu</h3><p>Email {EMAIL}</p></a>
  </div></section>
""",
    )

    # Liên hệ
    page(
        "lien-he/index.html",
        "Hỏi đáp – Liên hệ | Apoliq",
        "Liên hệ báo giá Apoliq",
        1,
        f"""
  <section class="page-hero"><div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Liên hệ</div>
    <h1>Hỏi đáp – Liên hệ</h1>
  </div></section>
  <section class="content"><div class="container content-grid">
    <div>
      <div class="contact-box" style="margin-bottom:1.2rem">
        <div><strong>Địa chỉ</strong><br>{ADDR}</div>
        <div><strong>Điện thoại</strong><br><a href="tel:{PHONE_T}">{PHONE_D}</a></div>
        <div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      </div>
      <form class="quote-form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
        <label>Họ tên<input name="name" required></label>
        <label>Số điện thoại<input name="phone" required></label>
        <label>Email<input type="email" name="email"></label>
        <label>Nhóm dịch vụ<select name="service"><option>Kiểm nghiệm</option><option>Chứng nhận</option><option>Môi trường</option><option>Khác</option></select></label>
        <label>Nội dung<textarea name="message" rows="6" required placeholder="Tên sản phẩm, chỉ tiêu, số mẫu..."></textarea></label>
        <button class="btn btn-primary" type="submit">Gửi yêu cầu</button>
      </form>
    </div>
    <aside class="side-card">
      <h3>FAQ</h3>
      <p><strong>Thời gian báo giá?</strong><br>Thường trong ngày làm việc khi đủ thông tin.</p>
      <p><strong>Có hiệu chuẩn / giám định không?</strong><br>Hiện chưa — không hiển thị trên menu.</p>
      <p><strong>Xem danh mục đầy đủ?</strong><br><a href="../nang-luc/index.html">Năng lực dịch vụ</a></p>
    </aside>
  </div></section>
""",
    )

    # Homepage — NIFC-like dense portal
    tech_news = news_items[:6]
    act_news = news_items[6:12]
    more_news = news_items[12:20]

    def li(items):
        return "\n".join(
            f'<li><div class="news-thumb">TIN</div><div><a href="tin-tuc/{fn}">{tt}</a></div></li>'
            for fn, tt in items
        )

    home_body = f"""
  <div class="ticker"><div class="container" style="display:flex;align-items:center;gap:.75rem;width:min(100% - 2rem,1180px)">
    <span class="ticker-badge">TIN HOT</span>
    <div class="ticker-track"><span>Apoliq nhận kiểm nghiệm thực phẩm · nước uống · mỹ phẩm · dược/TPCN · Tư vấn HACCP/ISO 22000/VietGAP/Organic/Halal/SMETA · Quan trắc &amp; tư vấn môi trường · Hotline {PHONE_D} · {EMAIL} · Hướng dẫn gửi mẫu trên website</span></div>
  </div></div>

  <section class="container home-grid">
    <div class="panel">
      <div class="panel-head">Tin mới</div>
      <div class="panel-body feature-card">
        <img src="images/banners/kiem-nghiem-thuc-pham.jpg" alt="Kiểm nghiệm" loading="lazy" onerror="this.style.display='none'">
        <h3><a href="tin-tuc/{tech_news[0][0] if tech_news else 'index.html'}">{tech_news[0][1] if tech_news else 'Tin tức Apoliq'}</a></h3>
        <p class="meta">Kỹ thuật – Chuyên môn</p>
        <p>Cập nhật kiến thức kiểm nghiệm và chứng nhận giúp doanh nghiệp chọn đúng gói dịch vụ, chuẩn bị hồ sơ và rút ngắn thời gian xử lý.</p>
        <a class="btn btn-primary" href="lien-he/index.html">Nhận báo giá</a>
        <a class="btn btn-outline" href="dich-vu/kiem-nghiem/huong-dan-gui-mau.html">Hướng dẫn gửi mẫu</a>
      </div>
    </div>
    <div class="panel">
      <div class="panel-head">Tin hoạt động</div>
      <div class="panel-body"><ul class="news-list">{li(act_news or tech_news)}</ul></div>
    </div>
    <div class="panel">
      <div class="hotline-box"><div class="label">Hotline tư vấn</div><a href="tel:{PHONE_T}">{PHONE_D}</a></div>
      <div class="quick-links">
        <a href="dich-vu/kiem-nghiem/index.html"><span class="ico">KN</span>Danh mục kiểm nghiệm</a>
        <a href="dich-vu/chung-nhan/index.html"><span class="ico">CN</span>Danh mục chứng nhận</a>
        <a href="dich-vu/moi-truong/index.html"><span class="ico">MT</span>Dịch vụ môi trường</a>
        <a href="dich-vu/kiem-nghiem/huong-dan-gui-mau.html"><span class="ico">HD</span>Hướng dẫn gửi mẫu</a>
        <a href="nang-luc/index.html"><span class="ico">NL</span>Năng lực dịch vụ</a>
        <a href="nang-luc/trang-thiet-bi.html"><span class="ico">TB</span>Trang thiết bị</a>
        <a href="tin-tuc/index.html"><span class="ico">TT</span>Tin tức – kiến thức</a>
        <a href="lien-he/index.html"><span class="ico">BG</span>Báo giá / Liên hệ</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="section-title">Dịch vụ</h2>
      <div class="service-grid">
        <a class="service-tile" href="dich-vu/kiem-nghiem/index.html"><div class="visual">KN</div><div class="body"><h3>Kiểm nghiệm</h3><p>Thực phẩm, bánh kẹo, nước, mỹ phẩm, dược/TPCN, TACN, dinh dưỡng…</p><span class="btn btn-outline">Xem chi tiết</span></div></a>
        <a class="service-tile" href="dich-vu/chung-nhan/index.html"><div class="visual">CN</div><div class="body"><h3>Chứng nhận</h3><p>HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</p><span class="btn btn-outline">Xem chi tiết</span></div></a>
        <a class="service-tile" href="dich-vu/moi-truong/index.html"><div class="visual">MT</div><div class="body"><h3>Môi trường</h3><p>Quan trắc và tư vấn hồ sơ môi trường cho cơ sở sản xuất.</p><span class="btn btn-outline">Xem chi tiết</span></div></a>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="container home-grid" style="padding-top:0;padding-bottom:0">
      <div class="panel">
        <div class="panel-head">Kỹ thuật – Chuyên môn</div>
        <div class="panel-body"><ul class="news-list">{li(tech_news)}</ul></div>
      </div>
      <div class="panel">
        <div class="panel-head">Tin tổng hợp</div>
        <div class="panel-body"><ul class="news-list">{li(more_news or tech_news)}</ul></div>
      </div>
      <div class="panel">
        <div class="panel-head">Giới thiệu nhanh</div>
        <div class="panel-body prose">
          <p><strong>{BRAND_FULL}</strong></p>
          <p>{ADDR}</p>
          <p><a href="gioi-thieu/index.html">Giới thiệu chung</a> · <a href="gioi-thieu/chinh-sach-chat-luong.html">Chính sách chất lượng</a> · <a href="gioi-thieu/chuc-nang.html">Chức năng – Nhiệm vụ</a></p>
          <p><a class="btn btn-secondary" href="mailto:{EMAIL}">Email {EMAIL}</a></p>
        </div>
      </div>
    </div>
  </section>
"""
    (ROOT / "index.html").write_text(
        shell(
            "Apoliq | Kiểm nghiệm – Chứng nhận – Môi trường",
            f"{BRAND_FULL} — kiểm nghiệm, chứng nhận, môi trường. Hotline {PHONE_D}.",
            0,
            home_body,
        ).replace(
            "</head>",
            f'  <link rel="canonical" href="{SITE}/">\n</head>',
            1,
        ),
        encoding="utf-8",
    )
    print("homepage written")


def update_main_js():
    js = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
    # expand intro dropdown links if missing
    if "chinh-sach-chat-luong.html" not in js:
        js = js.replace(
            """<li><a href="${root}gioi-thieu/index.html">Giới thiệu chung</a></li>
          <li><a href="${root}gioi-thieu/chuc-nang.html">Chức năng – Nhiệm vụ</a></li>
          <li><a href="${root}nang-luc/index.html">Năng lực</a></li>""",
            """<li><a href="${root}gioi-thieu/index.html">Giới thiệu chung</a></li>
          <li><a href="${root}gioi-thieu/chinh-sach-chat-luong.html">Chính sách chất lượng</a></li>
          <li><a href="${root}gioi-thieu/co-cau-to-chuc.html">Cơ cấu tổ chức</a></li>
          <li><a href="${root}gioi-thieu/chuc-nang.html">Chức năng – Nhiệm vụ</a></li>
          <li><a href="${root}gioi-thieu/thanh-tich.html">Thành tích – Định hướng</a></li>
          <li><a href="${root}nang-luc/index.html">Năng lực</a></li>
          <li><a href="${root}nang-luc/trang-thiet-bi.html">Trang thiết bị</a></li>""",
        )
    if "huong-dan-gui-mau.html" not in js:
        js = js.replace(
            '<li><a href="${root}dich-vu/kiem-nghiem/index.html"><strong>Kiểm nghiệm</strong></a></li>',
            '<li><a href="${root}dich-vu/kiem-nghiem/index.html"><strong>Kiểm nghiệm</strong></a></li>\n'
            '          <li><a href="${root}dich-vu/kiem-nghiem/huong-dan-gui-mau.html">· Hướng dẫn gửi mẫu</a></li>',
        )
    (ROOT / "js" / "main.js").write_text(js, encoding="utf-8")

    site_js = r"""
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq-item .faq-question').forEach((q) => {
    q.addEventListener('click', () => q.parentElement.classList.toggle('active'));
  });
});
"""
    (ROOT / "js" / "site.js").write_text(site_js, encoding="utf-8")


def write_readme():
    (ROOT / "README.md").write_text(
        f"""# Apoliq — Website đầy đủ

Portal kiểu [nifc.gov.vn](https://nifc.gov.vn/) + nội dung dịch vụ/tin tức dày (catalog giống TechLAB), brand **{BRAND_FULL}**.

## Live

- GitHub Pages: {SITE}/
- Repo: https://github.com/make-qr/apoliq.com

## Menu dịch vụ (chỉ hiện việc đang có)

- Kiểm nghiệm (+ hướng dẫn gửi mẫu)
- Chứng nhận (HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA)
- Môi trường (quan trắc, tư vấn)

Không có trên menu: hiệu chuẩn, giám định, TNTT, mẫu chuẩn, kiểm tra hàng nhập…

## Build lại

```bash
python3 build-full-site.py
```

## Liên hệ

- {ADDR}
- {PHONE_D}
- {EMAIL}
""",
        encoding="utf-8",
    )


def main():
    copy_assets()
    port_services()
    news_items = port_news()
    write_portal_pages(news_items)
    update_main_js()
    write_readme()
    print("DONE pages:", len(list(ROOT.rglob('*.html'))))


if __name__ == "__main__":
    main()
