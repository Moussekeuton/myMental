from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and KEY must be set in environment variables")
        
        # Create client with latest version
        self.supabase: Client = create_client(self.url, self.key)
    
    def get_client(self):
        return self.supabase