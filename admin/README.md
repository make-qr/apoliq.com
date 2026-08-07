# Admin đăng bài — Apoliq

Trang: **https://apoliq.com/admin/** (hoặc `admin/` trên máy local).

## Cách dùng (1 lần setup)

1. Mở [GitHub → Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Tạo **Classic token** với quyền **`repo`** (full control of private repositories — cần để ghi file lên `make-qr/apoliq.com`)
3. Mở https://apoliq.com/admin/ → dán token → **Lưu & tiếp tục**
4. Token chỉ lưu trên trình duyệt máy anh (`localStorage`). Không commit token vào git.

## Đăng bài

1. Điền tiêu đề, chuyên mục, ngày, mô tả SEO, lead, nội dung
2. Nội dung hỗ trợ:
   - `## Tiêu đề mục`
   - `### Tiêu đề nhỏ`
   - `- danh sách`
   - `1. danh sách số`
   - `**in đậm**`
   - Đoạn văn: cách nhau bằng dòng trống
3. Chọn **ảnh hero** (bắt buộc) và ảnh trong bài (tuỳ chọn)
4. **Xem trước HTML** nếu cần → **Đăng bài lên website**
5. Đợi GitHub Pages ~20–60 giây rồi mở `/tin-tuc/{slug}.html`

Admin sẽ tự:

- Upload ảnh → `images/tin-tuc/{slug}-hero.jpg` (+ inline nếu có)
- Tạo `tin-tuc/{slug}.html`
- Cập nhật `tin-tuc/posts.json` và `tin-tuc/index.html`

## Bảo mật

- Không share token; nếu lộ → revoke ngay trên GitHub
- Nút **Xóa token** trên admin để xóa khỏi trình duyệt
- Trang có `noindex` — không đưa vào sitemap/menu công khai
