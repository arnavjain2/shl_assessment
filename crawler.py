import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

PAGE_SIZE = 12
MAX_PAGES = 40          # enough to exceed 377
DETAIL_WORKERS = 6

# --------------------------------------------------
# SCRAPE ONE TABLE PAGE
# --------------------------------------------------
def scrape_table(table):
    assessments = []
    rows = table.find_all("tr")[1:]  # skip header

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        # Name + URL
        name_tag = cols[0].find("a")
        if not name_tag:
            continue

        name = name_tag.text.strip()
        url = "https://www.shl.com" + name_tag["href"]

        # Remote Support
        remote_support = (
            "Yes" if cols[1].find("span", class_="catalogue__circle -yes") else "No"
        )

        # Adaptive Support
        adaptive_support = (
            "Yes" if cols[2].find("span", class_="catalogue__circle -yes") else "No"
        )

        # Test Type (K / P / etc.)
        test_keys = cols[3].find_all("span", class_="product-catalogue__key")
        test_type = ", ".join(k.text.strip() for k in test_keys) if test_keys else "N/A"

        assessments.append({
            "name": name,
            "url": url,
            "description": "N/A",
            "duration": "N/A",
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "test_type": test_type
        })

    return assessments

# --------------------------------------------------
# SCRAPE PAGINATED CATALOG (INDIVIDUAL TESTS)
# --------------------------------------------------
def scrape_catalog():
    all_assessments = []

    for start in range(0, MAX_PAGES * PAGE_SIZE, PAGE_SIZE):
        url = f"{BASE_URL}?start={start}&type=1"
        print(f"🔍 Catalog page: {url}")

        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print("❌ Failed page, stopping")
            break

        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")

        if not table:
            print("❌ No table found, stopping")
            break

        page_items = scrape_table(table)
        if not page_items:
            print("❌ No more assessments, stopping")
            break

        all_assessments.extend(page_items)
        time.sleep(1)

    return all_assessments

# --------------------------------------------------
# ENRICH EACH ASSESSMENT PAGE
# --------------------------------------------------
def fetch_assessment_details(assessment):
    try:
        r = requests.get(assessment["url"], headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return assessment

        soup = BeautifulSoup(r.content, "html.parser")

        # ------------------------------------------
        # Parse structured info rows (YOUR FINDING)
        # ------------------------------------------
        info_rows = soup.find_all(
            "div",
            class_="product-catalogue-training-calendar__row"
        )

        extracted = {}

        for row in info_rows:
            title = row.find("h4")
            value = row.find("p")

            if not title or not value:
                continue

            key = title.text.strip().lower()
            val = value.text.strip()
            extracted[key] = val

        # Description
        assessment["description"] = extracted.get("description", "N/A")

        # Duration (Assessment length)
        duration_text = extracted.get("assessment length", "")
        match = re.search(r'(\d+)', duration_text)
        if match:
            assessment["duration"] = int(match.group(1))

    except Exception:
        pass

    return assessment

# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------
def scrape_shl_catalog():
    print("\n🚀 Starting SHL catalog scrape\n")

    assessments = scrape_catalog()
    print(f"\n✅ Catalog rows collected: {len(assessments)}")

    print("\n🔍 Enriching assessment pages (description & duration)...\n")

    with ThreadPoolExecutor(max_workers=DETAIL_WORKERS) as executor:
        futures = [
            executor.submit(fetch_assessment_details, a)
            for a in assessments
        ]

        for i, _ in enumerate(as_completed(futures), 1):
            if i % 25 == 0:
                print(f"Progress: {i}/{len(assessments)}")

    df = pd.DataFrame(assessments).drop_duplicates(subset=["url"])

    # Appendix-2 compliant column order
    df = df[
        [
            "name",
            "url",
            "description",
            "duration",
            "remote_support",
            "adaptive_support",
            "test_type"
        ]
    ]

    print(f"\n📊 FINAL COUNT: {len(df)}")
    assert len(df) >= 377, "Catalog size requirement not met"

    df.to_csv("shl_assessments.csv", index=False)
    print("✅ Saved to shl_assessments.csv")

    return df

# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    scrape_shl_catalog()
