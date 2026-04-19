import feedparser
import google.generativeai as genai
from supabase import create_client
import json
import os
import re
from datetime import datetime

# ── BAĞLANTILAR ──────────────────────────────────────────
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── RSS FEED'LER ─────────────────────────────────────────
RSS_FEEDS = [
    {
        "brand": "Siemens",
        "url": "https://news.siemens.com/global/en/news.rss",
        "category_default": "Yazılım"
    },
    {
        "brand": "Rockwell Automation",
        "url": "https://www.rockwellautomation.com/en-us/company/news/press-releases.rss",
        "category_default": "PLC Donanımı"
    },
    {
        "brand": "Schneider Electric",
        "url": "https://www.se.com/ww/en/about-us/newsroom/news/rss.xml",
        "category_default": "OT/IT"
    },
    {
        "brand": "ABB",
        "url": "https://new.abb.com/news/rss",
        "category_default": "Industrial AI"
    },
    {
        "brand": "Beckhoff",
        "url": "https://www.beckhoff.com/en-en/support/news-and-press/rss/",
        "category_default": "Motion"
    },
]

CATEGORIES = ["Yazılım", "PLC Donanımı", "OT/IT", "Industrial AI", "Motion", "Güvenlik", "Digital Twin"]

# ── SLUG OLUŞTUR ─────────────────────────────────────────
def make_slug(title):
    slug = title.lower()
    for old, new in [("ğ","g"),("ü","u"),("ş","s"),("ı","i"),("ö","o"),("ç","c")]:
        slug = slug.replace(old, new)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug[:60]

# ── MEVCUT SLUG'LARI ÇEK (tekrar ekleme önleme) ─────────
def get_existing_slugs():
    try:
        result = supabase.table("articles").select("slug").execute()
        return {row["slug"] for row in result.data}
    except Exception as e:
        print(f"Supabase okuma hatası: {e}")
        return set()

# ── GEMİNİ İLE ÖZETLE ───────────────────────────────────
def summarize(brand, raw_title, raw_content, category_default):
    prompt = f"""
Sen endüstriyel otomasyon alanında uzman bir teknik editörsün.
Aşağıdaki haberi analiz et ve JSON formatında döndür.

Kaynak: {brand}
Ham başlık: {raw_title}
Ham içerik: {raw_content[:1500]}

Şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "title": "Türkçe, net ve ilgi çekici başlık (max 80 karakter)",
  "excerpt": "2-3 cümle Türkçe özet, teknik ama anlaşılır (max 200 karakter)",
  "body": "Haberin Türkçe tam özeti, 3-5 paragraf, teknik detaylarla",
  "category": "Şunlardan biri seç: {', '.join(CATEGORIES)}",
  "readTime": "X dk"
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text)
    except Exception as e:
        print(f"  ⚠ Gemini hatası: {e}")
        return None

# ── ANA DÖNGÜ ────────────────────────────────────────────
def main():
    existing_slugs = get_existing_slugs()
    print(f"Veritabanında {len(existing_slugs)} mevcut haber var.")
    today = datetime.now().strftime("%d %b %Y")
    added = 0

    for feed_info in RSS_FEEDS:
        brand = feed_info["brand"]
        print(f"\n📡 {brand} RSS çekiliyor...")

        try:
            feed = feedparser.parse(feed_info["url"])
            entries = feed.entries[:5]
        except Exception as e:
            print(f"  ✗ RSS hatası: {e}")
            continue

        for entry in entries:
            raw_title = entry.get("title", "")
            raw_content = entry.get("summary", entry.get("description", ""))

            temp_slug = make_slug(raw_title)
            if temp_slug in existing_slugs:
                print(f"  → Zaten var: {raw_title[:50]}")
                continue

            print(f"  ✓ Özetleniyor: {raw_title[:60]}")
            result = summarize(brand, raw_title, raw_content, feed_info["category_default"])
            if not result:
                continue

            slug = make_slug(result["title"])
            existing_slugs.add(slug)

            row = {
                "slug":         slug,
                "brand":        brand,
                "category":     result.get("category", feed_info["category_default"]),
                "title":        result["title"],
                "excerpt":      result["excerpt"],
                "body":         result.get("body", ""),
                "date":         today,
                "read_time":    result.get("readTime", "3 dk"),
                "original_url": entry.get("link", ""),
            }

            try:
                supabase.table("articles").insert(row).execute()
                print(f"  ✅ Supabase'e eklendi: {result['title'][:50]}")
                added += 1
            except Exception as e:
                print(f"  ✗ Supabase yazma hatası: {e}")

    print(f"\n🎉 Tamamlandı. {added} yeni haber eklendi.")

if __name__ == "__main__":
    main()
