ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
DB_PATH  = DATA_DIR / "knowledge.db"

EMBED_MODEL = "all-MiniLM-L6-v2" 
LLM_ALIAS="qwen2.5-0.5b" 

TOP_K = 3 
CHUNK_MAX_CHARS = 800 