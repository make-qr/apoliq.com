#!/usr/bin/env python3
"""Generate Apoliq static pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SERVICES = {
    "kiem-nghiem": [
        {
            "slug": "thuc-pham",
            "title": "Kiểm nghiệm Thực phẩm",
            "lead": "Đánh giá chất lượng và an toàn thực phẩm chế biến, nguyên liệu, bán thành phẩm theo TCCS/QCVN/TCVN.",
            "bullets": [
                "Vi sinh, hóa lý, phụ gia, kim loại nặng theo mục đích công bố hoặc QC định kỳ.",
                "Tư vấn gói chỉ tiêu vừa đủ — tránh kiểm thừa.",
                "Hỗ trợ hồ sơ công bố sản phẩm sau khi có kết quả.",
            ],
            "pain": [
                ("Cần công bố sản phẩm mới", "Chọn đúng chỉ tiêu bắt buộc theo quy định ATTP."),
                ("Đối tác yêu cầu chứng từ", "Báo cáo rõ ràng để chào hàng siêu thị, sàn TMĐT."),
                ("Kiểm soát chất lượng định kỳ", "Phát hiện sớm lệch chỉ tiêu theo lô sản xuất."),
                ("Chưa rõ gói chỉ tiêu", "Tư vấn theo TCCS — tối ưu chi phí từng đợt."),
            ],
        },
        {
            "slug": "banh-keo",
            "title": "Kiểm nghiệm Bánh kẹo",
            "lead": "Gói kiểm nghiệm bánh kẹo và bánh theo mùa vụ — vi sinh, phụ gia, cảm quan theo TCCS.",
            "bullets": [
                "Phù hợp công bố sản phẩm và kiểm lô trước xuất hàng.",
                "Tư vấn gói mùa cao điểm để rút ngắn thời gian xử lý.",
                "Có thể kết hợp phân tích dinh dưỡng / ghi nhãn khi cần.",
            ],
            "pain": [
                ("Mùa cao điểm gấp", "Báo giá nhanh, lịch trả kết quả rõ ràng."),
                ("Công bố TCCS", "Chọn chỉ tiêu khớp hồ sơ nộp cơ quan quản lý."),
                ("Đối soát đại lý", "Phiếu kết quả dùng được cho đối tác phân phối."),
                ("Combo quà tặng", "Tư vấn thêm nước uống / TPCN nếu mở rộng dòng hàng."),
            ],
        },
        {
            "slug": "nuoc-uong",
            "title": "Kiểm nghiệm Nước sạch & nước uống",
            "lead": "Kiểm nghiệm nước đóng chai, nước đầu vào sản xuất theo QCVN liên quan.",
            "bullets": [
                "Vi sinh và hóa lý theo mục đích công bố hoặc QC.",
                "Phù hợp nhà máy đồ uống, xưởng thực phẩm dùng nước đầu vào.",
                "Tư vấn chỉ tiêu theo loại nước và kênh phân phối.",
            ],
            "pain": [
                ("Công bố nước đóng chai", "Gói chỉ tiêu theo QCVN áp dụng."),
                ("Nước đầu vào SX", "Giảm rủi ro nhiễm từ nguồn nước."),
                ("Kiểm định kỳ", "Lịch lấy mẫu và trả kết quả ổn định."),
                ("Chưa rõ tiêu chuẩn", "Tư vấn trước khi nhận mẫu."),
            ],
        },
        {
            "slug": "duoc-pham",
            "title": "Kiểm nghiệm Dược phẩm / TPCN",
            "lead": "Phân tích hóa lý, vi sinh, độ ẩm và các chỉ tiêu theo yêu cầu hồ sơ TPCN / dược phẩm.",
            "bullets": [
                "Hỗ trợ đối soát chất lượng nguyên liệu và thành phẩm.",
                "Tư vấn chỉ tiêu theo mục đích đăng ký / QC nội bộ.",
                "Phối hợp với dịch vụ dinh dưỡng khi cần ghi nhãn.",
            ],
            "pain": [
                ("Hồ sơ TPCN", "Chỉ tiêu phù hợp yêu cầu nộp hồ sơ."),
                ("QC nguyên liệu", "Phát hiện lệch chất lượng sớm."),
                ("Đối tác xuất khẩu", "Báo cáo rõ ràng, dễ đối chiếu."),
                ("Gói tùy chỉnh", "Chỉ kiểm đúng nhu cầu thực tế."),
            ],
        },
        {
            "slug": "my-pham",
            "title": "Kiểm nghiệm Mỹ phẩm",
            "lead": "Kiểm nghiệm mỹ phẩm theo các chỉ tiêu phổ biến: vi sinh, pH, kim loại nặng, ổn định cơ bản.",
            "bullets": [
                "Phù hợp công bố / tự công bố mỹ phẩm và QC định kỳ.",
                "Tư vấn checklist chỉ tiêu theo loại sản phẩm.",
                "Hỗ trợ doanh nghiệp mới bắt đầu dòng mỹ phẩm.",
            ],
            "pain": [
                ("Công bố mỹ phẩm", "Chọn chỉ tiêu đúng nhóm sản phẩm."),
                ("QC từng lô", "Giữ ổn định chất lượng trước xuất hàng."),
                ("Kim loại nặng / VS", "Đối soát rủi ro an toàn."),
                ("Chưa có checklist", "Apoliq tư vấn trước khi nhận mẫu."),
            ],
        },
        {
            "slug": "thuc-an-chan-nuoi",
            "title": "Kiểm nghiệm Thức ăn chăn nuôi",
            "lead": "Kiểm protein, aflatoxin, vi sinh và các chỉ tiêu liên quan thức ăn chăn nuôi.",
            "bullets": [
                "Phù hợp nhà máy TACN và cơ sở chăn nuôi cần đối soát đầu vào.",
                "Tư vấn gói theo loại thức ăn và mục đích sử dụng.",
                "Kết nối với dịch vụ môi trường khi cần quan trắc kèm theo.",
            ],
            "pain": [
                ("Đối soát nguyên liệu", "Giảm rủi ro aflatoxin / VS."),
                ("QC thành phẩm", "Đảm bảo chỉ tiêu dinh dưỡng."),
                ("Yêu cầu đối tác", "Phiếu kết quả rõ ràng."),
                ("Gói tối ưu", "Không kiểm thừa chỉ tiêu."),
            ],
        },
        {
            "slug": "dinh-duong",
            "title": "Phân tích dinh dưỡng / ghi nhãn",
            "lead": "Đối soát protein, năng lượng, vitamin và thông tin dinh dưỡng trên nhãn mác.",
            "bullets": [
                "Hỗ trợ chỉnh nhãn trước khi in bao bì hàng loạt.",
                "Phối hợp với kiểm nghiệm thực phẩm / bánh kẹo.",
                "Giảm rủi ro nhãn sai so với thành phần thực tế.",
            ],
            "pain": [
                ("In nhãn mới", "Đối soát số liệu trước khi lên khuôn."),
                ("Sàn TMĐT / siêu thị", "Thông tin dinh dưỡng khớp hồ sơ."),
                ("Đổi công thức", "Cập nhật lại bảng dinh dưỡng."),
                ("Hồ sơ công bố", "Bổ sung chỉ tiêu dinh dưỡng khi cần."),
            ],
        },
        {
            "slug": "khac",
            "title": "Dịch vụ kiểm nghiệm khác",
            "lead": "Mẫu R&D, bao bì tiếp xúc thực phẩm và các yêu cầu kiểm nghiệm theo chỉ tiêu riêng.",
            "bullets": [
                "Tư vấn khả năng thử nghiệm trước khi nhận mẫu.",
                "Phù hợp doanh nghiệp có nhu cầu không thuộc danh mục chuẩn.",
                "Định hướng phương án thay thế nếu chỉ tiêu ngoài phạm vi.",
            ],
            "pain": [
                ("Mẫu R&D", "Đánh giá sớm trước khi scale sản xuất."),
                ("Bao bì FCM", "Đối soát an toàn tiếp xúc thực phẩm."),
                ("Chỉ tiêu đặc thù", "Tư vấn trước, tránh gửi mẫu sai."),
                ("Nhiều loại mẫu", "Một đầu mối liên hệ báo giá."),
            ],
        },
    ],
    "chung-nhan": [
        {
            "slug": "haccp",
            "title": "Chứng nhận HACCP",
            "lead": "Tư vấn xây dựng và hoàn thiện hệ thống HACCP cho xưởng thực phẩm, đồ uống.",
            "bullets": [
                "Rà soát quy trình, điểm kiểm soát tới hạn (CCP).",
                "Hỗ trợ hồ sơ và chuẩn bị đánh giá.",
                "Có thể kết hợp kiểm nghiệm định kỳ tại cùng chuỗi dịch vụ.",
            ],
            "pain": [
                ("Vào chuỗi phân phối", "HACCP thường là yêu cầu tối thiểu."),
                ("Xưởng mới", "Xây hệ thống từ đầu đúng chuẩn."),
                ("Đánh giá lại", "Khắc phục điểm không phù hợp."),
                ("Song song kiểm nghiệm", "Khớp giấy tờ với thực tế lô hàng."),
            ],
        },
        {
            "slug": "iso-22000",
            "title": "Chứng nhận ISO 22000",
            "lead": "Tư vấn hệ thống quản lý an toàn thực phẩm theo ISO 22000.",
            "bullets": [
                "Phù hợp doanh nghiệp cần hệ thống ATTP toàn diện hơn HACCP.",
                "Hỗ trợ tài liệu hóa, đào tạo nội bộ cơ bản và chuẩn bị audit.",
                "Định hướng kết hợp kiểm nghiệm định kỳ.",
            ],
            "pain": [
                ("Xuất khẩu / chuỗi lớn", "ISO 22000 tăng độ tin cậy."),
                ("Nâng cấp từ HACCP", "Mở rộng hệ thống quản lý."),
                ("Audit lần đầu", "Chuẩn bị hồ sơ và thực hành."),
                ("Duy trì hệ thống", "Kế hoạch kiểm soát sau chứng nhận."),
            ],
        },
        {
            "slug": "vietgap",
            "title": "Chứng nhận VietGAP",
            "lead": "Tư vấn chứng nhận VietGAP cho sản xuất nông nghiệp.",
            "bullets": [
                "Hướng dẫn hồ sơ, nhật ký sản xuất và thực hành đồng ruộng / cơ sở.",
                "Phối hợp kiểm nghiệm khi đối tác yêu cầu phiếu kèm theo.",
                "Phù hợp HTX, trang trại, cơ sở vùng ĐBSCL và toàn quốc.",
            ],
            "pain": [
                ("Hồ sơ VietGAP", "Tránh thiếu nhật ký / bằng chứng."),
                ("OCOP / siêu thị", "Chứng nhận hỗ trợ đầu ra."),
                ("Nhầm với chỉ kiểm nghiệm", "Hai việc bổ sung cho nhau."),
                ("Bao bì sau chứng nhận", "Cập nhật thông tin đúng quy định."),
            ],
        },
        {
            "slug": "organic",
            "title": "Chứng nhận Organic",
            "lead": "Tư vấn hướng tới chứng nhận hữu cơ theo yêu cầu thị trường mục tiêu.",
            "bullets": [
                "Rà soát chuỗi sản xuất, nguyên liệu và truy xuất nguồn gốc.",
                "Định hướng tiêu chuẩn phù hợp thị trường nội địa / xuất khẩu.",
                "Kết hợp kiểm nghiệm khi cần chứng minh chỉ tiêu.",
            ],
            "pain": [
                ("Thị trường hữu cơ", "Yêu cầu chứng nhận riêng, không chỉ VietGAP."),
                ("Chuỗi cung ứng", "Kiểm soát nguyên liệu đầu vào."),
                ("Nhãn Organic", "Ghi nhận đúng phạm vi được chứng nhận."),
                ("Chuẩn bị audit", "Hồ sơ và thực địa."),
            ],
        },
        {
            "slug": "halal",
            "title": "Chứng nhận Halal",
            "lead": "Tư vấn chuẩn bị hồ sơ và quy trình hướng tới chứng nhận Halal.",
            "bullets": [
                "Rà soát nguyên liệu, quy trình và truy xuất.",
                "Phù hợp doanh nghiệp nhắm thị trường Hồi giáo.",
                "Có thể kết hợp kiểm nghiệm thành phẩm khi đối tác yêu cầu.",
            ],
            "pain": [
                ("Xuất khẩu Halal", "Yêu cầu chứng nhận rõ ràng."),
                ("Nguyên liệu nhạy cảm", "Đối soát nguồn gốc."),
                ("Đổi công thức", "Đánh giá lại phạm vi."),
                ("Hồ sơ lần đầu", "Tư vấn lộ trình từng bước."),
            ],
        },
        {
            "slug": "smeta-sedex",
            "title": "Chứng nhận SMETA / SEDEX",
            "lead": "Tư vấn chuẩn bị audit đạo đức xã hội SMETA / SEDEX cho chuỗi cung ứng FMCG.",
            "bullets": [
                "Rà soát điều kiện lao động, an toàn và hồ sơ nhà máy.",
                "Hỗ trợ doanh nghiệp đáp ứng yêu cầu buyer quốc tế.",
                "Lộ trình khắc phục trước và sau audit.",
            ],
            "pain": [
                ("Buyer yêu cầu SEDEX", "Cần chuẩn bị audit SMETA."),
                ("Nhà máy lần đầu", "Checklist thực tế, không lý thuyết suông."),
                ("Điểm không phù hợp", "Kế hoạch khắc phục."),
                ("Duy trì hồ sơ", "Sẵn sàng audit định kỳ."),
            ],
        },
    ],
    "moi-truong": [
        {
            "slug": "quan-trac",
            "title": "Quan trắc môi trường",
            "lead": "Quan trắc nước thải, khí thải, đất theo quy chuẩn và yêu cầu pháp lý liên quan.",
            "bullets": [
                "Phù hợp cơ sở sản xuất cần báo cáo định kỳ.",
                "Tư vấn chỉ tiêu theo loại hình hoạt động.",
                "Kết nối tư vấn hồ sơ môi trường khi cần.",
            ],
            "pain": [
                ("Báo cáo định kỳ", "Lịch lấy mẫu và trả kết quả rõ."),
                ("Nước thải / khí thải", "Đối soát theo QCVN áp dụng."),
                ("Thanh tra / kiểm tra", "Có số liệu sẵn sàng."),
                ("Mở rộng công suất", "Đánh giá lại phạm vi quan trắc."),
            ],
        },
        {
            "slug": "tu-van",
            "title": "Tư vấn môi trường",
            "lead": "Tư vấn ĐTM, đăng ký môi trường và hồ sơ pháp lý liên quan hoạt động sản xuất.",
            "bullets": [
                "Định hướng loại hồ sơ phù hợp quy mô cơ sở.",
                "Hỗ trợ doanh nghiệp mới thành lập hoặc mở rộng.",
                "Có thể kết hợp quan trắc và đào tạo nội bộ cơ bản.",
            ],
            "pain": [
                ("Chưa rõ loại hồ sơ", "Tư vấn đúng thủ tục cần làm."),
                ("Mở nhà máy mới", "Lộ trình pháp lý môi trường."),
                ("Bổ sung công đoạn", "Cập nhật đăng ký / ĐTM."),
                ("Đào tạo nội bộ", "Nhận thức tuân thủ tại chỗ."),
            ],
        },
    ],
}

CATEGORY_META = {
    "kiem-nghiem": {
        "name": "Kiểm nghiệm",
        "blurb": "Dịch vụ kiểm nghiệm nguyên liệu, bán thành phẩm và thành phẩm — hỗ trợ công bố và kiểm soát chất lượng.",
    },
    "chung-nhan": {
        "name": "Chứng nhận",
        "blurb": "Tư vấn chứng nhận hệ thống và tiêu chuẩn nông nghiệp / ATTP / chuỗi cung ứng.",
    },
    "moi-truong": {
        "name": "Môi trường",
        "blurb": "Quan trắc và tư vấn hồ sơ môi trường cho cơ sở sản xuất.",
    },
}


def shell(title, description, depth, body, canonical=""):
    root = "../" * depth
    can = f'\n  <link rel="canonical" href="{canonical}">' if canonical else ""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">{can}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/style.css">
  <link rel="icon" href="{root}images/logo.png" type="image/png">
</head>
<body data-depth="{depth}">
  <div id="site-header"></div>
{body}
  <div id="site-footer"></div>
  <script src="{root}js/main.js"></script>
</body>
</html>
"""


def service_page(cat, item):
    meta = CATEGORY_META[cat]
    pains = "\n".join(
        f'        <div class="info-card"><h3>{t}</h3><p>{d}</p></div>' for t, d in item["pain"]
    )
    bullets = "\n".join(f"          <li>{b}</li>" for b in item["bullets"])
    related = "".join(
        f'        <a href="{s["slug"]}.html">{s["title"]}</a>\n'
        for s in SERVICES[cat]
        if s["slug"] != item["slug"]
    )
    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../../index.html">Trang chủ</a> / <a href="index.html">{meta["name"]}</a> / {item["title"]}</div>
      <h1>{item["title"]}</h1>
      <p>{item["lead"]}</p>
    </div>
  </section>
  <section class="content">
    <div class="container content-grid">
      <article class="prose">
        <h2>Phạm vi hỗ trợ</h2>
        <ul>
{bullets}
        </ul>
        <h2>Chúng tôi giúp bạn giải quyết</h2>
        <div class="card-grid">
{pains}
        </div>
        <h2>Quy trình làm việc</h2>
        <ol>
          <li>Tiếp nhận yêu cầu — mô tả sản phẩm / mục đích / số mẫu.</li>
          <li>Báo giá và thống nhất chỉ tiêu.</li>
          <li>Nhận mẫu và thực hiện phân tích / tư vấn.</li>
          <li>Trả kết quả hoặc bàn giao hồ sơ; hỗ trợ bước tiếp theo nếu cần.</li>
        </ol>
        <p><a class="btn btn-primary" href="../../lien-he/index.html">Nhận báo giá</a>
           <a class="btn btn-secondary" href="tel:+84917333965">Gọi 0917 333 965</a></p>
      </article>
      <aside class="side-card">
        <h3>Cùng nhóm dịch vụ</h3>
{related}        <a href="../../lien-he/index.html"><strong>Liên hệ báo giá</strong></a>
      </aside>
    </div>
  </section>
"""
    return shell(
        f"{item['title']} | Apoliq",
        item["lead"],
        3,
        body,
    )


def category_index(cat):
    meta = CATEGORY_META[cat]
    cards = "\n".join(
        f"""      <a class="service-tile" href="{s['slug']}.html">
        <div class="visual">{meta['name'][:2].upper()}</div>
        <div class="body">
          <h3>{s['title']}</h3>
          <p>{s['lead']}</p>
          <span class="btn btn-outline">Xem chi tiết</span>
        </div>
      </a>"""
        for s in SERVICES[cat]
    )
    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../../index.html">Trang chủ</a> / Dịch vụ / {meta["name"]}</div>
      <h1>Dịch vụ {meta["name"]}</h1>
      <p>{meta["blurb"]}</p>
    </div>
  </section>
  <section class="section">
    <div class="container service-grid">
{cards}
    </div>
  </section>
"""
    return shell(f"Dịch vụ {meta['name']} | Apoliq", meta["blurb"], 2, body)


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def main():
    # category indexes + service pages
    for cat, items in SERVICES.items():
        write(ROOT / "dich-vu" / cat / "index.html", category_index(cat))
        for item in items:
            write(ROOT / "dich-vu" / cat / f"{item['slug']}.html", service_page(cat, item))

    # gioi thieu
    write(
        ROOT / "gioi-thieu" / "index.html",
        shell(
            "Giới thiệu | Apoliq",
            "Giới thiệu Công ty Cổ phần Khoa học và Công nghệ Apoliq.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Giới thiệu</div>
      <h1>Giới thiệu chung</h1>
      <p>Apoliq Science and Technology Joint Stock Company — đồng hành cùng doanh nghiệp kiểm soát chất lượng và tuân thủ.</p>
    </div>
  </section>
  <section class="content">
    <div class="container prose">
      <p><strong>APOLIQ SCIENCE AND TECHNOLOGY JOINT STOCK COMPANY</strong> cung cấp dịch vụ kiểm nghiệm, tư vấn chứng nhận và hỗ trợ hồ sơ môi trường, giúp doanh nghiệp giảm rủi ro chất lượng và đáp ứng yêu cầu thị trường.</p>
      <h2>Định hướng</h2>
      <ul>
        <li>Ưu tiên dịch vụ thực tế doanh nghiệp đang cần: kiểm nghiệm, chứng nhận, môi trường.</li>
        <li>Quy trình rõ ràng — báo giá nhanh, phối hợp dễ theo dõi.</li>
        <li>Phục vụ doanh nghiệp tại Cần Thơ và các tỉnh thành khác.</li>
      </ul>
      <h2>Trụ sở</h2>
      <p>K2-15 Võ Nguyên Giáp, P. Hưng Phú, TP. Cần Thơ</p>
      <p>Hotline: <a href="tel:+84917333965">0917 333 965</a> · Email: <a href="mailto:info@apoliq.com">info@apoliq.com</a></p>
    </div>
  </section>
""",
        ),
    )

    write(
        ROOT / "gioi-thieu" / "chuc-nang.html",
        shell(
            "Chức năng – Nhiệm vụ | Apoliq",
            "Chức năng và nhiệm vụ của Apoliq trong kiểm nghiệm, chứng nhận và môi trường.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / <a href="index.html">Giới thiệu</a> / Chức năng</div>
      <h1>Chức năng – Nhiệm vụ</h1>
      <p>Các nhóm công việc Apoliq tập trung triển khai cho khách hàng doanh nghiệp.</p>
    </div>
  </section>
  <section class="content">
    <div class="container card-grid">
      <div class="info-card"><h3>Kiểm nghiệm</h3><p>Tiếp nhận mẫu, tư vấn chỉ tiêu, thực hiện phân tích và trả kết quả phục vụ công bố / QC.</p></div>
      <div class="info-card"><h3>Chứng nhận</h3><p>Tư vấn hệ thống HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</p></div>
      <div class="info-card"><h3>Môi trường</h3><p>Quan trắc và tư vấn hồ sơ pháp lý môi trường cho cơ sở sản xuất.</p></div>
      <div class="info-card"><h3>Đồng hành hồ sơ</h3><p>Hỗ trợ doanh nghiệp hiểu rõ yêu cầu và chuẩn bị tài liệu liên quan chất lượng.</p></div>
    </div>
  </section>
""",
        ),
    )

    write(
        ROOT / "nang-luc" / "index.html",
        shell(
            "Năng lực | Apoliq",
            "Năng lực dịch vụ kiểm nghiệm, chứng nhận và môi trường của Apoliq.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Năng lực</div>
      <h1>Năng lực dịch vụ</h1>
      <p>Tập trung vào các dịch vụ Apoliq đang triển khai — không liệt kê hạng mục ngoài phạm vi.</p>
    </div>
  </section>
  <section class="content">
    <div class="container prose">
      <h2>Nhóm năng lực đang cung cấp</h2>
      <div class="card-grid">
        <div class="info-card"><h3>Kiểm nghiệm sản phẩm</h3><p>Thực phẩm, bánh kẹo, nước uống, dược/TPCN, mỹ phẩm, TACN, dinh dưỡng và yêu cầu đặc thù.</p></div>
        <div class="info-card"><h3>Chứng nhận & tư vấn</h3><p>HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</p></div>
        <div class="info-card"><h3>Môi trường</h3><p>Quan trắc môi trường và tư vấn hồ sơ (ĐTM, đăng ký môi trường…).</p></div>
      </div>
      <h2>Cam kết vận hành</h2>
      <ul>
        <li>Báo giá rõ ràng theo chỉ tiêu / phạm vi công việc.</li>
        <li>Trao đổi tiến độ và kết quả dễ theo dõi.</li>
        <li>Tư vấn đúng nhu cầu — không đẩy dịch vụ doanh nghiệp chưa cần.</li>
      </ul>
      <p><a class="btn btn-primary" href="../lien-he/index.html">Liên hệ tư vấn năng lực phù hợp</a></p>
    </div>
  </section>
""",
        ),
    )

    write(
        ROOT / "tin-tuc" / "index.html",
        shell(
            "Tin tức | Apoliq",
            "Tin hoạt động và kiến thức kiểm nghiệm, chứng nhận từ Apoliq.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Tin tức</div>
      <h1>Tin tức</h1>
      <p>Cập nhật hoạt động và kiến thức liên quan kiểm nghiệm – chứng nhận – môi trường.</p>
    </div>
  </section>
  <section class="content">
    <div class="container">
      <ul class="news-list">
        <li>
          <div class="news-thumb">KN</div>
          <div>
            <a href="../dich-vu/kiem-nghiem/thuc-pham.html">Hướng dẫn chọn gói kiểm nghiệm thực phẩm trước khi công bố</a>
            <p class="meta">Kiến thức chuyên môn · Kiểm nghiệm</p>
          </div>
        </li>
        <li>
          <div class="news-thumb">CN</div>
          <div>
            <a href="../dich-vu/chung-nhan/haccp.html">Khi nào doanh nghiệp nên triển khai HACCP?</a>
            <p class="meta">Kiến thức chuyên môn · Chứng nhận</p>
          </div>
        </li>
        <li>
          <div class="news-thumb">MT</div>
          <div>
            <a href="../dich-vu/moi-truong/quan-trac.html">Quan trắc môi trường định kỳ: những việc cần chuẩn bị</a>
            <p class="meta">Kiến thức chuyên môn · Môi trường</p>
          </div>
        </li>
        <li>
          <div class="news-thumb">TT</div>
          <div>
            <a href="../gioi-thieu/index.html">Apoliq mở cổng thông tin dịch vụ kiểm nghiệm &amp; chứng nhận</a>
            <p class="meta">Tin hoạt động</p>
          </div>
        </li>
      </ul>
    </div>
  </section>
""",
        ),
    )

    write(
        ROOT / "van-ban" / "index.html",
        shell(
            "Văn bản – Tài liệu | Apoliq",
            "Tài liệu tham khảo liên quan kiểm nghiệm, chứng nhận và môi trường.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Văn bản</div>
      <h1>Văn bản – Tài liệu</h1>
      <p>Tài liệu hướng dẫn nội bộ và liên kết tham khảo cho khách hàng.</p>
    </div>
  </section>
  <section class="content">
    <div class="container card-grid">
      <div class="info-card"><h3>Hướng dẫn gửi mẫu</h3><p>Chuẩn bị thông tin sản phẩm, số lượng mẫu và mục đích kiểm nghiệm trước khi liên hệ.</p></div>
      <div class="info-card"><h3>Checklist công bố</h3><p>Các hạng mục thường cần khi chuẩn bị hồ sơ công bố sản phẩm (tham khảo).</p></div>
      <div class="info-card"><h3>Lộ trình chứng nhận</h3><p>Các bước phổ biến khi triển khai HACCP / ISO 22000 / VietGAP.</p></div>
      <div class="info-card"><h3>Liên hệ nhận tài liệu</h3><p>Gửi yêu cầu tới <a href="mailto:info@apoliq.com">info@apoliq.com</a> để nhận hướng dẫn phù hợp.</p></div>
    </div>
  </section>
""",
        ),
    )

    write(
        ROOT / "lien-he" / "index.html",
        shell(
            "Liên hệ – Báo giá | Apoliq",
            "Liên hệ Apoliq để nhận báo giá kiểm nghiệm, chứng nhận hoặc tư vấn môi trường.",
            1,
            """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Trang chủ</a> / Liên hệ</div>
      <h1>Hỏi đáp – Liên hệ</h1>
      <p>Gửi yêu cầu báo giá hoặc trao đổi nhu cầu dịch vụ với đội ngũ Apoliq.</p>
    </div>
  </section>
  <section class="content">
    <div class="container content-grid">
      <div>
        <div class="contact-box" style="margin-bottom:1.2rem">
          <div><strong>Địa chỉ</strong><br>K2-15 Võ Nguyên Giáp, P. Hưng Phú, TP. Cần Thơ</div>
          <div><strong>Điện thoại</strong><br><a href="tel:+84917333965">0917 333 965</a></div>
          <div><strong>Email</strong><br><a href="mailto:info@apoliq.com">info@apoliq.com</a></div>
        </div>
        <form class="quote-form" action="mailto:info@apoliq.com" method="post" enctype="text/plain">
          <label>Họ tên<input name="name" required placeholder="Nguyễn Văn A"></label>
          <label>Số điện thoại<input name="phone" required placeholder="+84..."></label>
          <label>Email<input type="email" name="email" placeholder="ban@email.com"></label>
          <label>Nhóm dịch vụ
            <select name="service">
              <option>Kiểm nghiệm</option>
              <option>Chứng nhận</option>
              <option>Môi trường</option>
              <option>Khác</option>
            </select>
          </label>
          <label>Nội dung nhu cầu<textarea name="message" rows="5" required placeholder="Mô tả sản phẩm, chỉ tiêu hoặc loại chứng nhận..."></textarea></label>
          <button class="btn btn-primary" type="submit">Gửi yêu cầu</button>
        </form>
      </div>
      <aside class="side-card">
        <h3>FAQ nhanh</h3>
        <p><strong>Thời gian báo giá?</strong><br>Thường phản hồi trong ngày làm việc khi đủ thông tin mẫu.</p>
        <p><strong>Cần chuẩn bị gì?</strong><br>Tên sản phẩm, mục đích (công bố/QC), số mẫu, chỉ tiêu nếu đã biết.</p>
        <p><strong>Có những dịch vụ nào?</strong><br>Chỉ các nhóm Kiểm nghiệm, Chứng nhận, Môi trường đang liệt kê trên menu.</p>
      </aside>
    </div>
  </section>
""",
        ),
    )

    # homepage
    write(
        ROOT / "index.html",
        shell(
            "Apoliq | Kiểm nghiệm – Chứng nhận – Môi trường",
            "Apoliq Science and Technology JSC — dịch vụ kiểm nghiệm, chứng nhận và tư vấn môi trường tại Cần Thơ.",
            0,
            """
  <div class="ticker">
    <div class="container" style="display:flex;align-items:center;gap:.75rem;width:min(100% - 2rem,1180px)">
      <span class="ticker-badge">TIN HOT</span>
      <div class="ticker-track"><span>Apoliq nhận yêu cầu kiểm nghiệm thực phẩm, nước uống, mỹ phẩm · Tư vấn HACCP / ISO 22000 / VietGAP · Quan trắc &amp; tư vấn môi trường · Hotline 0917 333 965 · info@apoliq.com</span></div>
    </div>
  </div>

  <section class="container home-grid">
    <div class="panel">
      <div class="panel-head">Tin mới</div>
      <div class="panel-body feature-card">
        <div class="visual" style="height:200px;border-radius:8px;background:linear-gradient(135deg,#20b8c8,#089848);display:grid;place-items:center;color:#fff;font-weight:800;font-size:1.2rem;text-align:center;padding:1rem">Kiểm soát chất lượng<br>cùng Apoliq</div>
        <h3><a href="tin-tuc/index.html">Apoliq mở cổng thông tin dịch vụ kiểm nghiệm &amp; chứng nhận</a></h3>
        <p class="meta">Tin hoạt động</p>
        <p>Doanh nghiệp có thể tra cứu nhanh các gói kiểm nghiệm, chứng nhận và dịch vụ môi trường đang triển khai — chỉ hiển thị dịch vụ thực nhận.</p>
        <a class="btn btn-primary" href="lien-he/index.html">Nhận báo giá</a>
      </div>
    </div>

    <div class="panel">
      <div class="panel-head">Tin hoạt động</div>
      <div class="panel-body">
        <ul class="news-list">
          <li>
            <div class="news-thumb">TP</div>
            <div><a href="dich-vu/kiem-nghiem/thuc-pham.html">Kiểm nghiệm thực phẩm phục vụ công bố và QC định kỳ</a></div>
          </li>
          <li>
            <div class="news-thumb">NU</div>
            <div><a href="dich-vu/kiem-nghiem/nuoc-uong.html">Kiểm nghiệm nước sạch &amp; nước uống theo nhu cầu doanh nghiệp</a></div>
          </li>
          <li>
            <div class="news-thumb">HC</div>
            <div><a href="dich-vu/chung-nhan/haccp.html">Tư vấn chứng nhận HACCP cho xưởng thực phẩm</a></div>
          </li>
          <li>
            <div class="news-thumb">MT</div>
            <div><a href="dich-vu/moi-truong/quan-trac.html">Quan trắc môi trường định kỳ cho cơ sở sản xuất</a></div>
          </li>
        </ul>
      </div>
    </div>

    <div class="panel">
      <div class="hotline-box">
        <div class="label">Hotline tư vấn</div>
        <a href="tel:+84917333965">0917 333 965</a>
      </div>
      <div class="quick-links">
        <a href="dich-vu/kiem-nghiem/index.html"><span class="ico">KN</span>Danh mục kiểm nghiệm</a>
        <a href="dich-vu/chung-nhan/index.html"><span class="ico">CN</span>Danh mục chứng nhận</a>
        <a href="dich-vu/moi-truong/index.html"><span class="ico">MT</span>Dịch vụ môi trường</a>
        <a href="nang-luc/index.html"><span class="ico">NL</span>Năng lực dịch vụ</a>
        <a href="lien-he/index.html"><span class="ico">BG</span>Báo giá / Liên hệ</a>
      </div>
    </div>
  </section>

  <section class="section alt">
    <div class="container">
      <h2 class="section-title">Dịch vụ</h2>
      <div class="service-grid">
        <a class="service-tile" href="dich-vu/kiem-nghiem/index.html">
          <div class="visual">KN</div>
          <div class="body">
            <h3>Kiểm nghiệm</h3>
            <p>Thực phẩm, nước uống, mỹ phẩm, dược/TPCN, TACN, dinh dưỡng và yêu cầu đặc thù.</p>
            <span class="btn btn-outline">Xem dịch vụ</span>
          </div>
        </a>
        <a class="service-tile" href="dich-vu/chung-nhan/index.html">
          <div class="visual">CN</div>
          <div class="body">
            <h3>Chứng nhận</h3>
            <p>HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX.</p>
            <span class="btn btn-outline">Xem dịch vụ</span>
          </div>
        </a>
        <a class="service-tile" href="dich-vu/moi-truong/index.html">
          <div class="visual">MT</div>
          <div class="body">
            <h3>Môi trường</h3>
            <p>Quan trắc môi trường và tư vấn hồ sơ pháp lý cho cơ sở sản xuất.</p>
            <span class="btn btn-outline">Xem dịch vụ</span>
          </div>
        </a>
      </div>
    </div>
  </section>
""",
            canonical="https://apoliq.com/",
        ),
    )

    write(
        ROOT / "README.md",
        """# Apoliq — Website

Portal tĩnh của **APOLIQ SCIENCE AND TECHNOLOGY JOINT STOCK COMPANY**, layout theo phong cách nifc.gov.vn, màu logo Apoliq.

## Dịch vụ trên menu

Chỉ hiển thị dịch vụ đang có (cùng catalog TechLAB):

- **Kiểm nghiệm:** thực phẩm, bánh kẹo, nước uống, dược/TPCN, mỹ phẩm, TACN, dinh dưỡng, khác
- **Chứng nhận:** HACCP, ISO 22000, VietGAP, Organic, Halal, SMETA/SEDEX
- **Môi trường:** quan trắc, tư vấn

Không có trên menu: hiệu chuẩn, giám định, thử nghiệm thành thạo, mẫu chuẩn, kiểm tra hàng nhập…

## Local

Mở `index.html` hoặc:

```bash
python3 -m http.server 8080 --directory .
# http://127.0.0.1:8080/
```

Tạo lại các trang dịch vụ:

```bash
python3 generate-pages.py
```

## GitHub Pages

Repo: `make-qr/apoliq.com`  
URL: https://apoliq.com/

## Liên hệ

- K2-15 Võ Nguyên Giáp, P. Hưng Phú, TP. Cần Thơ
- 0917 333 965
- info@apoliq.com
""",
    )

    # GitHub Pages: project site needs relative links (already used).
    # Add .nojekyll so GH Pages serves as-is.
    write(ROOT / ".nojekyll", "")
    write(
        ROOT / ".gitignore",
        """__pycache__/
.DS_Store
*.log
https:--apoliq.com.txt
logo-1.png
""",
    )


if __name__ == "__main__":
    main()
