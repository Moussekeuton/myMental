from database import SupabaseClient
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import streamlit as st

class CleaningTaskManager:
    def __init__(self):
        self.db = SupabaseClient().get_client()
    
    def create_task(self, task_name: str, assigned_to: str, room: str, frequency: str, description: str = "", due_date: date = None) -> bool:
        """Create a new cleaning task"""
        try:
            task_data = {
                "task_name": task_name,
                "assigned_to": assigned_to,
                "room": room,
                "frequency": frequency,
                "description": description,
                "due_date": due_date.isoformat() if due_date else None,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "completed_at": None
            }
            
            result = self.db.table("cleaning_tasks").insert(task_data).execute()
            return True
        except Exception as e:
            st.error(f"Error creating task: {str(e)}")
            return False
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all cleaning tasks"""
        try:
            result = self.db.table("cleaning_tasks").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            st.error(f"Error fetching tasks: {str(e)}")
            return []
    
    def get_tasks_by_person(self, person: str) -> List[Dict]:
        """Get tasks assigned to a specific person"""
        try:
            result = self.db.table("cleaning_tasks").select("*").eq("assigned_to", person).order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            st.error(f"Error fetching tasks for {person}: {str(e)}")
            return []
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks"""
        try:
            result = self.db.table("cleaning_tasks").select("*").eq("status", "pending").order("due_date").execute()
            return result.data
        except Exception as e:
            st.error(f"Error fetching pending tasks: {str(e)}")
            return []
    
    def complete_and_rotate_task(self, task_id: int) -> bool:
        """Mark a task as done and rotate assignment for next week"""
        try:
            # First get the current task
            task_result = self.db.table("cleaning_tasks").select("*").eq("id", task_id).execute()
            if not task_result.data:
                return False
            
            task = task_result.data[0]
            current_assignee = task['assigned_to']
            
            # Rotate assignment
            new_assignee = "Yvonne" if current_assignee == "Fernand" else "Fernand"
            
            # Update task: mark as completed and rotate assignment
            result = self.db.table("cleaning_tasks").update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "assigned_to": new_assignee
            }).eq("id", task_id).execute()
            
            # Immediately reset to pending for the new assignee
            reset_result = self.db.table("cleaning_tasks").update({
                "status": "pending",
                "completed_at": None
            }).eq("id", task_id).execute()
            
            return True
        except Exception as e:
            st.error(f"Error rotating task: {str(e)}")
            return False
    
    def reset_task(self, task_id: int) -> bool:
        """Reset a completed task back to pending"""
        try:
            result = self.db.table("cleaning_tasks").update({
                "status": "pending",
                "completed_at": None
            }).eq("id", task_id).execute()
            return True
        except Exception as e:
            st.error(f"Error resetting task: {str(e)}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            result = self.db.table("cleaning_tasks").delete().eq("id", task_id).execute()
            return True
        except Exception as e:
            st.error(f"Error deleting task: {str(e)}")
            return False
    
    def update_task(self, task_id: int, updates: Dict) -> bool:
        """Update a task"""
        try:
            result = self.db.table("cleaning_tasks").update(updates).eq("id", task_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating task: {str(e)}")
            return False
    
    def get_completed_tasks_this_week(self) -> List[Dict]:
        """Get tasks completed this week"""
        try:
            # Calculate start of week (Monday)
            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            
            result = self.db.table("cleaning_tasks").select("*").eq("status", "completed").gte("completed_at", start_of_week.isoformat()).execute()
            return result.data
        except Exception as e:
            st.error(f"Error fetching completed tasks: {str(e)}")
            return []