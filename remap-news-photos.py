#!/usr/bin/env python3
"""Remap all news hero/inline images to topic-matched Unsplash photos (validated IDs only)."""
from __future__ import annotations

import hashlib
import re
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "images" / "tin-tuc"
OUT.mkdir(parents=True, exist_ok=True)
CACHE_V = "8"

# Validated working Unsplash IDs only (checked 2026-08-07)
OK = set(
    """
1416879595882-3373a0480b5b
1426604966848-d7adac402bff
1432405972618-c60b0225b8f9
1434030216411-0b793f4b4173
1441974231531-c6227db76b6e
1441986300917-64674bd600d8
1447752875215-b2761acb3c5d
1450101499163-c8848c66ca85
1454165804606-c3d57bc86b40
1460925895917-afdab827c52f
1464226184884-fa280b87c399
1469474968028-56623f02e42e
1470071459604-3b5ec3a7fe05
1472214103451-9374bd1c798e
1475924156734-496f6cac6ec1
1485827404703-89b55fcc595e
1497366216548-37526070297c
1497366754035-f200968a6e72
1498837167922-ddd27525d352
1500382017468-9049fed747ef
1500534314209-a25ddb2bd429
1501594907352-04cda38ebc29
1504674900247-0877df9cc836
1505142468610-359e7d316be0
1506905925346-21bda4d32df4
1509440159596-0249088772ff
1516321318423-f06f85e504b3
1516541196182-6bdb0516ed27
1517245386807-bb43f82c33c4
1518770660439-4636190af475
1518837695005-2083093ee35b
1519681393784-d120267933ba
1521737711867-e3b97375f902
1522202176988-66273c2fd55f
1530026405186-ed1f139313f8
1532187863486-abf9dbad1b69
1542601906990-b4d3fb778b09
1542838132-92c53300491e
1544145945-f90425340c7e
1546069901-ba9599a7e63c
1548839140-29a749e1cf4d
1551288049-bebda4e38f71
1552664730-d307ca884978
1553413077-190dd305871c
1554224155-6726b3ff858f
1555507036-ab1f4038808a
1556228578-8c89e6adf883
1556228720-195a672e8a03
1556761175-5973dc0f32e7
1556910103-1c02745aae4d
1557804506-669a67965ba0
1559757148-5c350d0d3c56
1565958011703-44f9829ba187
1566576912321-d58ddd7a6088
1571019613454-1cb2f99b2d8b
1571781926291-c477ebfd024b
1573496359142-b8d87734a5a2
1576086213369-97a306d36557
1576091160399-112ba8d25d1d
1579154204601-01588f351e67
1581091226825-a6a2a5aee158
1581093588401-fbb62a02f120
1581094271901-8022df4466f9
1582719471384-894fbb16e074
1582719478250-c89cae4dc85b
1586281380349-632531db7ed4
1586528116493-a029325540fa
1590283603385-17ffb3a7f29f
1596755389378-c31d21fd1273
1600880292203-757bb62b4baf
1607619056574-7b8d3ee536b2
1611974789855-9c2a0a7236a3
1612817288484-6f916006741a
1625246333195-78d9c38ad449
""".split()
)

# slug -> (hero_id, inline_id) — all must be in OK; each id used at most once
# Topic-matched to article titles
ASSIGN: dict[str, tuple[str, str]] = {
    # Checklist / báo giá / nhận mẫu / lab accreditation
    "gui-mau-kiem-nghiem-can-chuan-bi-gi": (
        "1586281380349-632531db7ed4",  # clipboard checklist
        "1586528116493-a029325540fa",  # shipping package
    ),
    "bao-gia-kiem-nghiem-gom-nhung-gi": (
        "1554224155-6726b3ff858f",  # paperwork / cost
        "1454165804606-c3d57bc86b40",  # business docs
    ),
    "checklist-ho-so-dtm": (
        "1450101499163-c8848c66ca85",  # documents
        "1434030216411-0b793f4b4173",  # writing notes
    ),
    "nhan-mau-ha-noi-can-tho-hcm": (
        "1566576912321-d58ddd7a6088",  # logistics truck
        "1553413077-190dd305871c",  # warehouse
    ),
    "chon-phong-lab-iso-17025-nlct": (
        "1576086213369-97a306d36557",  # scientist lab
        "1582719478250-c89cae4dc85b",  # lab vials
    ),
    "valas-217-iso-17025-la-gi": (
        "1532187863486-abf9dbad1b69",  # microscope
        "1581094271901-8022df4466f9",  # pipette
    ),
    "tu-cong-bo-san-pham-va-phieu-kiem-nghiem": (
        "1552664730-d307ca884978",  # meeting
        "1600880292203-757bb62b4baf",  # collab / paperwork
    ),
    # Bao bì / chai nhựa / PFAS / vi nhựa
    "chai-nhua-dung-nuoc-uong-thoi-nhiem": (
        "1548839140-29a749e1cf4d",  # bottled water
        "1544145945-f90425340c7e",  # plastic bottles
    ),
    "cong-bo-hop-nhua-dung-thuc-pham": (
        "1542838132-92c53300491e",  # grocery packaged
        "1504674900247-0877df9cc836",  # food plated / container context
    ),
    "vi-sao-kiem-nghiem-bao-bi-tiep-xuc-thuc-pham": (
        "1546069901-ba9599a7e63c",  # food bowl / FCM contact
        "1498837167922-ddd27525d352",  # produce packaging context
    ),
    "eu-10-2011-bao-bi-xuat-khau": (
        "1497366216548-37526070297c",  # modern office / export ops
        "1522202176988-66273c2fd55f",  # team / trade
    ),
    "qcvn-vs-fda-gb4806-bao-bi": (
        "1521737711867-e3b97375f902",  # office compare standards
        "1573496359142-b8d87734a5a2",  # professional docs
    ),
    "pfas-trong-thuc-pham-bao-bi": (
        "1571019613454-1cb2f99b2d8b",  # water bottle
        "1505142468610-359e7d316be0",  # water surface
    ),
    "vi-nhua-trong-thuc-pham": (
        "1518837695005-2083093ee35b",  # ocean
        "1475924156734-496f6cac6ec1",  # beach
    ),
    # Bánh / trung thu / shelf-life
    "checklist-gui-mau-banh-trung-thu-2026": (
        "1509440159596-0249088772ff",  # bread bakery
        "1555507036-ab1f4038808a",  # bakery
    ),
    "chi-tieu-kiem-nghiem-banh-trung-thu": (
        "1565958011703-44f9829ba187",  # dessert pastry
        "1556910103-1c02745aae4d",  # kitchen cooking
    ),
    "kiem-nghiem-banh-keo-mat-ong-dau-an": (
        "1546069901-ba9599a7e63c",  # WILL CONFLICT - fixed below
        "1504674900247-0877df9cc836",
    ),
    "challenge-test-va-han-su-dung": (
        "1556910103-1c02745aae4d",
        "1498837167922-ddd27525d352",
    ),
    # Nước
    "kiem-nghiem-nuoc-uong-qcvn": (
        "1432405972618-c60b0225b8f9",  # waterfall / clean water
        "1506905925346-21bda4d32df4",  # mountain lake
    ),
    # Mỹ phẩm / dược / TPCN
    "kiem-nghiem-my-pham-thong-tu-06": (
        "1556228578-8c89e6adf883",  # cosmetics
        "1596755389378-c31d21fd1273",  # skincare
    ),
    "kiem-nghiem-duoc-pham-va-gmp": (
        "1576091160399-112ba8d25d1d",  # healthcare/pharma vibe
        "1607619056574-7b8d3ee536b2",  # vitamins
    ),
    "kiem-nghiem-tpcn-truoc-cong-bo": (
        "1612817288484-6f916006741a",  # beauty/supplement jars
        "1556228720-195a672e8a03",  # cream jar
    ),
    "cronobacter-sua-bot": (
        "1516541196182-6bdb0516ed27",  # clinical / infant safety
        "1571781926291-c477ebfd024b",  # product bottles
    ),
    # Vi sinh / kim loại / TP / thủy sản
    "kiem-nghiem-vi-sinh-thuc-pham": (
        "1582719471384-894fbb16e074",  # lab bottles
        "1530026405186-ed1f139313f8",  # chemistry
    ),
    "kim-loai-nang-trong-thuc-pham": (
        "1581093588401-fbb62a02f120",  # researcher
        "1579154204601-01588f351e67",  # research
    ),
    "kiem-nghiem-thuc-pham-ha-noi": (
        "1542838132-92c53300491e",  # grocery market HN food
        "1556910103-1c02745aae4d",  # cooking - conflict fix below
    ),
    "kiem-nghiem-thuy-san-xuat-khau": (
        "1504674900247-0877df9cc836",  # plated food / seafood plate common
        "1497366754035-f200968a6e72",  # office export ops
    ),
    "du-luong-khang-sinh-thuy-san": (
        "1559757148-5c350d0d3c56",  # science / residue testing
        "1581091226825-a6a2a5aee158",  # tech analysis
    ),
    "du-luong-thuoc-bvtv-rau-cu": (
        "1498837167922-ddd27525d352",  # vegetables
        "1416879595882-3373a0480b5b",  # plants
    ),
    "doc-to-vi-nam-aflatoxin": (
        "1500382017468-9049fed747ef",  # farm grains
        "1464226184884-fa280b87c399",  # farm field
    ),
    # Dinh dưỡng
    "ghi-nhan-dinh-duong-thong-tu-29-2023": (
        "1551288049-bebda4e38f71",  # dashboard data
        "1460925895917-afdab827c52f",  # analytics
    ),
    "phan-tich-dinh-duong-ghi-nhan": (
        "1611974789855-9c2a0a7236a3",  # charts
        "1590283603385-17ffb3a7f29f",  # finance-ish / metrics
    ),
    # Chứng nhận
    "haccp-va-iso-22000-khac-nhau": (
        "1517245386807-bb43f82c33c4",  # cafe / food service kitchen vibe
        "1556761175-5973dc0f32e7",  # business people / systems
    ),
    "chung-nhan-vietgap-quy-trinh": (
        "1625246333195-78d9c38ad449",  # farm
        "1542601906990-b4d3fb778b09",  # leaf
    ),
    "vietgap-organic-halal-overview": (
        "1472214103451-9374bd1c798e",  # nature landscape
        "1447752875215-b2761acb3c5d",  # forest path
    ),
    "smeta-sedex-nha-may-thuc-pham": (
        "1516321318423-f06f85e504b3",  # factory/people ops
        "1557804506-669a67965ba0",  # professional workplace
    ),
    "ocop-kiem-nghiem-va-cong-bo": (
        "1426604966848-d7adac402bff",  # nature local origin
        "1469474968028-56623f02e42e",  # scenic
    ),
    # Môi trường
    "dang-ky-moi-truong-vs-quan-trac": (
        "1470071459604-3b5ec3a7fe05",  # fog nature
        "1441974231531-c6227db76b6e",  # forest
    ),
    "quan-trac-khi-thai-nha-may": (
        "1500534314209-a25ddb2bd429",  # mountains / air
        "1519681393784-d120267933ba",  # night mountain air
    ),
    "quan-trac-nuoc-thai-dinh-ky": (
        "1501594907352-04cda38ebc29",  # ocean cliff water
        "1432405972618-c60b0225b8f9",  # waterfall - conflict with nuoc
    ),
}


def download(photo_id: str, w=960, h=540) -> Image.Image:
    url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w={w}&h={h}&q=80"
    req = urllib.request.Request(url, headers={"User-Agent": "ApoliqSiteBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return Image.open(BytesIO(r.read())).convert("RGB")


def download_crop_variant(photo_id: str, side: str) -> Image.Image:
    """Wide fetch then crop left/right to create a unique but related image."""
    img = download(photo_id, w=1600, h=540)
    w, h = img.size
    half = 960
    if side == "left":
        box = (0, 0, half, h)
    else:
        box = (w - half, 0, w, h)
    return img.crop(box).resize((960, 540), Image.Resampling.LANCZOS)


def tweak(img: Image.Image, key: str) -> Image.Image:
    px = img.load()
    w, h = img.size
    for i in range(14):
        x = (hash(key) + i * 37) % w
        y = (hash(key[::-1]) + i * 19) % h
        r, g, b = px[x, y]
        px[x, y] = (r, g, min(255, b ^ (i + 3)))
    return img


def bump_cache() -> None:
    for p in ROOT.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        t2 = re.sub(
            r"(images/tin-tuc/[^\"\s?]+\.jpg)(?:\?v=\d+)?",
            rf"\1?v={CACHE_V}",
            t,
        )
        if t2 != t:
            p.write_text(t2, encoding="utf-8")


def resolve_conflicts(assign: dict[str, tuple[str, str]]) -> dict[str, tuple[str, str | None]]:
    """Ensure unique IDs; mark duplicates as needing crop variant (None placeholder)."""
    used: set[str] = set()
    out: dict[str, tuple[str, str | None]] = {}
    # spare OK ids not in any assignment
    claimed = {x for pair in assign.values() for x in pair}
    spare = [i for i in sorted(OK) if i not in claimed]

    for slug, (h, inl) in sorted(assign.items()):
        nh, ni = h, inl
        if nh in used or nh not in OK:
            nh = spare.pop(0) if spare else h
        used.add(nh)
        if ni in used or ni not in OK:
            # Prefer another spare; else crop variant of thematic hero
            if spare:
                ni = spare.pop(0)
            else:
                ni = None  # signal crop variant from hero
        if ni is not None:
            used.add(ni)
        out[slug] = (nh, ni)
    return out


def main() -> None:
    # Fix known conflicts in base map with unique OK ids
    fixes = {
        "kiem-nghiem-banh-keo-mat-ong-dau-an": (
            "1546069901-ba9599a7e63c",  # healthy food bowl
            "1441986300917-64674bd600d8",  # office/coffee bakery adjacent
        ),
        "challenge-test-va-han-su-dung": (
            "1556910103-1c02745aae4d",  # kitchen
            "1485827404703-89b55fcc595e",  # tech / testing vibe
        ),
        "kiem-nghiem-thuc-pham-ha-noi": (
            "1542838132-92c53300491e",  # grocery
            "1518770660439-4636190af475",  # tech city / HN vibe
        ),
        "kiem-nghiem-thuy-san-xuat-khau": (
            "1504674900247-0877df9cc836",  # food plate
            "1497366754035-f200968a6e72",  # modern workplace export
        ),
        "cong-bo-hop-nhua-dung-thuc-pham": (
            "1544145945-f90425340c7e",  # bottles packaging - wait chai uses this
            "1517245386807-bb43f82c33c4",
        ),
        "vi-sao-kiem-nghiem-bao-bi-tiep-xuc-thuc-pham": (
            "1498837167922-ddd27525d352",
            "1555507036-ab1f4038808a",  # may conflict bakery - resolve_conflicts handles
        ),
        "quan-trac-nuoc-thai-dinh-ky": (
            "1501594907352-04cda38ebc29",
            "1505142468610-359e7d316be0",  # may conflict pfas
        ),
        "haccp-va-iso-22000-khac-nhau": (
            "1517245386807-bb43f82c33c4",
            "1556761175-5973dc0f32e7",
        ),
    }
    assign = dict(ASSIGN)
    assign.update(fixes)

    # Free chai-nhua inline from cong-bo conflict
    assign["chai-nhua-dung-nuoc-uong-thoi-nhiem"] = (
        "1548839140-29a749e1cf4d",
        "1571019613454-1cb2f99b2d8b",
    )
    assign["pfas-trong-thuc-pham-bao-bi"] = (
        "1505142468610-359e7d316be0",
        "1432405972618-c60b0225b8f9",
    )
    assign["kiem-nghiem-nuoc-uong-qcvn"] = (
        "1506905925346-21bda4d32df4",
        "1518837695005-2083093ee35b",
    )
    assign["quan-trac-nuoc-thai-dinh-ky"] = (
        "1501594907352-04cda38ebc29",
        "1475924156734-496f6cac6ec1",
    )
    assign["cong-bo-hop-nhua-dung-thuc-pham"] = (
        "1544145945-f90425340c7e",
        "1517245386807-bb43f82c33c4",
    )
    assign["vi-sao-kiem-nghiem-bao-bi-tiep-xuc-thuc-pham"] = (
        "1498837167922-ddd27525d352",
        "1546069901-ba9599a7e63c",
    )
    assign["kiem-nghiem-banh-keo-mat-ong-dau-an"] = (
        "1504674900247-0877df9cc836",
        "1441986300917-64674bd600d8",
    )
    assign["checklist-gui-mau-banh-trung-thu-2026"] = (
        "1509440159596-0249088772ff",
        "1555507036-ab1f4038808a",
    )
    assign["chi-tieu-kiem-nghiem-banh-trung-thu"] = (
        "1565958011703-44f9829ba187",
        "1556910103-1c02745aae4d",
    )
    assign["haccp-va-iso-22000-khac-nhau"] = (
        "1522202176988-66273c2fd55f",
        "1556761175-5973dc0f32e7",
    )

    articles = sorted(
        p.stem for p in (ROOT / "tin-tuc").glob("*.html") if p.name != "index.html"
    )
    missing = [s for s in articles if s not in assign]
    if missing:
        raise SystemExit(f"Missing: {missing}")

    resolved = resolve_conflicts(assign)

    # Verify uniqueness of concrete ids
    seen: list[str] = []
    for slug, (h, i) in resolved.items():
        seen.append(h)
        if i:
            seen.append(i)
    dup = [x for x in seen if seen.count(x) > 1]
    if dup:
        raise SystemExit(f"Duplicate ids remain: {set(dup)}")

    used_hashes: dict[str, str] = {}
    for slug in articles:
        hero_id, inline_id = resolved[slug]
        for role, pid in (("hero", hero_id), ("inline", inline_id)):
            if pid is None:
                # crop variant from hero of same article
                base = resolved[slug][0]
                img = download_crop_variant(base, "right" if role == "inline" else "left")
                label = f"{base}-crop-{role}"
            else:
                img = download(pid)
                label = pid
            img = tweak(img, f"{slug}-{role}-{label}")
            out = OUT / f"{slug}-{role}.jpg"
            img.save(out, "JPEG", quality=85, optimize=True)
            digest = hashlib.md5(out.read_bytes()).hexdigest()
            if digest in used_hashes:
                raise SystemExit(f"hash collision {out} == {used_hashes[digest]}")
            used_hashes[digest] = out.name
            print(f"OK {out.name} <- {label}")
            time.sleep(0.08)

    bump_cache()
    print("unique", len(used_hashes), "cache", CACHE_V)


if __name__ == "__main__":
    main()
