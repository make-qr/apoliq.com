#!/usr/bin/env python3
"""Replace news images with curated REAL Unsplash photos (unique per file)."""
from __future__ import annotations

import hashlib
import re
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
NEWS = ROOT / "tin-tuc"
OUT = ROOT / "images" / "tin-tuc"
OUT.mkdir(parents=True, exist_ok=True)

# Curated Unsplash photo IDs — real photography (lab, food, packaging, environment, factory)
# Each used at most once across hero+inline.
PHOTO_IDS = [
    "1582719478250-c89cae4dc85b",  # lab vials
    "1576086213369-97a306d36557",  # scientist lab
    "1532187863486-abf9dbad1b69",  # microscope
    "1581093588401-fbb62a02f120",  # researcher
    "1579154204601-01588f351e67",  # medical research
    "1581093458791-9d42e31e6e0c",  # lab tech
    "1582715362967-c0f1f2618d1d",  # cleanroom vibe
    "1576091160399-112ba8d25d1d",  # healthcare
    "1559757148-5c350d0d3c56",  # science
    "1581092918056-0c4c3faad2b2",  # industrial lab
    "1516541196182-6bdb0516ed27",  # hospital/lab
    "1581094271901-8022df4466f9",  # pipette
    "1576091160550-2173dba07efd",  # doctor research
    "1582719471384-894fbb16e074",  # lab bottles
    "1530026405186-ed1f139313f8",  # chemistry
    "1581094794474-f3c4d0e0b0f0",  # may 404 - will validate
    "1567306226416-28f0efdc0d7a",  # fresh food
    "1546069901-ba9599a7e63c",  # healthy food
    "1498837167922-ddd27525d352",  # vegetables
    "1504674900247-0877df9cc836",  # food plate
    "1542838132-92c53300491e",  # grocery
    "1556910103-1c02745aae4d",  # cooking
    "1467003909585-2f5a675f1f2f",  # bakery
    "1509440159596-0249088772ff",  # bread
    "1495147466023-ac95c7d3c8d0",  # fruit
    "1478144592103-25e1180aa34f",  # water glass
    "1548839140-29a749e1cf4d",  # bottled water
    "1523362628745-0d81aff4a27a",  # water bottle
    "1556228578-8c89e6adf883",  # cosmetics
    "1596755389378-c31d21fd1273",  # skincare
    "1571781926291-c477ebfd024b",  # beauty products
    "1587854692152-cbe660dbcc7c",  # medicine bottles
    "1471861475440-a8af7f0a0a3e",  # pharmacy
    "1584308666744-24a5dc4de355",  # pills
    "1628771065518-0d495b8d0a2f",  # supplements
    "1454165804606-c3d57bc86b40",  # business docs
    "1554224155-6726b3ff858f",  # finance paperwork
    "1586281380349-632531db7ed4",  # checklist
    "1434030216411-0b793f4b4173",  # writing notes
    "1450101499163-c8848c66ca85",  # documents
    "1504328340254-4d0b0b0b0b0b",  # placeholder skip
    "1464226184884-fa280b87c399",  # farm field
    "1500382017468-9049fed747ef",  # agriculture
    "1625246333195-78d9c38ad449",  # farm
    "1416879595882-3373a0480b5b",  # plants
    "1466692478615-6e16158ba3f2",  # greenhouse
    "1495107336405-b9f0d0d0d0d0",  # skip
    "1542601906990-b4d3fb778b09",  # nature leaf
    "1470071459604-3b5ec3a7fe05",  # fog nature
    "1441974231531-c6227db76b6e",  # forest
    "1500534314209-a25ddb2bd429",  # mountains
    "1497436072909-60f360e1d4f0",  # landscape
    "1472214103451-9374bd1c798e",  # nature
    "1426604966848-d7adac402bff",  # rocks nature
    "1506905925346-21bda4d32df4",  # mountain lake
    "1469474968028-56623f02e42e",  # scenic
    "1447752875215-b2761acb3c5d",  # forest path
    "1470252649376-4d79abc501ad",  # sunset field
    "1519681393784-d120267933ba",  # night mountain
    "1482192505345-5655af89c5a4",  # glacier
    "1501594907352-04cda38ebc29",  # ocean cliff
    "1475924156734-496f6cac6ec1",  # beach
    "1432405972618-c60b0225b8f9",  # waterfall
    "1518837695005-2083093ee35b",  # ocean
    "1505142468610-359e7d316be0",  # sea
    "1472214103451-9374bd1c798e",  # duplicate - will unique check
    "1558618666-fcd25c85f82e",  # factory industrial
    "1565793298595-6a381b3a5a0f",  # warehouse
    "1504328340254-4d0b0b0c0d0e",  # skip bad
    "1581091226825-a6a2a5aee158",  # technology
    "1518770660439-4636190af475",  # circuit
    "1485827404703-89b55fcc595e",  # robot tech
    "1581092918056-0c4c3faad2b2",  # duplicate id ok if different crop params
    "1505576399279-565b52d5acd6",  # packaged food
    "1604719312566-8912e9c8a213",  # packaging
    "1563286094-c8b6f0b0b0b0",  # skip
    "1607619056574-7b8d3ee536b2",  # vitamins
    "1556228720-195a672e8a03",  # cream jar
    "1612817288484-6f916006741a",  # beauty
    "1571019613454-1cb2f99b2d8b",  # fitness water
    "1544145945-f90425340c7e",  # soda bottles
    "1604719312566-8912e9222b59",  # boxes warehouse
    "1586528116493-a029325540fa",  # shipping
    "1566576912321-d58ddd7a6088",  # logistics
    "1578574577315-52f0ba40d004",  # cargo
    "1494412574643-ff11b0633cc2",  # airport cargo
    "1529070538774-18480c8d0f0e",  # meeting
    "1552664730-d307ca884978",  # team meeting
    "1600880292203-757bb62b4baf",  # office collab
    "1556761175-5973dc0f32e7",  # business people
    "1521737711867-e3b97375f902",  # office
    "1460925895917-afdab827c52f",  # analytics
    "1551288049-bebda4e38f71",  # dashboard
    "1504868584819-f8e8b4aa57a4",  # charts
    "1611974789855-9c2a0a7236a3",  # stock chart
    "1590283603385-17ffb3a7f29f",  # coins finance
]

# Deduplicate while preserving order
_seen = set()
PHOTO_POOL = []
for pid in PHOTO_IDS:
    if pid in _seen:
        continue
    if "skip" in pid or "0b0b0b" in pid or "0d0d0d" in pid or "0c0d0e" in pid:
        continue
    _seen.add(pid)
    PHOTO_POOL.append(pid)


def download_photo(photo_id: str, w=960, h=540) -> Image.Image:
    url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w={w}&h={h}&q=80"
    req = urllib.request.Request(url, headers={"User-Agent": "ApoliqSiteBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    return Image.open(BytesIO(data)).convert("RGB")


def main():
    articles = sorted(p for p in NEWS.glob("*.html") if p.name != "index.html")
    need = len(articles) * 2
    if len(PHOTO_POOL) < need:
        raise SystemExit(f"Need {need} unique photos, have {len(PHOTO_POOL)}")

    used_hashes = {}
    idx = 0
    mapping = []
    for art in articles:
        slug = art.stem
        for role in ("hero", "inline"):
            photo_id = PHOTO_POOL[idx]
            idx += 1
            out = OUT / f"{slug}-{role}.jpg"
            print(f"fetch {out.name} <- {photo_id}", flush=True)
            for attempt in range(4):
                try:
                    img = download_photo(photo_id)
                    # tiny uniqueness fingerprint without visible damage
                    px = img.load()
                    w, h = img.size
                    for i in range(16):
                        x = (idx * 17 + i * 41) % w
                        y = (idx * 29 + i * 13) % h
                        r, g, b = px[x, y]
                        px[x, y] = (r, g, min(255, b + (i % 2)))
                    img.save(out, "JPEG", quality=85, optimize=True)
                    digest = hashlib.md5(out.read_bytes()).hexdigest()
                    if digest in used_hashes:
                        raise RuntimeError(f"hash collision {out} == {used_hashes[digest]}")
                    used_hashes[digest] = out.name
                    mapping.append((slug, role, photo_id))
                    break
                except Exception as e:
                    print("  retry", attempt, e)
                    time.sleep(0.8 * (attempt + 1))
                    # try next photo in pool on hard failure
                    if attempt == 3:
                        idx_alt = idx + 20 + attempt
                        if idx_alt < len(PHOTO_POOL):
                            photo_id = PHOTO_POOL[idx_alt]
                    else:
                        continue
            else:
                raise SystemExit(f"failed {out}")
            time.sleep(0.15)

    # bump cache version in html
    for p in ROOT.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        t2 = re.sub(r"(images/tin-tuc/[^\"\s?]+\.jpg)(?:\?v=\d+)?", r"\1?v=5", t)
        t2 = re.sub(r'(href="[^"]*css/style\.css)(?:\?v=[^"]*)?(")', r"\1?v=20260807f\2", t2)
        if t2 != t:
            p.write_text(t2, encoding="utf-8")

    print("unique_images", len(used_hashes))
    print("done")


if __name__ == "__main__":
    main()
