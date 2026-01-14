#!/usr/bin/env python3
"""Add sample mental load tasks"""

from database import SupabaseClient

try:
    print('Adding sample mental load tasks...')
    client = SupabaseClient()
    supabase = client.get_client()
    
    # Sample mental load tasks
    sample_tasks = [
        {
            "task_name": "Clean Aro's litter box",
            "assigned_to": "Fernand",
            "room": "Bathroom",
            "frequency": "Weekly",
            "description": "Clean and refill the cat litter for our beloved Aro",
            "status": "pending",
            "due_date": "2026-01-20"
        },
        {
            "task_name": "Take out trash & recycling",
            "assigned_to": "Yvonne",
            "room": "Kitchen", 
            "frequency": "Weekly",
            "description": "Empty all bins and take to curb on collection day",
            "status": "pending",
            "due_date": "2026-01-19"
        },
        {
            "task_name": "Vacuum living room",
            "assigned_to": "Fernand",
            "room": "Living Room",
            "frequency": "Bi-weekly", 
            "description": "Deep vacuum including under furniture",
            "status": "pending"
        },
        {
            "task_name": "Clean bathroom thoroughly",
            "assigned_to": "Yvonne",
            "room": "Bathroom",
            "frequency": "Monthly",
            "description": "Deep clean toilet, shower, sink, and floor",
            "status": "pending"
        }
    ]
    
    # Insert sample tasks
    result = supabase.table("cleaning_tasks").insert(sample_tasks).execute()
    print(f'✅ Added {len(sample_tasks)} sample mental load tasks!')
    
    # Show current tasks
    all_tasks = supabase.table("cleaning_tasks").select("*").execute()
    print(f'📋 Total tasks in database: {len(all_tasks.data)}')
    
    for task in all_tasks.data:
        print(f"  • {task['task_name']} - {task['assigned_to']} ({task['frequency']})")
        
except Exception as e:
    print(f'❌ Error: {str(e)}')