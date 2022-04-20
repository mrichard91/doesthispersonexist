from typing import Optional, Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import aiohttp

from gan_detector import scan_data
import json

class ScanRequest(BaseModel):
    url: Optional[str]
    data: Optional[str]

class ScanResponse(BaseModel):
    status: str
    error: Optional[str]
    results: Optional[Dict[str, Any]]

app = FastAPI()

async def fetch_url(url: str):
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        if r.status == 200:
            data = await r.content.read()
            return data

@app.post('/scan_url', response_model=ScanResponse)
async def url_scan(scan_request: ScanRequest) -> ScanResponse:
    if scan_request.url:
        url_data = await fetch_url(scan_request.url)
        results = scan_data(url_data)
    elif scan_request.data:
        data = base64.b64decode(scan_request.data.split(',')[1])
        results = scan_data(data)
    return {"status": "ok", "results": results}

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)