#!/usr/bin/env python3
"""Test script for Supabase connection"""

from database import SupabaseClient

try:
    print('Testing database connection with latest Supabase and modern API key...')
    client = SupabaseClient()
    supabase = client.get_client()
    print('✅ Connected to Supabase successfully!')
    
    # Test table access
    result = supabase.table('cleaning_tasks').select('*').limit(1).execute()
    print('✅ Table exists and accessible!')
    print(f'Records found: {len(result.data)}')
    
    if len(result.data) == 0:
        print('✅ Table is empty - ready for new tasks!')
    else:
        print('Sample record:', result.data[0])
        
except Exception as e:
    print(f'❌ Error: {str(e)}')
    if 'relation "public.cleaning_tasks" does not exist' in str(e) or 'does not exist' in str(e).lower():
        print('📋 The cleaning_tasks table needs to be created first.')
        print('Create it in your Supabase SQL Editor with this command:')
        print('''
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
);''')
    else:
        print('Please check your Supabase credentials and connection.')