/**
 * Apoliq Admin — đăng bài tin tức qua GitHub Contents API.
 * Token chỉ lưu localStorage trên máy anh.
 */
(function () {
  "use strict";

  const STORAGE_KEY = "apoliq_admin_auth";
  const CACHE_V = "7";
  const CSS_V = "20260807g";
  const NEWS_CSS_V = "20260807e";

  const $ = (id) => document.getElementById(id);

  const authCard = $("authCard");
  const editorCard = $("editorCard");
  const previewCard = $("previewCard");
  const listCard = $("listCard");
  const logEl = $("log");

  function todayISO() {
    const d = new Date();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${m}-${day}`;
  }

  function formatDateVN(iso) {
    if (!iso) return "";
    const [y, m, d] = iso.split("-");
    return `${d}/${m}/${y}`;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function slugify(text) {
    return String(text || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d")
      .replace(/Đ/g, "D")
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .slice(0, 80);
  }

  function loadAuth() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    } catch {
      return null;
    }
  }

  function saveAuth(auth) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(auth));
  }

  function clearAuth() {
    localStorage.removeItem(STORAGE_KEY);
  }

  function log(msg, isErr) {
    logEl.hidden = false;
    const line = `[${new Date().toLocaleTimeString("vi-VN")}] ${msg}`;
    logEl.textContent += (logEl.textContent ? "\n" : "") + line;
    logEl.classList.toggle("err", !!isErr);
    logEl.scrollTop = logEl.scrollHeight;
  }

  function clearLog() {
    logEl.textContent = "";
    logEl.hidden = true;
  }

  /** Markdown-lite → HTML (##, ###, -, 1., paragraphs, **bold**) */
  function bodyToHtml(raw) {
    const lines = String(raw || "").replace(/\r\n/g, "\n").split("\n");
    const out = [];
    let i = 0;

    function flushPara(buf) {
      const t = buf.join(" ").trim();
      if (!t) return;
      const withBold = escapeHtml(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      out.push(`<p>${withBold}</p>`);
    }

    while (i < lines.length) {
      const line = lines[i];
      const trimmed = line.trim();

      if (!trimmed) {
        i += 1;
        continue;
      }

      if (trimmed.startsWith("### ")) {
        out.push(`<h3>${escapeHtml(trimmed.slice(4))}</h3>`);
        i += 1;
        continue;
      }
      if (trimmed.startsWith("## ")) {
        out.push(`<h2>${escapeHtml(trimmed.slice(3))}</h2>`);
        i += 1;
        continue;
      }

      if (/^[-*]\s+/.test(trimmed)) {
        const items = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) {
          const t = lines[i].trim().replace(/^[-*]\s+/, "");
          items.push(
            `<li>${escapeHtml(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")}</li>`
          );
          i += 1;
        }
        out.push(`<ul>\n${items.join("\n")}\n</ul>`);
        continue;
      }

      if (/^\d+\.\s+/.test(trimmed)) {
        const items = [];
        while (i < lines.length && /^\d+\.\s+/.test(lines[i].trim())) {
          const t = lines[i].trim().replace(/^\d+\.\s+/, "");
          items.push(
            `<li>${escapeHtml(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")}</li>`
          );
          i += 1;
        }
        out.push(`<ol>\n${items.join("\n")}\n</ol>`);
        continue;
      }

      const buf = [trimmed];
      i += 1;
      while (i < lines.length) {
        const n = lines[i].trim();
        if (!n || n.startsWith("##") || /^[-*]\s+/.test(n) || /^\d+\.\s+/.test(n)) break;
        buf.push(n);
        i += 1;
      }
      flushPara(buf);
    }

    return out.join("\n\n");
  }

  function pickRelated(posts, slug, n) {
    const others = posts.filter((p) => p.slug !== slug);
    const shuffled = others.slice().sort(() => Math.random() - 0.5);
    return shuffled.slice(0, n);
  }

  function buildArticleHtml(meta, bodyHtml, related) {
    const title = escapeHtml(meta.title);
    const desc = escapeHtml(meta.description);
    const tag = escapeHtml(meta.tag);
    const date = escapeHtml(meta.date);
    const author = escapeHtml(meta.author || "Apoliq");
    const lead = escapeHtml(meta.lead);
    const hero = `../images/tin-tuc/${meta.slug}-hero.jpg?v=${CACHE_V}`;
    const inline = meta.hasInline
      ? `../images/tin-tuc/${meta.slug}-inline.jpg?v=${CACHE_V}`
      : "";

    const relatedAside = related
      .map(
        (p) =>
          `<li><a href="${escapeHtml(p.slug)}.html">${escapeHtml(p.title)}</a></li>`
      )
      .join("\n");

    const relatedCards = related
      .slice(0, 3)
      .map(
        (p) => `
            <article class="news-card" data-tag="${escapeHtml(p.tag || "")}">
                <div class="news-card-accent" aria-hidden="true"></div>
                <div class="news-card-inner">
                    <div class="news-card-meta"><span class="news-card-tag">${escapeHtml(p.tag || "")}</span></div>
                    <h2><a href="${escapeHtml(p.slug)}.html">${escapeHtml(p.title)}</a></h2>
                    <p>${escapeHtml(p.description || p.lead || "")}</p>
                    <div class="news-card-footer">
                        <a class="news-card-link" href="${escapeHtml(p.slug)}.html">Đọc tiếp <i class="fas fa-arrow-right"></i></a>
                        <span class="news-card-date">${escapeHtml(p.date || "")}</span>
                    </div>
                </div>
            </article>`
      )
      .join("\n");

    const inlineBlock = inline
      ? `
<figure class="news-inline">
  <img src="${inline}" alt="${title} — minh họa" width="960" height="540" loading="lazy">
</figure>`
      : "";

    // Insert inline image after first h2 block if present
    let content = bodyHtml;
    if (inlineBlock) {
      const h2Idx = content.indexOf("</h2>");
      if (h2Idx !== -1) {
        const after = content.indexOf("\n", h2Idx);
        const pos = after !== -1 ? after + 1 : h2Idx + 5;
        content = content.slice(0, pos) + "\n" + inlineBlock + "\n" + content.slice(pos);
      } else {
        content = inlineBlock + "\n\n" + content;
      }
    }

    return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} | Apoliq</title>
  <meta name="description" content="${desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../css/style.css?v=${CSS_V}">
  <link rel="stylesheet" href="../css/service-page.css?v=${NEWS_CSS_V}">
  <link rel="stylesheet" href="../css/news.css?v=${NEWS_CSS_V}">
  <link rel="icon" href="../images/logo.png" type="image/png">
</head>
<body data-depth="1" class="service-page">
  <div id="site-header"></div>
<section class="news-article-hero">
        <div class="container">
            <div class="news-article-hero-inner">
                <nav class="news-breadcrumb" aria-label="Breadcrumb">
                    <a href="../index.html">Trang chủ</a>
                    <span class="news-breadcrumb-sep">/</span>
                    <a href="index.html">Tin tức</a>
                    <span class="news-breadcrumb-sep">/</span>
                    <span>${tag}</span>
                </nav>
                <h1>${title}</h1>
                <div class="news-article-meta">
                    <span class="news-card-tag">${tag}</span>
                    <span><i class="far fa-calendar-alt"></i> ${date}</span>
                    <span>${author}</span>
                </div>
            </div>
        </div>
    </section>
    <div class="news-layout">
        <article class="news-article-body">
            <div class="container">
<figure class="news-featured">
  <img src="${hero}" alt="${title}" width="960" height="540" loading="eager">
</figure>
<p class="news-lead">${lead}</p>
${content}
                <div class="news-cta-box">
                    <p><strong>Cần báo giá kiểm nghiệm?</strong> Apoliq — phòng lab ISO/IEC 17025, nhận mẫu CT · HN · HCM.</p>
                    <div class="news-cta-actions"><a href="../index.html#bao-gia" class="btn btn-hero-primary">Gửi yêu cầu</a><a href="tel:+84901339669" class="btn btn-hero-secondary">Gọi 0901 339 669</a></div>
                </div>
            </div>
        </article>
                <aside class="news-aside" aria-label="Thông tin bổ sung">
                    <div class="news-aside-card">
                        <h3>Bài liên quan</h3>
                        <ul class="news-aside-list">
${relatedAside}
                        </ul>
                    </div>
                    <div class="news-aside-card news-aside-cta">
                        <h3>Cần báo giá?</h3>
                        <p>Lab ISO/IEC 17025 — nhận mẫu CT · HN · HCM.</p>
                        <a href="../index.html#bao-gia" class="btn btn-hero-primary">Gửi yêu cầu</a>
                    </div>
                </aside>
    </div>
    <section class="news-related">
        <div class="container">
            <h2>Đọc tiếp</h2>
            <div class="news-grid">
${relatedCards}
            </div>
        </div>
    </section>
  <div id="site-footer"></div>
  <script src="../js/main.js?v=${CSS_V}"></script>
</body>
</html>
`;
  }

  function buildIndexHtml(posts) {
    const sorted = posts.slice().sort((a, b) => a.slug.localeCompare(b.slug, "vi"));
    const items = sorted
      .map((p) => {
        const title = escapeHtml(p.title);
        const slug = escapeHtml(p.slug);
        const img = `../images/tin-tuc/${slug}-hero.jpg?v=${CACHE_V}`;
        return `        <li class="news-item-card">
          <a class="news-item-link" href="${slug}.html">
            <img class="news-thumb-img" src="${img}" alt="${title}" width="160" height="100" loading="lazy">
            <span class="news-item-title">${title}</span>
          </a>
        </li>`;
      })
      .join("\n");

    return `<!DOCTYPE html>
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
  <link rel="stylesheet" href="../css/style.css?v=${CSS_V}">
  <link rel="stylesheet" href="../css/news.css?v=${NEWS_CSS_V}">
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
${items}
      </ul>
    </div>
  </section>
  <div id="site-footer"></div>
  <script src="../js/main.js?v=${CSS_V}"></script>
</body>
</html>
`;
  }

  async function fileToJpegBase64(file, maxW) {
    const bitmap = await createImageBitmap(file);
    const scale = Math.min(1, (maxW || 1600) / bitmap.width);
    const w = Math.round(bitmap.width * scale);
    const h = Math.round(bitmap.height * scale);
    const canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, w, h);
    ctx.drawImage(bitmap, 0, 0, w, h);
    bitmap.close();
    const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
    return dataUrl.split(",")[1];
  }

  function textToBase64(text) {
    return btoa(unescape(encodeURIComponent(text)));
  }

  async function ghRequest(auth, method, path, body) {
    const url = `https://api.github.com/repos/${auth.repo}/contents/${path}`;
    const headers = {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${auth.token}`,
      "X-GitHub-Api-Version": "2022-11-28",
    };
    const opts = { method, headers };
    if (body) {
      headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    const res = await fetch(url + (method === "GET" ? `?ref=${encodeURIComponent(auth.branch)}` : ""), opts);
    if (method === "GET" && res.status === 404) return null;
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = data.message || res.statusText || "GitHub API error";
      throw new Error(msg);
    }
    return data;
  }

  async function ghGet(auth, path) {
    return ghRequest(auth, "GET", path);
  }

  async function ghPut(auth, path, contentB64, message, sha) {
    const body = {
      message,
      content: contentB64,
      branch: auth.branch,
    };
    if (sha) body.sha = sha;
    return ghRequest(auth, "PUT", path, body);
  }

  async function verifyAuth(auth) {
    const res = await fetch(`https://api.github.com/repos/${auth.repo}`, {
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${auth.token}`,
        "X-GitHub-Api-Version": "2022-11-28",
      },
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.message || "Token hoặc repo không hợp lệ");
    }
    return res.json();
  }

  async function loadPosts(auth) {
    const file = await ghGet(auth, "tin-tuc/posts.json");
    if (!file || !file.content) return [];
    const json = decodeURIComponent(escape(atob(file.content.replace(/\n/g, ""))));
    return { posts: JSON.parse(json), sha: file.sha };
  }

  function getFormMeta() {
    const title = $("title").value.trim();
    let slug = $("slug").value.trim() || slugify(title);
    slug = slugify(slug);
    return {
      title,
      slug,
      tag: $("tag").value,
      date: formatDateVN($("date").value),
      dateIso: $("date").value,
      author: $("author").value.trim() || "Apoliq",
      description: $("description").value.trim(),
      lead: $("lead").value.trim(),
      body: $("body").value,
      hasInline: !!$("inlineFile").files[0],
    };
  }

  function showEditor(auth) {
    authCard.classList.add("hidden");
    editorCard.classList.remove("hidden");
    listCard.classList.remove("hidden");
    $("authStatus").textContent = `Đã kết nối ${auth.repo} (${auth.branch})`;
    $("authStatus").className = "status ok";
  }

  function showAuth() {
    authCard.classList.remove("hidden");
    editorCard.classList.add("hidden");
    previewCard.classList.add("hidden");
    listCard.classList.add("hidden");
  }

  async function refreshList(auth) {
    const box = $("postList");
    box.innerHTML = "<p class='hint'>Đang tải…</p>";
    try {
      const data = await loadPosts(auth);
      const posts = data.posts || [];
      if (!posts.length) {
        box.innerHTML = "<p class='hint'>Chưa có bài trong posts.json</p>";
        return;
      }
      box.innerHTML = posts
        .slice()
        .sort((a, b) => a.slug.localeCompare(b.slug, "vi"))
        .map(
          (p) => `<div class="post-item">
            <a href="../tin-tuc/${escapeHtml(p.slug)}.html" target="_blank" rel="noopener">${escapeHtml(p.title)}</a>
            <span class="hint">${escapeHtml(p.date || "")} · ${escapeHtml(p.tag || "")}</span>
          </div>`
        )
        .join("");
    } catch (e) {
      box.innerHTML = `<p class="status err">${escapeHtml(e.message)}</p>`;
    }
  }

  // --- UI wiring ---
  $("date").value = todayISO();

  $("title").addEventListener("input", () => {
    if (!$("slug").dataset.manual) {
      $("slug").value = slugify($("title").value);
    }
  });
  $("slug").addEventListener("input", () => {
    $("slug").dataset.manual = "1";
  });

  function previewFile(input, img) {
    input.addEventListener("change", () => {
      const f = input.files[0];
      if (!f) {
        img.classList.add("hidden");
        img.removeAttribute("src");
        return;
      }
      img.src = URL.createObjectURL(f);
      img.classList.remove("hidden");
    });
  }
  previewFile($("heroFile"), $("heroPreview"));
  previewFile($("inlineFile"), $("inlinePreview"));

  $("btnSaveAuth").addEventListener("click", async () => {
    const token = $("ghToken").value.trim();
    const repo = $("ghRepo").value.trim();
    const branch = $("ghBranch").value.trim() || "master";
    if (!token) {
      alert("Nhập GitHub Personal Access Token");
      return;
    }
    const auth = { token, repo, branch };
    $("btnSaveAuth").disabled = true;
    try {
      await verifyAuth(auth);
      saveAuth(auth);
      showEditor(auth);
      await refreshList(auth);
    } catch (e) {
      alert("Không kết nối được: " + e.message);
    } finally {
      $("btnSaveAuth").disabled = false;
    }
  });

  $("btnLogout").addEventListener("click", () => {
    clearAuth();
    $("ghToken").value = "";
    showAuth();
  });

  $("btnPreview").addEventListener("click", () => {
    const meta = getFormMeta();
    const html = bodyToHtml(meta.body);
    previewCard.classList.remove("hidden");
    $("previewBody").innerHTML =
      `<p class="news-lead"><em>${escapeHtml(meta.lead)}</em></p>` + html;
    previewCard.scrollIntoView({ behavior: "smooth" });
  });

  $("postForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const auth = loadAuth();
    if (!auth) {
      alert("Chưa đăng nhập GitHub");
      return;
    }

    const meta = getFormMeta();
    if (!meta.title || !meta.slug || !meta.description || !meta.lead || !meta.body) {
      alert("Điền đủ các trường bắt buộc");
      return;
    }
    const heroFile = $("heroFile").files[0];
    if (!heroFile) {
      alert("Chọn ảnh hero");
      return;
    }

    const btn = $("btnPublish");
    btn.disabled = true;
    clearLog();
    log("Bắt đầu đăng bài…");

    try {
      const existing = await ghGet(auth, `tin-tuc/${meta.slug}.html`);
      if (existing) {
        const ok = confirm(
          `Slug "${meta.slug}" đã tồn tại. Ghi đè bài cũ?`
        );
        if (!ok) {
          btn.disabled = false;
          return;
        }
      }

      log("Nén ảnh hero…");
      const heroB64 = await fileToJpegBase64(heroFile, 1600);
      const heroPath = `images/tin-tuc/${meta.slug}-hero.jpg`;
      const heroExisting = await ghGet(auth, heroPath);
      log("Upload ảnh hero…");
      await ghPut(
        auth,
        heroPath,
        heroB64,
        `admin: upload hero ${meta.slug}`,
        heroExisting && heroExisting.sha
      );

      let hasInline = false;
      const inlineFile = $("inlineFile").files[0];
      if (inlineFile) {
        log("Nén & upload ảnh trong bài…");
        const inlineB64 = await fileToJpegBase64(inlineFile, 1400);
        const inlinePath = `images/tin-tuc/${meta.slug}-inline.jpg`;
        const inlineExisting = await ghGet(auth, inlinePath);
        await ghPut(
          auth,
          inlinePath,
          inlineB64,
          `admin: upload inline ${meta.slug}`,
          inlineExisting && inlineExisting.sha
        );
        hasInline = true;
      }
      meta.hasInline = hasInline;

      log("Đọc danh sách bài…");
      const postsData = await loadPosts(auth);
      let posts = postsData.posts || [];
      const related = pickRelated(posts, meta.slug, 5);

      const bodyHtml = bodyToHtml(meta.body);
      const articleHtml = buildArticleHtml(meta, bodyHtml, related);
      const articlePath = `tin-tuc/${meta.slug}.html`;
      log("Tạo trang bài viết…");
      await ghPut(
        auth,
        articlePath,
        textToBase64(articleHtml),
        `admin: đăng bài ${meta.slug}`,
        existing && existing.sha
      );

      const entry = {
        slug: meta.slug,
        title: meta.title,
        description: meta.description,
        lead: meta.lead,
        tag: meta.tag,
        date: meta.date,
        hero: `../images/tin-tuc/${meta.slug}-hero.jpg`,
        inline: hasInline
          ? `../images/tin-tuc/${meta.slug}-inline.jpg`
          : `../images/tin-tuc/${meta.slug}-hero.jpg`,
      };
      posts = posts.filter((p) => p.slug !== meta.slug);
      posts.unshift(entry);

      log("Cập nhật posts.json…");
      await ghPut(
        auth,
        "tin-tuc/posts.json",
        textToBase64(JSON.stringify(posts, null, 2) + "\n"),
        `admin: cập nhật posts.json — ${meta.slug}`,
        postsData.sha
      );

      log("Cập nhật danh sách tin tức…");
      const indexFile = await ghGet(auth, "tin-tuc/index.html");
      const indexHtml = buildIndexHtml(posts);
      await ghPut(
        auth,
        "tin-tuc/index.html",
        textToBase64(indexHtml),
        `admin: cập nhật tin-tuc/index — ${meta.slug}`,
        indexFile && indexFile.sha
      );

      log("Xong! Bài sẽ lên https://apoliq.com/tin-tuc/" + meta.slug + ".html sau ~1 phút.");
      await refreshList(auth);
      alert("Đã đăng bài thành công!\n\nhttps://apoliq.com/tin-tuc/" + meta.slug + ".html");
      $("postForm").reset();
      $("date").value = todayISO();
      $("author").value = "Apoliq";
      $("heroPreview").classList.add("hidden");
      $("inlinePreview").classList.add("hidden");
      delete $("slug").dataset.manual;
    } catch (e) {
      log("Lỗi: " + e.message, true);
      alert("Đăng bài thất bại: " + e.message);
    } finally {
      btn.disabled = false;
    }
  });

  // Boot
  (async function init() {
    const auth = loadAuth();
    if (auth && auth.token) {
      $("ghToken").value = auth.token;
      $("ghRepo").value = auth.repo || "make-qr/apoliq.com";
      $("ghBranch").value = auth.branch || "master";
      try {
        await verifyAuth(auth);
        showEditor(auth);
        await refreshList(auth);
      } catch {
        clearAuth();
        showAuth();
      }
    }
  })();
})();
