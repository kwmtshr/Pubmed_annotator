import json
import re
import time
import traceback

from ratelimit import limits, sleep_and_retry
from openai import OpenAI

from .config import ENG_KEYS, OPENAI_API_KEY, MAX_RETRIES, SUMMARY_SLEEP
from .utils import clean_json

client = OpenAI(api_key=OPENAI_API_KEY)

@limits(calls=3500, period=60)
@sleep_and_retry
def call_openai(messages):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )

def summarize_batch(pmids, abstracts):
    skeleton = {pm: {k: "" for k in ENG_KEYS} for pm in pmids}
    example = json.dumps(skeleton, ensure_ascii=False, indent=2)

    prompt = (
        "You are a genius who can explain things concisely. "
        "For each abstract below, provide a JSON object with the following English keys: "
        f"{ENG_KEYS}.\n\n"
        "Output only JSON. Here is the structure example:\n"
        + example + "\n\n"
        "Now analyze these abstracts:\n"
    )
    for pm in pmids:
        prompt += f"PMID:{pm}\nAbstract:{abstracts.get(pm,'')}\n\n"

    messages = [
        {"role": "system", "content": "You are a genius who can explain things concisely."},
        {"role": "user",   "content": prompt}
    ]

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            res = call_openai(messages)
            print(f"[debug] OpenAI reply (truncated): {res.choices[0].message.content[:200]!r}")

            txt = res.choices[0].message.content
            m = re.search(r'^\{[\s\S]*\}$', txt, flags=re.M)
            if not m:
                raise ValueError("no JSON block in reply")

            js = clean_json(m.group(0))
            data = json.loads(js)
            print(f"[debug] Parsed PMIDs: {list(data.keys())[:5]}")
            return data

        except Exception as e:
            print(f"[debug] summarizer attempt {attempt} failed: {e}")
            traceback.print_exc()
            time.sleep(2 ** attempt)
        finally:
            time.sleep(SUMMARY_SLEEP)

    return {pm: {k: "unknown" for k in ENG_KEYS} for pm in pmids}
