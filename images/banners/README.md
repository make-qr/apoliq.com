# Banner hero — từng trang landing

## Cấu trúc hiện tại

| Loại trang | Ảnh | Ghi chú |
|------------|-----|---------|
| **Trang chủ** `index.html` | `images/hero-banner-trang-chu.png` | Kiểm nghiệm nước — sửa trong `css/style.css` (`body.home .hero`) |
| **Hồ sơ năng lực** | `images/hero-banner.jpg` | Đội ngũ tập thể |
| **Trang con** `pages/*.html` | `images/banners/<slug>.jpg` | Mỗi trang một ảnh — bảng bên dưới |

## Bảng banner đang dùng (16 trang)

### Kiểm nghiệm
| Trang | File banner |
|-------|-------------|
| `kiem-nghiem-thuc-pham.html` | `kiem-nghiem-thuc-pham.jpg` |
| `kiem-nghiem-banh-keo.html` | `kiem-nghiem-banh-keo.jpg` |
| `kiem-nghiem-nuoc-giai-khat.html` | `kiem-nghiem-nuoc-giai-khat.png` |
| `kiem-nghiem-my-pham.html` | `kiem-nghiem-my-pham.jpg` |
| `kiem-nghiem-duoc-pham.html` | `kiem-nghiem-duoc-pham.jpg` |
| `kiem-nghiem-dinh-duong.html` | `kiem-nghiem-dinh-duong.jpg` |
| `kiem-nghiem-thuc-an-chan-nuoi.html` | `kiem-nghiem-thuc-an-chan-nuoi.jpg` |
| `dich-vu-kiem-nghiem-khac.html` | `dich-vu-kiem-nghiem-khac.jpg` |
| `quan-trac-moi-truong.html` | `quan-trac-moi-truong.jpg` |
| `tu-van-moi-truong.html` | `tu-van-moi-truong.jpg` |

### Chứng nhận
| Trang | File banner |
|-------|-------------|
| `chung-nhan-vietgap.html` | `chung-nhan-vietgap.jpg` |
| `chung-nhan-haccp.html` | `chung-nhan-haccp.jpg` |
| `chung-nhan-iso-22000.html` | `chung-nhan-iso-22000.jpg` |
| `chung-nhan-organic.html` | `chung-nhan-organic.jpg` |
| `chung-nhan-halal.html` | `chung-nhan-halal.jpg` |
| `chung-nhan-smeta-sedex.html` | `chung-nhan-smeta-sedex.jpg` |

---

## Đổi banner một trang (thủ công)

### Bước 1 — Chuẩn bị ảnh
- Kích thước: **1600×900** px trở lên (tỉ lệ ngang 16:9)
- Định dạng: **JPG** (ưu tiên, nhẹ) hoặc PNG
- Dung lượng: **150–300 KB** sau nén ([squoosh.app](https://squoosh.app))
- Tên file = **slug trang**, không dấu: `kiem-nghiem-thuc-pham.jpg`

### Bước 2 — Copy vào thư mục
```bash
cp anh-moi.jpg ~/huong-dan/he-thong-du-an/03_KiemNghiem/kiemnghiem-techlab/images/banners/kiem-nghiem-thuc-pham.jpg
```

### Bước 3 — Kiểm tra HTML (thường đã có sẵn)
Mở `pages/kiem-nghiem-thuc-pham.html`, tìm dòng:
```html
<section class="service-hero" style="--hero-bg: url('../images/banners/kiem-nghiem-thuc-pham.jpg')">
```
Chỉ cần **thay file** trong `images/banners/` — không sửa HTML nếu tên file giữ nguyên.

### Bước 4 — Căn khung ảnh (tùy chọn)
Nếu ảnh có người/thiết bị bên phải, thêm `--hero-pos`:
```html
<section class="service-hero" style="--hero-bg: url('../images/banners/ten-file.jpg'); --hero-pos: 72% center">
```
Mặc định: `center 35%` (định nghĩa trong `css/service-page.css`).

### Bước 5 — Xem lại
```bash
cd ~/huong-dan/he-thong-du-an/03_KiemNghiem/kiemnghiem-techlab
npx serve .
```
Mở trang → **Ctrl+Shift+R** (hard refresh).

---

## Đổi hàng loạt (script)

Sau khi thay ảnh nguồn trong `images/`, chạy lại:
```bash
python3 scripts/setup-page-banners.py
```
Script copy ảnh vào `banners/` và cập nhật thẻ `<section class="service-hero">`.

## Đổi banner trang chủ

1. Thay file `images/hero-banner-trang-chu.png`
2. Hard refresh trang chủ
3. (Tùy chọn) Sửa `background-position` trong `css/style.css` → `body.home .hero`
