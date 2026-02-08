import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from urllib.parse import quote, unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

# ==========================================
# SETTINGS
# ==========================================
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "TalhaY61")
GITHUB_REPO = os.getenv("GITHUB_REPO", "open-hutbe-api")
GITHUB_PAGES_BASE = f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO}"

START_PAGE = 1
END_PAGE = int(os.getenv("HUTBE_MAX_PAGES", "10")) 
TIMEOUT = 45

# Static Prayer PDFs
PRAYER_URLS = {
    "friday_prayer": {
        "title": "Friday Khutbah Prayers",
        "url": "https://dinhizmetleri.diyanet.gov.tr/HutbeDualari/Cuma%20Hutbesi%20Dualar%C4%B1.pdf"
    },
    "eid_prayer": {
        "title": "Eid Khutbah Prayers",
        "url": "https://dinhizmetleri.diyanet.gov.tr/HutbeDualari/Bayram%20Hutbesi%20Dualar%C4%B1.pdf"
    }
}

# Diyanet Language Links
URLS = {
    "tr": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/türkçe",
    "de": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/deutsche-(almanca)",
    "en": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/english-(ingilizce)",
    "fr": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/français-(fransızca)",
    "ru": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/русский-(rusça)",
    "ar": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/عربي-(arapça)",
    "it": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/italiano-(italyanca)",
    "es": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/espanol-(ispanyolca)"
}

BASE_SITE = "https://dinhizmetleri.diyanet.gov.tr"
ROOT = Path(__file__).resolve().parents[1]

# OUTPUT FILES
HUTBES_PATH = ROOT / "hutbes.json"
PRAYERS_PATH = ROOT / "prayers.json"
PDF_ROOT = ROOT / "pdfs"

DATE_RE = re.compile(r"\b(\d{1,2}\.\d{1,2}\.\d{4})\b")
YEAR_RE = re.compile(r"(20\d{2})")

def load_json(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_json(data: List[Dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hutbe_id_from_url(source_pdf_url: str) -> str:
    return hashlib.sha1(source_pdf_url.encode("utf-8")).hexdigest()[:16]

def slugify_filename(text: str) -> str:
    text = unquote(text).strip()
    # Turkish char mapping
    replacements = {"ı": "i", "İ": "i", "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u", "ş": "s", "Ş": "s", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c"}
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text or "hutbe"

def download_file(session: requests.Session, url: str, destination: Path) -> bool:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with session.get(url, stream=True, timeout=TIMEOUT, verify=False) as r:
            if r.status_code != 200:
                return False
            with destination.open("wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 32):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:
        print(f"Download error {url}: {e}")
        return False

def process_prayers(session: requests.Session) -> None:
    print("\n--- Processing Prayers ---")
    prayers_list = []
    
    # Folder for prayers
    prayers_dir = PDF_ROOT / "prayers"
    prayers_dir.mkdir(parents=True, exist_ok=True)

    for key, info in PRAYER_URLS.items():
        url = info["url"]
        title = info["title"]
        
        filename = f"{slugify_filename(title)}.pdf"
        local_path = prayers_dir / filename
        
        if not local_path.exists():
            print(f"Downloading prayer: {title}")
            success = download_file(session, url, local_path)
            if not success:
                print(f"Failed to download prayer: {title}")
                continue
        else:
            print(f"Prayer already exists: {title}")

        public_url = f"{GITHUB_PAGES_BASE}/pdfs/prayers/{quote(filename)}"
        
        prayers_list.append({
            "id": key,
            "title": title,
            "filename": filename,
            "pdf_url": public_url,
            "source_url": url
        })

    save_json(prayers_list, PRAYERS_PATH)
    print("prayers.json updated.")

def extract_pdf_candidates(page_html: str, page_url: str) -> List[Dict]:
    soup = BeautifulSoup(page_html, "html.parser")
    candidates: List[Dict] = []

    # 1. Method: Scan table rows
    for row in soup.find_all("tr"):
        pdf_anchor = None
        for a in row.find_all("a", href=True):
            if a["href"].strip().lower().endswith(".pdf"):
                pdf_anchor = a
                break
        if not pdf_anchor:
            continue

        source_pdf_url = urljoin(BASE_SITE, pdf_anchor["href"])
        row_text = row.get_text(" ", strip=True)
        date_match = DATE_RE.search(row_text)
        parsed_date = datetime.strptime(date_match.group(1), "%d.%m.%Y").date() if date_match else None
        
        title = pdf_anchor.get_text(" ", strip=True)
        if not title or len(title) < 3:
             title = Path(unquote(urlsplit(source_pdf_url).path)).stem

        candidates.append({
            "source_pdf_url": source_pdf_url,
            "title": title,
            "date": parsed_date,
            "found_on_page": page_url,
        })

    # 2. Method: Fallback
    if not candidates:
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.lower().endswith(".pdf"):
                source_pdf_url = urljoin(BASE_SITE, href)
                title = a.get_text(" ", strip=True) or Path(unquote(urlsplit(source_pdf_url).path)).stem
                candidates.append({
                    "source_pdf_url": source_pdf_url,
                    "title": title,
                    "date": None,
                    "found_on_page": page_url,
                })

    return candidates

def determine_year(candidate: Dict) -> int:
    if candidate["date"]:
        return candidate["date"].year
    source_name = Path(unquote(urlsplit(candidate["source_pdf_url"]).path)).stem
    year_match = YEAR_RE.search(source_name)
    if year_match:
        return int(year_match.group(1))
    return datetime.now(timezone.utc).year

def main() -> None:
    requests.packages.urllib3.disable_warnings() 
    session = requests.Session()
    
    # Process Prayers first
    process_prayers(session)
    
    # Process Hutbes
    hutbes = load_json(HUTBES_PATH)
    existing_ids = {item.get("id") for item in hutbes}
    existing_urls = {item.get("source_pdf_url") for item in hutbes}
    new_entries: List[Dict] = []
    
    print(f"\nStarting Hutbe Scan: {len(hutbes)} existing items found.")

    for lang, base_url in URLS.items():
        print(f"--- Scanning Language: {lang.upper()} ---")
        
        for page_num in range(START_PAGE, END_PAGE + 1):
            page_url = f"{base_url}?page={page_num}"
            print(f"   Scanning page {page_num}...")
            
            try:
                response = session.get(page_url, timeout=TIMEOUT, verify=False)
                if response.status_code != 200:
                    print(f"   Page not found, skipping.")
                    break
                
                candidates = extract_pdf_candidates(response.text, page_url)
                if not candidates:
                    print("   Content not found, stopping.")
                    break

                for candidate in candidates:
                    source_url = candidate["source_pdf_url"]
                    h_id = hutbe_id_from_url(source_url)
                    
                    if h_id in existing_ids or source_url in existing_urls:
                        continue

                    year = determine_year(candidate)
                    base_slug = slugify_filename(candidate["title"])
                    filename = f"{base_slug}.pdf"
                    
                    local_rel_path = f"{lang}/{year}/{filename}"
                    local_path = PDF_ROOT / lang / str(year) / filename
                    
                    if local_path.exists():
                        filename = f"{base_slug}-{h_id[:6]}.pdf"
                        local_path = PDF_ROOT / lang / str(year) / filename

                    print(f"      Downloading: {candidate['title']}")
                    success = download_file(session, source_url, local_path)
                    
                    if success:
                        public_url = f"{GITHUB_PAGES_BASE}/pdfs/{lang}/{year}/{quote(filename)}"
                        date_str = candidate["date"].isoformat() if candidate["date"] else datetime.now().strftime("%Y-%m-%d")

                        new_entry = {
                            "id": h_id,
                            "title": candidate["title"],
                            "date": date_str,
                            "year": year,
                            "language": lang,
                            "filename": filename,
                            "source_pdf_url": source_url,
                            "pdf_url": public_url,
                        }
                        
                        new_entries.append(new_entry)
                        hutbes.insert(0, new_entry)
                        existing_ids.add(h_id)
                        existing_urls.add(source_url)
            
            except Exception as e:
                print(f"   Error: {e}")
                continue

    if new_entries:
        save_json(hutbes, HUTBES_PATH)
        print(f"Complete. Added {len(new_entries)} new hutbes.")
    else:
        print("No new hutbes found.")

if __name__ == "__main__":
    main()