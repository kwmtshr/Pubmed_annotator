import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
NCBI_API_KEY    = os.getenv("NCBI_API_KEY")

INPUT_CSV   = Path(os.getenv("INPUT_CSV", "./data/src/pubmed_data.csv"))
OUTPUT_CSV  = Path(os.getenv("OUTPUT_CSV", "./data/src/pubmed_annotated.csv"))

BASE_URL         = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DB               = "pubmed"
RETMODE          = "xml"
DELAY            = 0.12 if NCBI_API_KEY else 0.34
PM_FETCH_BATCH   = int(os.getenv("PM_FETCH_BATCH", 200))
MAX_FETCH_WORKERS= int(os.getenv("MAX_FETCH_WORKERS", 10))

ENG_KEYS             = ["Known", "Research Question", "Methods", "Findings", "Limitations"]
SUMMARY_BATCH_SIZE   = int(os.getenv("SUMMARY_BATCH_SIZE", 20))
MAX_SUMMARY_WORKERS  = int(os.getenv("MAX_SUMMARY_WORKERS", 10))
SUMMARY_SLEEP        = float(os.getenv("SUMMARY_SLEEP", 1.0))
MAX_RETRIES          = int(os.getenv("MAX_RETRIES", 3))
