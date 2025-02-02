import requests
from bs4 import BeautifulSoup
import aiohttp
from typing import List, Optional,Dict



def get_bs_html(url, headers: Optional[Dict[str, str]] = None) -> BeautifulSoup:
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to get {url}. Status code: {response.status_code}")
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs

async def aget_bs_html(url, headers: Optional[Dict[str, str]] = None)-> BeautifulSoup:
    with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ConnectionError(f"Failed to get {url}. Status code: {response.status}")
            bs = BeautifulSoup(await response.text(), 'html.parser')
            return bs
            