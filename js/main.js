(function () {
  const PHONE_CT_DISPLAY = "0917 333 965";
  const PHONE_CT_TEL = "+84917333965";
  const EMAIL = "info@apoliq.com";
  const ADDR_CT =
    "K2-15 Võ Nguyên Giáp, P. Hưng Phú, TP. Cần Thơ";

  function depthPrefix() {
    const depth = Number(document.body.dataset.depth || "0");
    return "../".repeat(depth);
  }

  function headerHTML() {
    const root = depthPrefix();
    return `
<header class="site-header">
  <div class="container header-top">
    <a class="brand" href="${root}index.html">
      <img src="${root}images/logo.png" alt="Apoliq logo" width="176" height="49">
      <div class="brand-text">
        <strong>APOLIQ SCIENCE AND TECHNOLOGY JOINT STOCK COMPANY</strong>
        <span>Công ty Cổ phần Khoa học và Công nghệ Apoliq</span>
      </div>
    </a>
    <div class="header-tools">
      <form class="search-box" action="${root}lien-he/index.html" method="get" role="search">
        <input type="search" name="q" placeholder="Tìm kiếm..." aria-label="Tìm kiếm">
        <button type="submit" aria-label="Tìm">⌕</button>
      </form>
    </div>
  </div>
</header>
<nav class="nav-bar" aria-label="Menu chính">
  <div class="container nav-inner" id="navInner">
    <ul class="nav-list">
      <li><a href="${root}index.html">Trang chủ</a></li>
      <li>
        <button type="button" aria-expanded="false">Giới thiệu ▾</button>
        <ul class="dropdown">
          <li><a href="${root}gioi-thieu/index.html">Giới thiệu chung</a></li>
          <li><a href="${root}gioi-thieu/chinh-sach-chat-luong.html">Chính sách chất lượng</a></li>
          <li><a href="${root}gioi-thieu/co-cau-to-chuc.html">Cơ cấu tổ chức</a></li>
          <li><a href="${root}gioi-thieu/chuc-nang.html">Chức năng – Nhiệm vụ</a></li>
          <li><a href="${root}gioi-thieu/thanh-tich.html">Thành tích – Định hướng</a></li>
          <li><a href="${root}nang-luc/index.html">Năng lực</a></li>
          <li><a href="${root}nang-luc/trang-thiet-bi.html">Trang thiết bị</a></li>
        </ul>
      </li>
      <li><a href="${root}nang-luc/index.html">Năng lực</a></li>
      <li>
        <button type="button" aria-expanded="false">Dịch vụ ▾</button>
        <ul class="dropdown">
          <li><a href="${root}dich-vu/kiem-nghiem/index.html"><strong>Kiểm nghiệm</strong></a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/huong-dan-gui-mau.html">· Hướng dẫn gửi mẫu</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/thuc-pham.html">· Thực phẩm</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/banh-keo.html">· Bánh kẹo</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/nuoc-uong.html">· Nước uống</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/duoc-pham.html">· Dược phẩm / TPCN</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/my-pham.html">· Mỹ phẩm</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/thuc-an-chan-nuoi.html">· Thức ăn chăn nuôi</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/dinh-duong.html">· Dinh dưỡng / ghi nhãn</a></li>
          <li><a href="${root}dich-vu/kiem-nghiem/khac.html">· Dịch vụ khác</a></li>
          <li><a href="${root}dich-vu/chung-nhan/index.html"><strong>Chứng nhận</strong></a></li>
          <li><a href="${root}dich-vu/chung-nhan/haccp.html">· HACCP</a></li>
          <li><a href="${root}dich-vu/chung-nhan/iso-22000.html">· ISO 22000</a></li>
          <li><a href="${root}dich-vu/chung-nhan/vietgap.html">· VietGAP</a></li>
          <li><a href="${root}dich-vu/chung-nhan/organic.html">· Organic</a></li>
          <li><a href="${root}dich-vu/chung-nhan/halal.html">· Halal</a></li>
          <li><a href="${root}dich-vu/chung-nhan/smeta-sedex.html">· SMETA / SEDEX</a></li>
          <li><a href="${root}dich-vu/moi-truong/index.html"><strong>Môi trường</strong></a></li>
          <li><a href="${root}dich-vu/moi-truong/quan-trac.html">· Quan trắc môi trường</a></li>
          <li><a href="${root}dich-vu/moi-truong/tu-van.html">· Tư vấn môi trường</a></li>
        </ul>
      </li>
      <li><a href="${root}tin-tuc/index.html">Tin tức</a></li>
      <li><a href="${root}van-ban/index.html">Văn bản – Tài liệu</a></li>
      <li><a href="${root}lien-he/index.html">Hỏi đáp – Liên hệ</a></li>
    </ul>
    <button type="button" class="nav-toggle" id="navToggle" aria-label="Mở menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>`;
  }

  function footerHTML() {
    const root = depthPrefix();
    return `
<footer class="site-footer">
  <div class="container footer-contact">
    <div class="footer-contact-main">
      <h3>Trụ sở chính — Cần Thơ</h3>
      <p class="footer-address">${ADDR_CT}</p>
    </div>
    <div class="footer-contact-meta">
      <p><span class="footer-label">Hotline</span> <a href="tel:${PHONE_CT_TEL}">${PHONE_CT_DISPLAY}</a></p>
      <p><span class="footer-label">Email</span> <a href="mailto:${EMAIL}">${EMAIL}</a></p>
    </div>
  </div>
  <div class="container footer-links-row">
    <a href="${root}dich-vu/kiem-nghiem/index.html">Kiểm nghiệm</a>
    <a href="${root}dich-vu/chung-nhan/index.html">Chứng nhận</a>
    <a href="${root}dich-vu/moi-truong/index.html">Môi trường</a>
    <a href="${root}nang-luc/index.html">Năng lực</a>
    <a href="${root}tin-tuc/index.html">Tin tức</a>
    <a href="${root}lien-he/index.html">Liên hệ / Báo giá</a>
  </div>
  <div class="container footer-bottom">
    © ${new Date().getFullYear()} Apoliq Science and Technology Joint Stock Company. All rights reserved.
  </div>
</footer>`;
  }

  function bindSecureQuoteForms() {
    document.querySelectorAll("form.quote-form").forEach((form) => {
      const action = (form.getAttribute("action") || "").trim();
      // #region agent log
      fetch("http://127.0.0.1:7684/ingest/50fec90f-3a5c-4043-90b3-1fb261f9789c", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "b9a7e9" },
        body: JSON.stringify({
          sessionId: "b9a7e9",
          runId: "post-fix",
          hypothesisId: "H1",
          location: "js/main.js:bindSecureQuoteForms",
          message: "quote form action before normalize",
          data: {
            path: location.pathname,
            actionBefore: action,
            insecureBefore: /^(mailto:|javascript:|http:)/i.test(action),
          },
          timestamp: Date.now(),
        }),
      }).catch(() => {});
      // #endregion

      // Chrome disables autofill on mailto:/http: form actions even on HTTPS pages.
      if (/^(mailto:|javascript:|http:)/i.test(action) || action === "") {
        form.setAttribute("action", "#");
      }
      form.removeAttribute("enctype");
      form.setAttribute("method", "post");

      const autoMap = {
        name: "name",
        "Họ và tên": "name",
        phone: "tel",
        "Số điện thoại": "tel",
        email: "email",
        Email: "email",
      };
      form.querySelectorAll("input, textarea, select").forEach((el) => {
        if (el.getAttribute("autocomplete")) return;
        const key = el.getAttribute("name") || el.getAttribute("data-field") || "";
        if (autoMap[key]) el.setAttribute("autocomplete", autoMap[key]);
      });

      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const lines = [];
        new FormData(form).forEach((value, key) => {
          const v = String(value || "").trim();
          if (v) lines.push(`${key}: ${v}`);
        });
        const subject = encodeURIComponent("Yêu cầu báo giá — Apoliq");
        const body = encodeURIComponent(lines.join("\n") || "(Không có nội dung)");
        window.location.href = `mailto:${EMAIL}?subject=${subject}&body=${body}`;
      });

      // #region agent log
      fetch("http://127.0.0.1:7684/ingest/50fec90f-3a5c-4043-90b3-1fb261f9789c", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "b9a7e9" },
        body: JSON.stringify({
          sessionId: "b9a7e9",
          runId: "post-fix",
          hypothesisId: "H1",
          location: "js/main.js:bindSecureQuoteForms",
          message: "quote form action after normalize",
          data: {
            path: location.pathname,
            actionAfter: form.getAttribute("action"),
            insecureAfter: /^(mailto:|javascript:|http:)/i.test(form.getAttribute("action") || ""),
          },
          timestamp: Date.now(),
        }),
      }).catch(() => {});
      // #endregion
    });
  }

  function mountShell() {
    const headerMount = document.getElementById("site-header");
    const footerMount = document.getElementById("site-footer");
    if (headerMount) headerMount.innerHTML = headerHTML();
    if (footerMount) footerMount.innerHTML = footerHTML();

    bindSecureQuoteForms();

    const navInner = document.getElementById("navInner");
    const navToggle = document.getElementById("navToggle");
    if (navToggle && navInner) {
      navToggle.addEventListener("click", () => {
        const open = navInner.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", String(open));
      });
    }

    document.querySelectorAll(".nav-list > li > button").forEach((btn) => {
      btn.addEventListener("click", () => {
        const li = btn.parentElement;
        const open = li.classList.toggle("open");
        btn.setAttribute("aria-expanded", String(open));
      });
    });
  }

  document.addEventListener("DOMContentLoaded", mountShell);
})();
