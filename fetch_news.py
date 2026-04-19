import requests
import google.genai as genai
from supabase import create_client
import json
import os
import re
from datetime import datetime

# ── BAĞLANTILAR ──────────────────────────────────────────
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS2JSON = "https://api.rss2json.com/v1/api.json?rss_url="

# ── ÇALIŞAN RSS FEED'LER ─────────────────────────────────
RSS_FEEDS = [
    {
        "brand": "Control Engineering",
        "url": "https://www.controleng.com/feed/",
        "category_default": "Yazılım"
    },
    {
        "brand": "Automation World",
        "url": "https://www.automationworld.com/rss.xml",
        "category_default": "OT/IT"
    },
    {
        "brand": "Plant Engineering",
        "url": "https://www.plantengineering.com/rss/all",
        "category_default": "PLC Donanımı"
    },
    {
        "brand": "Manufacturing Tomorrow",
        "url": "https://www.manufacturingtomorrow.com/rss/articles",
        "category_default": "Industrial AI"
    },
    {
        "brand": "IEEE Spectrum",
        "url": "https://spectrum.ieee.org/feeds/topic/robotics.rss",
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

# ── RSS PROXY İLE ÇEK ───────────────────────────────────
def fetch_feed(url):
    try:
        resp = requests.get(RSS2JSON + url, timeout=15)
        data = resp.json()
        if data.get("status") == "ok":
            items = data.get("items", [])
            print(f"  → {len(items)} haber bulundu")
            return items[:3]
        else:
            print(f"  ✗ Hata: {data.get('message', 'bilinmiyor')}")
            return []
    except Exception as e:
        print(f"  ✗ Bağlantı hatası: {e}")
        return []

# ── MEVCUT SLUG'LARI ÇEK ────────────────────────────────
def get_existing_slugs():
    try:
        result = supabase.table("articles").select("slug").execute()
        return {row["slug"] for row in result.data}
    except Exception as e:
        print(f"Supabase okuma hatası: {e}")
        return set()

# ── GEMİNİ İLE ÖZETLE ───────────────────────────────────
def summarize(brand, raw_title, raw_content, category_default):
    clean = re.sub(r'<[^>]+>', ' ', raw_content)
    clean = re.sub(r'\s+', ' ', clean).strip()

    prompt = f"""Sen endüstriyel otomasyon alanında uzman bir teknik editörsün.
Aşağıdaki İngilizce haberi Türkçeye çevir ve özetle. SADECE JSON döndür, başka hiçbir şey yazma.

Kaynak: {brand}
Başlık: {raw_title}
İçerik: {clean[:1200]}

Yanıt formatı:
{{
  "title": "Türkçe başlık (max 80 karakter)",
  "excerpt": "Türkçe kısa özet, 2 cümle (max 200 karakter)",
  "body": "Türkçe detaylı özet, 3-4 paragraf",
  "category": "Şunlardan biri: {', '.join(CATEGORIES)}",
  "readTime": "X dk"
}}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        text = response.text.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse hatası: {e}")
        return None
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

        entries = fetch_feed(feed_info["url"])
        if not entries:
            continue

        for entry in entries:
            raw_title = entry.get("title", "").strip()
            raw_content = entry.get("description", entry.get("content", ""))

            if not raw_title:
                continue

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
                print(f"  ✅ Eklendi: {result['title'][:50]}")
                added += 1
            except Exception as e:
                print(f"  ✗ Supabase yazma hatası: {e}")

    print(f"\n🎉 Tamamlandı. {added} yeni haber eklendi.")

if __name__ == "__main__":
    main()
