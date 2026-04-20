const SOURCE_FEEDS = [
  {
    id: "siemens",
    name: "Siemens",
    brand: "Siemens",
    url: "https://www.siemens.com/",
    cadence: "Otomatik taraniyor",
    focus: ["Yazilim", "Digital Twin", "OT/IT"],
  },
  {
    id: "schneider-electric",
    name: "Schneider Electric",
    brand: "Schneider Electric",
    url: "https://www.se.com/",
    cadence: "Otomatik taraniyor",
    focus: ["OT/IT", "Energy", "Industrial AI"],
  },
  {
    id: "rockwell-automation",
    name: "Rockwell Automation",
    brand: "Rockwell Automation",
    url: "https://www.rockwellautomation.com/",
    cadence: "Otomatik taraniyor",
    focus: ["PLC Donanimi", "FactoryTalk", "Analytics"],
  },
  {
    id: "abb",
    name: "ABB",
    brand: "ABB",
    url: "https://global.abb/",
    cadence: "Otomatik taraniyor",
    focus: ["Industrial AI", "Motion", "Robotics"],
  },
  {
    id: "beckhoff",
    name: "Beckhoff",
    brand: "Beckhoff",
    url: "https://www.beckhoff.com/",
    cadence: "Otomatik taraniyor",
    focus: ["Motion", "EtherCAT", "Automation"],
  },
];

const INGESTION_STAGES = [
  {
    title: "Kaynak tarama",
    detail: "Resmi press ve newsroom sayfalari duzenli araliklarla kontrol edilir.",
  },
  {
    title: "Yeni link tespiti",
    detail: "Slug ve benzer kayitlar kontrol edilerek tekrar yayin onlenir.",
  },
  {
    title: "AI ceviri ve ozet",
    detail: "Metin Turkceye cevrilir, teknik terimler korunur ve sade bir yapiya donusturulur.",
  },
  {
    title: "Yayin",
    detail: "Supabase'e yazilan veri ana sayfa ve detay sayfasinda otomatik gorunur.",
  },
];

const AI_PIPELINE_NOTES = {
  promptLabel: "AI isleme kurali",
  promptSummary:
    "Basligi Turkcelestir, kisa bir ozet cikar, govdeyi duzenle, kategoriyi sec ve resmi kaynagi gorunur birak.",
};

const CATEGORY_LABELS = {
  Yazilim: "Yazilim",
  "PLC Donanimi": "PLC Donanimi",
  "OT/IT": "OT / IT",
  "Industrial AI": "Industrial AI",
  Motion: "Motion",
  Guvenlik: "Guvenlik",
  "Digital Twin": "Digital Twin",
};

const BRAND_ICONS = {
  Siemens: "⚙️",
  "Rockwell Automation": "🔩",
  "Schneider Electric": "🌐",
  ABB: "🤖",
  Beckhoff: "⚡",
  KUKA: "🤖",
  "Bosch Rexroth": "🦾",
  "Phoenix Contact": "🔌",
  "Parker Hannifin": "⚙️",
};

const CATEGORY_FALLBACKS = {
  Yazilim: [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1400&q=80&sat=-10",
  ],
  "PLC Donanimi": [
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1400&q=80&sat=-10",
  ],
  "OT/IT": [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1400&q=80&hue=10",
  ],
  "Industrial AI": [
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1400&q=80&sat=-15",
  ],
  Motion: [
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
  ],
  Guvenlik: [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1400&q=80&sat=-25",
  ],
  "Digital Twin": [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1400&q=80&sat=-5",
  ],
};

const BRAND_FALLBACKS = {
  KUKA: [
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1400&q=80&sat=-12",
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1300&q=80&hue=8",
  ],
  "Bosch Rexroth": [
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1350&q=80&sat=-8",
  ],
  "Phoenix Contact": [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1350&q=80&sat=-8",
  ],
  "Parker Hannifin": [
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1300&q=80&hue=12",
  ],
  Siemens: [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1280&q=80&hue=20",
  ],
  "Rockwell Automation": [
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1280&q=80&sat=-10",
  ],
  "Schneider Electric": [
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1759836096317-e746643cc277?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1695668548342-c0c1ad479aee?auto=format&fit=crop&w=1280&q=80&sat=-12",
  ],
  ABB: [
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1752614671052-92e18f534db1?auto=format&fit=crop&w=1280&q=80&hue=10",
  ],
  Beckhoff: [
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1756973584844-ae528fadd2c2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1684695747561-9372850cf165?auto=format&fit=crop&w=1280&q=80&sat=-12",
  ],
};

const usedDisplayImages = new Set();

let supabaseClient;

function getSupabaseConfig() {
  const config = window.AUTOS_NEWS_CONFIG || {};
  return {
    supabaseUrl: config.supabaseUrl || "",
    supabaseAnonKey: config.supabaseAnonKey || "",
  };
}

function getSupabaseClient() {
  if (supabaseClient) {
    return supabaseClient;
  }

  if (!window.supabase || typeof window.supabase.createClient !== "function") {
    throw new Error("Supabase istemcisi yuklenemedi.");
  }

  const config = getSupabaseConfig();
  if (!config.supabaseUrl || !config.supabaseAnonKey) {
    throw new Error("config.js icinde supabaseUrl ve supabaseAnonKey alanlarini doldurman gerekiyor.");
  }

  supabaseClient = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
  return supabaseClient;
}

function normalizeCategory(value) {
  if (!value) {
    return "Yazilim";
  }

  const cleaned = String(value).trim();
  const map = {
    "Yazılım": "Yazilim",
    Yazilim: "Yazilim",
    "PLC Donanımı": "PLC Donanimi",
    "PLC Donanimi": "PLC Donanimi",
    "OT / IT": "OT/IT",
    "OT/IT": "OT/IT",
    "Industrial AI": "Industrial AI",
    Motion: "Motion",
    Güvenlik: "Guvenlik",
    Guvenlik: "Guvenlik",
    "Digital Twin": "Digital Twin",
  };

  return map[cleaned] || cleaned;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

function escapeJs(value) {
  return String(value ?? "").replace(/\\/g, "\\\\").replace(/'/g, "\\'");
}

function initialsForBrand(brand) {
  return String(brand || "AN")
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function articleIcon(article) {
  return BRAND_ICONS[article.brand] || "📰";
}

function isTrustedImageUrl(url) {
  if (!url) {
    return false;
  }

  const lowered = String(url).toLowerCase();
  if (!lowered.startsWith("http://") && !lowered.startsWith("https://")) {
    return false;
  }

  const blockedHosts = ["news.google.com", "google.com", "googleusercontent.com", "gstatic.com"];
  return !blockedHosts.some((host) => lowered.includes(host));
}

function buildFallbackImage(article) {
  const pool =
    BRAND_FALLBACKS[article.brand] ||
    CATEGORY_FALLBACKS[article.categoryKey] ||
    CATEGORY_FALLBACKS["Industrial AI"];

  const seed = hashString(`${article.slug || ""}:${article.brand || ""}:${article.categoryKey || ""}`);
  const candidates = Array.isArray(pool) ? pool : [pool];

  for (let offset = 0; offset < candidates.length; offset += 1) {
    const candidate = candidates[(seed + offset) % candidates.length];
    if (!usedDisplayImages.has(candidate)) {
      usedDisplayImages.add(candidate);
      return candidate;
    }
  }

  const fallback = candidates[seed % candidates.length];
  usedDisplayImages.add(fallback);
  return fallback;
}

function hashString(value) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash * 31 + value.charCodeAt(index)) >>> 0;
  }
  return hash;
}

function gradientClass(index) {
  const classes = ["g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8"];
  return classes[index % classes.length];
}

function splitBodyToParagraphs(body) {
  return String(body || "")
    .split(/\n{2,}/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function renderBodyParagraphs(body) {
  const paragraphs = splitBodyToParagraphs(body);
  if (!paragraphs.length) {
    return "<p>Bu haber icin govde icerigi henuz olusmadi.</p>";
  }
  return paragraphs.map((paragraph) => "<p>" + escapeHtml(paragraph) + "</p>").join("");
}

function bodyPreview(body) {
  const plain = String(body || "").replace(/\s+/g, " ").trim();
  return plain.slice(0, 180) + (plain.length > 180 ? "..." : "");
}

function parseDateValue(row) {
  if (row.created_at) {
    const parsed = new Date(row.created_at);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed;
    }
  }
  if (row.date) {
    const parsed = new Date(row.date);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed;
    }
  }
  return new Date(0);
}

function formatDateLabel(row) {
  if (row.created_at) {
    const parsed = new Date(row.created_at);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleDateString("tr-TR", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
    }
  }
  return row.date || "Tarih yok";
}

function mapArticle(row) {
  const categoryKey = normalizeCategory(row.category);
  const sourceImageUrl = row.image_url || "";

  return {
    ...row,
    categoryKey,
    category: CATEGORY_LABELS[categoryKey] || categoryKey,
    dateLabel: formatDateLabel(row),
    readTime: row.read_time || row.readTime || "3 dk",
    excerpt: row.excerpt || "",
    body: row.body || "",
    sourceImageUrl,
    imageUrl: isTrustedImageUrl(sourceImageUrl) ? sourceImageUrl : "",
    bodyPreview: bodyPreview(row.body),
    originalUrl: row.original_url || "#",
    brandInitials: initialsForBrand(row.brand),
    brandTag: String(row.brand || "kaynak").replace(/\s+/g, ""),
    categoryTag: String(CATEGORY_LABELS[categoryKey] || categoryKey).replace(/\s+/g, ""),
    sortDate: parseDateValue(row),
  };
}

function withDisplayImage(article) {
  return {
    ...article,
    displayImageUrl: article.imageUrl || buildFallbackImage(article),
  };
}

function sortArticles(rows) {
  return rows.sort((left, right) => right.sortDate - left.sortDate);
}

async function fetchArticles(limit = 30) {
  const client = getSupabaseClient();
  const { data, error } = await client.from("articles").select("*").limit(limit);

  if (error) {
    throw new Error(error.message);
  }

  return sortArticles((data || []).map(mapArticle)).map(withDisplayImage);
}

async function fetchArticleBySlug(slug) {
  const client = getSupabaseClient();
  const { data, error } = await client
    .from("articles")
    .select("*")
    .eq("slug", slug)
    .limit(1)
    .maybeSingle();

  if (error) {
    throw new Error(error.message);
  }

  return data ? withDisplayImage(mapArticle(data)) : null;
}

async function fetchRelatedArticles(article, limit = 5) {
  const articles = await fetchArticles(Math.max(20, limit + 8));
  return articles.filter((item) => item.slug !== article.slug).slice(0, limit);
}

function renderRelated(items) {
  if (!items.length) {
    return '<div class="sidebar-source-box"><div class="source-box-desc">Bu haber disinda gosterilecek ek kayit bulunamadi.</div></div>';
  }

  return items
    .map(
      (article, index) => `
    <div class="related-item" onclick="window.location.href='article.html?slug=${escapeJs(article.slug)}'">
      <div class="related-thumb ${gradientClass(index + 1)}">${articleIcon(article)}</div>
      <div class="related-body">
        <div class="related-cat">${escapeHtml(article.category)}</div>
        <div class="related-title">${escapeHtml(article.title)}</div>
        <div class="related-date">${escapeHtml(article.dateLabel)}</div>
      </div>
    </div>
  `,
    )
    .join("");
}
