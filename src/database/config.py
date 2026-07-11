import os

from dotenv import load_dotenv
from supabase import create_client, Client

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL not found in .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY not found in .env")

# ==========================================
# Create Supabase Client
# ==========================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)