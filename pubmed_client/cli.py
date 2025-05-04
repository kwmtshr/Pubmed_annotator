#!/usr/bin/env python3
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .config import INPUT_CSV, OUTPUT_CSV, SUMMARY_BATCH_SIZE, MAX_SUMMARY_WORKERS, ENG_KEYS
from .io import read_input, write_output
from .utils import chunk_list
from .fetcher import fetch_abstracts
from .summarizer import summarize_batch

def main():
    parser = argparse.ArgumentParser(description="Fetch & summarize PubMed abstracts")
    parser.add_argument("-i", "--input",  default=INPUT_CSV,  help="INPUT CSV PATH")
    parser.add_argument("-o", "--output", default=OUTPUT_CSV, help="OUTPUT CSV PATH")
    args = parser.parse_args()

    df = read_input(args.input)
    pmids = df["PMID"].str.replace(r"\D","",regex=True).tolist()
    non_empty = [p for p in pmids if p]
    print(f"[debug] total PMIDs: {len(pmids)}, non-empty: {len(non_empty)}")
    print(f"[debug] sample PMIDs: {non_empty[:5]}")

    abstracts = fetch_abstracts(pmids)
    print(f"[debug] fetched {len(abstracts)} abstracts")
    df["Abstract"] = df["PMID"].map(abstracts).fillna("")

    for key in ENG_KEYS:
        df[key] = ""

    batches = list(chunk_list(pmids, SUMMARY_BATCH_SIZE))
    with ThreadPoolExecutor(max_workers=MAX_SUMMARY_WORKERS) as ex:
        futures = {ex.submit(summarize_batch, b, abstracts): b for b in batches}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Summarizing"):
            out = fut.result()
            for pm, summary in out.items():
                for k, v in summary.items():
                    df.loc[df["PMID"]==pm, k] = v

    write_output(df, args.output)

if __name__ == "__main__":
    main()
