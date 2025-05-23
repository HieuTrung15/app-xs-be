from app.utils.date_helper import generate_dates
from app.utils.fetcher import fetch_all_htmls, process_all_pages
from app.cache.simple_cache import get_cache, set_cache
from datetime import datetime

CACHE_KEY = "gdb_data"
CACHE_TIMEOUT = 300  # seconds

async def get_gdb_data():
    cached = get_cache(CACHE_KEY)
    if cached:
        return {**cached, "cached": True}

    dates = generate_dates()
    urls = [f"https://xsmn.mobi/xsmb-{date}.html" for date in dates]
    html_pages = await fetch_all_htmls(urls)
    data = await process_all_pages(html_pages, urls, dates)

    if not data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu phù hợp")

    response = {
        "data": data,
        "count": len(data),
        "success": True,
        "cached": False
    }
    set_cache(CACHE_KEY, response, timeout=CACHE_TIMEOUT)
    return response
