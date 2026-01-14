"""
Simple setup script to create the cleaning_tasks table
Run this after updating your .env file with the correct Supabase credentials
"""

from supabase import create_client
import os
from dotenv import load_dotenv

def setup_database():
    # Load environment variables
    load_dotenv()
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key or 'YOUR_FULL_ANON_KEY_HERE' in key:
        print("❌ Please update your .env file with the correct Supabase credentials first!")
        print("Get your credentials from: https://app.supabase.com > Your Project > Settings > API")
        return False
    
    try:
        print("🔄 Connecting to Supabase...")
        supabase = create_client(url, key)
        print("✅ Connected successfully!")
        
        # Check if table exists
        try:
            result = supabase.table('cleaning_tasks').select('*').limit(1).execute()
            print("✅ Table 'cleaning_tasks' already exists!")
            return True
        except Exception as e:
            if 'does not exist' in str(e):
                print("❌ Table doesn't exist. Please create it manually.")
                print("\n📋 Go to your Supabase Dashboard > SQL Editor and run this:")
                print("""
CREATE TABLE cleaning_tasks (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    assigned_to VARCHAR(50) NOT NULL,
    room VARCHAR(100) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    due_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
                """)
                return False
            else:
                raise e
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🏠 Cleaning Task Manager - Database Setup")
    print("=" * 50)
    
    if setup_database():
        print("\n🎉 Setup completed! You can now run:")
        print("streamlit run app.py")
    else:
        print("\n💡 Please follow the instructions above to complete setup.")