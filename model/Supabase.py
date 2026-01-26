import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"), # type: ignore
    os.environ.get("SUPABASE_KEY") # type: ignore
)

## print(supabase.table("novel").select("*").execute())