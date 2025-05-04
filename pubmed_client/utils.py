import re

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def clean_json(s: str) -> str:
    return re.sub(r',(\s*[}\]])', r'\1', s).strip()
