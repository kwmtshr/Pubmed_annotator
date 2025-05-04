import pytest
import requests
from pubmed_client.fetcher import fetch_batch

class DummyResp:
    def __init__(self, code, text):
        self.status_code = code
        self.text = text

def test_fetch_batch_non_200(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kw: DummyResp(404, ""))
    assert fetch_batch(["123"]) == {}

def test_fetch_batch_success(monkeypatch):
    xml = """
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <PMID>123</PMID>
          <Abstract><AbstractText>Test</AbstractText></Abstract>
        </MedlineCitation>
      </PubmedArticle>
    </PubmedArticleSet>
    """
    monkeypatch.setattr(requests, "get", lambda *args, **kw: DummyResp(200, xml))
    out = fetch_batch(["123"])
    assert out["123"] == "Test"
