import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from app.utils.date_helper import get_day_name

async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200 or "404.html" in str(response.url):
                return None
            return await response.text()
    except:
        return None

async def fetch_all_htmls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def process_page(html, url, date_str):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        result = {"gdb": 0, "date": "", "dayName": "", "url": url}

        if gdb_el := soup.select_one('.v-gdb'):
            text = gdb_el.get_text().strip()
            if text[-2:].isdigit():
                result["gdb"] = int(text[-2:])

        if link := soup.select_one('.vietlott-link:last-child'):
            if href := link.get("href"):
                parts = urlparse(href).path.split('-')
                if len(parts) >= 3:
                    day, month, year = map(int, [parts[-3], parts[-2], parts[-1].replace('.html', '')])
                    date_obj = datetime(year, month, day)
                    result["dayName"] = get_day_name(date_obj)
                    result["date"] = f"{day}-{month}"
        return result if result["date"] else None
    except:
        return None

async def process_all_pages(htmls, urls, dates):
    tasks = [
        process_page(html, url, date)
        for html, url, date in zip(htmls, urls, dates) if html
    ]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r]
