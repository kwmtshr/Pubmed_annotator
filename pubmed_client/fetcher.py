import time
import xml.etree.ElementTree as ET
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import BASE_URL, DB, RETMODE, NCBI_API_KEY, DELAY, PM_FETCH_BATCH, MAX_FETCH_WORKERS
from .utils import chunk_list

def fetch_batch(batch):
    params = {"db": DB, "retmode": RETMODE, "id": ",".join(batch)}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    resp = requests.get(BASE_URL, params=params, timeout=10)
    time.sleep(DELAY)
    if resp.status_code != 200:
        print(f"[debug] fetch_batch failed: status={resp.status_code}, ids={batch[:5]}...")

    out = {}
    if resp.status_code == 200:
        root = ET.fromstring(resp.text)
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//PMID", "").strip()
            texts = [n.text or "" for n in art.findall(".//AbstractText")]
            out[pmid] = "\n".join(texts).strip()
    else:
        print(f"[debug] response body snippet: {resp.text[:200]}")
    return out

def fetch_abstracts(pmids, max_workers=MAX_FETCH_WORKERS):
    abstracts = {}
    batches = list(chunk_list(pmids, PM_FETCH_BATCH))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(fetch_batch, b): b for b in batches}
        for fut in as_completed(futures):
            abstracts.update(fut.result() or {})
    return abstracts
