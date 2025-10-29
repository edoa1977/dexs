import csv, time, json, re, pathlib, datetime, random
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (PortfolioBot; +https://github.com/your-username/ecommerce-price-monitor)"
}

def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text

def parse_value(html: str, css: str | None, regex: str | None):
    if css:
        soup = BeautifulSoup(html, "lxml")
        el = soup.select_one(css)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)
    if regex:
        m = re.search(regex, html, re.I)
        if m:
            return m.group(0)
    return None

def monitor_once(sites: list[dict]) -> list[dict]:
    rows = []
    for s in sites:
        try:
            html = fetch(s["url"])
            price_raw = parse_value(html, s["price"].get("css"), s["price"].get("regex"))
            stock_raw = parse_value(html, s["in_stock"].get("css"), s["in_stock"].get("regex"))
            rows.append({
                "name": s["name"],
                "url": s["url"],
                "price_raw": price_raw or "",
                "in_stock_raw": stock_raw or "",
                "currency": s.get("currency","")
            })
            time.sleep(1.0 + random.random())  # be polite
        except Exception as e:
            rows.append({
                "name": s["name"],
                "url": s["url"],
                "price_raw": f"ERROR: {e}",
                "in_stock_raw": "",
                "currency": s.get("currency","")
            })
    return rows

def write_report(rows: list[dict], out_dir: pathlib.Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"report_{ts}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name","url","price_raw","in_stock_raw","currency"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {path}")
    return path

def main():
    cfg = json.loads(pathlib.Path("sites.json").read_text(encoding="utf-8"))
    rows = monitor_once(cfg)
    write_report(rows, pathlib.Path("reports"))

if __name__ == "__main__":
    main()
