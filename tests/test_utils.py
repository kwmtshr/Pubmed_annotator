import pytest
from pubmed_client.utils import chunk_list, clean_json

def test_chunk_list():
    data = list(range(7))
    chunks = list(chunk_list(data, 3))
    assert chunks == [[0,1,2],[3,4,5],[6]]

def test_clean_json():
    raw = '{"a":1,}' # Trailing comma
    assert clean_json(raw) == '{"a":1}'
