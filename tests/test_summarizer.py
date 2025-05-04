import pytest
from pubmed_client.summarizer import summarize_batch, call_openai

def test_summarize_batch_fallback(monkeypatch):
    # call_openai
    monkeypatch.setattr("pubmed_client.summarizer.call_openai", lambda *_: (_ for _ in ()).throw(Exception))
    result = summarize_batch(["1","2"], {"1":"", "2":""})
    assert result["1"]["Known"] == "unknown"
    assert result["2"]["Limitations"] == "unknown"
