import json
import os
import re
import time
import unicodedata
from datetime import datetime

import feedparser
import google.generativeai as genai
from supabase import create_client


GENAI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
REQUEST_DELAY_SECONDS = int(os.getenv("REQUEST_DELAY_SECONDS", "5"))
MAX_ENTRIES_PER_FEED = int(os.getenv("MAX_ENTRIES_PER_FEED", "2"))

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(GENAI_MODEL)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS_FEEDS = [
    {
        "brand": "Siemens",
        "url": "https://news.siemens.com/global/en/feed/",
        "category_default": "Yazilim",
    },
    {
        "brand": "Rockwell Automation",
        "url": "https://www.rockwellautomation.com/en-us/company/news/press-releases/_jcr_content/root/container/container/parsys_copy_19886/genericlist_copy.stream.json?content-type=text/rss",
        "category_default": "PLC Donanimi",
    },
    {
        "brand": "Schneider Electric",
        "url": "https://www.se.com/ww/en/about-us/newsroom/rss-news.jsp",
        "category_default": "OT/IT",
    },
    {
        "brand": "ABB",
        "url": "https://global.abb/group/en/media/rss-feeds/news.xml",
        "category_default": "Industrial AI",
    },
    {
        "brand": "Beckhoff",
        "url": "https://www.beckhoff.com/en-en/company/news/rss.xml",
        "category_default": "Motion",
    },
]

CATEGORIES = [
    "Yazilim",
    "PLC Donanimi",
    "OT/IT",
    "Industrial AI",
    "Motion",
    "Guvenlik",
    "Digital Twin",
]


def make_slug(title):
    slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = slug.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug[:60]


def get_existing_slugs():
    try:
        result = supabase.table("articles").select("slug").execute()
        return {row["slug"] for row in result.data}
    except Exception as exc:
        print(f"Supabase okuma hatasi: {exc}")
        return set()


def parse_json_response(text):
    cleaned = text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def summarize(brand, raw_title, raw_content):
    prompt = f"""
Sen endustriyel otomasyon alaninda uzman bir teknik editorsun.
Asagidaki haberi analiz et ve sadece gecerli JSON dondur.

Kaynak: {brand}
Ham baslik: {raw_title}
Ham icerik: {raw_content[:1500]}

Su JSON formatina sadik kal:
{{
  "title": "Turkce, net ve ilgi cekici baslik (max 80 karakter)",
  "excerpt": "2-3 cumle Turkce ozet, teknik ama anlasilir (max 200 karakter)",
  "body": "Haberin Turkce tam ozeti, 3-5 paragraf, teknik detaylarla",
  "category": "Sunlardan biri: {', '.join(CATEGORIES)}",
  "readTime": "X dk"
}}
"""
    try:
        if REQUEST_DELAY_SECONDS > 0:
            print(f"    Gemini istegi oncesi {REQUEST_DELAY_SECONDS} sn bekleniyor...")
            time.sleep(REQUEST_DELAY_SECONDS)

        response = model.generate_content(prompt)
        return parse_json_response(response.text)
    except Exception as exc:
        print(f"    Gemini hatasi: {exc}")
        if "RESOURCE_EXHAUSTED" in str(exc) or "429" in str(exc):
            print("    Not: Bu hata genelde kota/proje/API key kaynakli olur. Sadece bekleme eklemek tek basina yetmeyebilir.")
        return None


def get_entry_content(entry):
    if entry.get("summary"):
        return entry["summary"]
    if entry.get("description"):
        return entry["description"]
    content_items = entry.get("content") or []
    if content_items and isinstance(content_items, list):
        return content_items[0].get("value", "")
    return ""


def load_feed(feed_info):
    feed = feedparser.parse(feed_info["url"])

    if getattr(feed, "bozo", 0):
        print(f"  RSS uyarisi: {feed.bozo_exception}")

    entries = getattr(feed, "entries", [])[:MAX_ENTRIES_PER_FEED]
    if not entries:
        print("  RSS bos veya gecersiz gorunuyor.")
        return []

    return entries


def main():
    existing_slugs = get_existing_slugs()
    print(f"Veritabaninda {len(existing_slugs)} mevcut haber var.")
    print(f"Model: {GENAI_MODEL}")
    print(f"Istekler arasi bekleme: {REQUEST_DELAY_SECONDS} saniye")
    print(f"Her kaynaktan alinacak haber: {MAX_ENTRIES_PER_FEED}")

    today = datetime.now().strftime("%d %b %Y")
    added = 0

    for feed_info in RSS_FEEDS:
        brand = feed_info["brand"]
        print(f"\\n{brand} RSS cekiliyor...")

        try:
            entries = load_feed(feed_info)
        except Exception as exc:
            print(f"  RSS hatasi: {exc}")
            continue

        for entry in entries:
            raw_title = entry.get("title", "").strip()
            raw_content = get_entry_content(entry)

            if not raw_title:
                print("  Baslik bos oldugu icin atlandi.")
                continue

            temp_slug = make_slug(raw_title)
            if temp_slug in existing_slugs:
                print(f"  Zaten var: {raw_title[:60]}")
                continue

            print(f"  Ozetleniyor: {raw_title[:60]}")
            result = summarize(brand, raw_title, raw_content)
            if not result:
                continue

            title = result.get("title", raw_title).strip()
            slug = make_slug(title)
            existing_slugs.add(slug)

            row = {
                "slug": slug,
                "brand": brand,
                "category": result.get("category", feed_info["category_default"]),
                "title": title,
                "excerpt": result.get("excerpt", "")[:200],
                "body": result.get("body", ""),
                "date": today,
                "read_time": result.get("readTime", "3 dk"),
                "original_url": entry.get("link", ""),
            }

            try:
                supabase.table("articles").insert(row).execute()
                print(f"  Supabase'e eklendi: {title[:60]}")
                added += 1
            except Exception as exc:
                print(f"  Supabase yazma hatasi: {exc}")

    print(f"\\nTamamlandi. {added} yeni haber eklendi.")


if __name__ == "__main__":
    main()
