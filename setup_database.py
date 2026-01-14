"""
Database setup script for Cleaning Task Manager
Run this script to create the required table in your Supabase database.
"""

from database import SupabaseClient
import streamlit as st

def create_table():
    """Create the cleaning_tasks table in Supabase"""
    
    # SQL to create the table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cleaning_tasks (
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
    """
    
    try:
        # Initialize Supabase client
        db = SupabaseClient().get_client()
        
        # Execute the SQL
        result = db.rpc('exec_sql', {'sql': create_table_sql}).execute()
        
        print("✅ Table 'cleaning_tasks' created successfully!")
        
        # Add some sample data
        sample_tasks = [
            {
                "task_name": "Vacuum living room",
                "assigned_to": "Husband",
                "room": "Living Room",
                "frequency": "Weekly",
                "description": "Vacuum carpets and under furniture",
                "status": "pending",
                "due_date": "2026-01-20"
            },
            {
                "task_name": "Clean bathroom",
                "assigned_to": "Wife",
                "room": "Bathroom",
                "frequency": "Weekly",
                "description": "Deep clean toilet, shower, and sink",
                "status": "pending",
                "due_date": "2026-01-18"
            },
            {
                "task_name": "Wash dishes",
                "assigned_to": "Husband",
                "room": "Kitchen",
                "frequency": "Daily",
                "description": "Clean all dishes and utensils",
                "status": "completed",
                "completed_at": "2026-01-13T10:30:00"
            }
        ]
        
        # Insert sample tasks
        result = db.table("cleaning_tasks").insert(sample_tasks).execute()
        print("✅ Sample tasks added successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {str(e)}")
        print("\nPlease create the table manually using the SQL Editor in Supabase:")
        print(create_table_sql)
        return False

def verify_setup():
    """Verify that the database setup is working"""
    try:
        db = SupabaseClient().get_client()
        result = db.table("cleaning_tasks").select("*").limit(1).execute()
        print("✅ Database connection and table verified!")
        return True
    except Exception as e:
        print(f"❌ Database verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🏠 Cleaning Task Manager - Database Setup")
    print("=" * 50)
    
    # Check if .env file is configured
    try:
        db_client = SupabaseClient()
        print("✅ Environment variables loaded successfully")
    except ValueError as e:
        print(f"❌ {str(e)}")
        print("\nPlease update your .env file with the correct Supabase credentials")
        exit(1)
    
    # Create table and add sample data
    if create_table():
        print("\n🎉 Database setup completed!")
        print("You can now run the main application with: streamlit run app.py")
    else:
        print("\n💡 Manual setup required. Please check the instructions in README.md")
        
    # Verify setup
    print("\nVerifying setup...")
    verify_setup()