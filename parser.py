from datetime import date, datetime
from typing import List, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_page_links(
    html: str, start_date: date, end_date: date, base_url: str
) -> List[Tuple[str, date]]:
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    PREFIX = "/upload/reports/oil_xls/oil_xls_"
    results: List[Tuple[str, date]] = []

    for link in links:
        parts = (link.get("href") or "").split("?")
        href, tail = parts[0].strip(), parts[1] if len(parts) > 1 else None
        if not (href.startswith(PREFIX) or PREFIX in href) or not href.endswith(".xls"):
            continue

        try:
            date_str = href.split("oil_xls_")[1][:8]
            file_date = datetime.strptime(date_str, "%Y%m%d").date()
        except Exception:
            continue

        if not (start_date <= file_date <= end_date):
            continue

        full_url = urljoin(base_url, href)
        if tail:
            full_url = f"{full_url}?{tail}"
        results.append((full_url, file_date))

    return results
