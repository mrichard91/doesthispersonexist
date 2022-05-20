from typing import Optional, Dict, Any, List
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import aiohttp
import asyncio

from gan_detector import scan_data
import json

class ScanRequest(BaseModel):
    url: Optional[str]
    data: Optional[str]

class ScanResponse(BaseModel):
    status: str
    error: Optional[str]
    results: Optional[Dict[str, Any]]

class ScanMultipleRequest(BaseModel):
    url: List[str]

class ScanMultipleResponse(BaseModel):
    status: str
    error: Optional[List[str]]
    results: Optional[Dict[str, Any]]

app = FastAPI()

async def fetch_url(url: str, session: aiohttp.ClientSession = None):
    if session:
        r = await session.get(url)
        if r.status == 200:
            data = await r.content.read()
            return data
    else:
        async with aiohttp.ClientSession() as session:
            r = await session.get(url)
            if r.status == 200:
                data = await r.content.read()
                return data

@app.post('/scan_urls', response_model=ScanResponse)
async def url_scans(scan_request: ScanRequest) -> ScanResponse:
    urls = scan_request.urls
    async with aiohttp.ClientSession() as session:

        async def fetch_scan(url):
            data = await fetch_url(url, session)
            return scan_data(data)

        futures = [fetch_scan(url) for url in urls]
        results = await asyncio.gather(*futures)
    final_results = {
        url:result
        for url, result in zip(urls, results)
    }
    return {"status": "ok", "results": final_results}

@app.post('/scan_url', response_model=ScanResponse)
async def url_scan(scan_request: ScanRequest) -> ScanResponse:
    if scan_request.url:
        url_data = await fetch_url(scan_request.url)
        results = scan_data(url_data)
    elif scan_request.data:
        if scan_request.data.startswith('data'):
            data = base64.b64decode(scan_request.data.split(',')[1])
        else:
            data = base64.b64decode(scan_request.data)
        results = scan_data(data)
    return {"status": "ok", "results": results}

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)