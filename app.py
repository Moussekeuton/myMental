import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
from task_manager import CleaningTaskManager

# Page configuration
st.set_page_config(
    page_title="🏠 Mental Load Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #2E86AB;
        border-bottom: 2px solid #A23B72;
        margin-bottom: 2rem;
    }
    .task-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .completed-task {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .overdue-task {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .stats-card {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the task manager
@st.cache_resource
def init_task_manager():
    try:
        return CleaningTaskManager()
    except ValueError as e:
        st.error(f"Database connection error: {str(e)}")
        st.info("Please check your Supabase credentials in the .env file")
        st.stop()

def main():
    st.markdown('<h1 class="main-header">🏠 Mental Load Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Track whose turn it is for recurring household tasks</p>', unsafe_allow_html=True)

    try:
        task_manager = init_task_manager()
    except:
        st.error("Failed to initialize task manager. Please check your database connection.")
        return

    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📋 This Week", "➕ Add Task", "✅ Manage Tasks", "📊 Statistics", "⚙️ Settings"]
    )

    if page == "📋 This Week":
        show_dashboard(task_manager)
    elif page == "➕ Add Task":
        show_add_task(task_manager)
    elif page == "✅ Manage Tasks":
        show_manage_tasks(task_manager)
    elif page == "📊 Statistics":
        show_statistics(task_manager)
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard(task_manager):
    # Calculate current week info
    today = date.today()
    # Get Monday of current week (ISO week starts on Monday)
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    week_number = today.isocalendar()[1]
    
    st.header("📋 This Week's Tasks")
    st.subheader(f"🗓️ Week {week_number} ({monday.strftime('%B %d')} - {sunday.strftime('%B %d, %Y')})")
    
    # Get task data
    all_tasks = task_manager.get_all_tasks()
    pending_tasks = [task for task in all_tasks if task['status'] == 'pending']
    completed_tasks = [task for task in all_tasks if task['status'] == 'completed']
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fernand_tasks = len([task for task in pending_tasks if task['assigned_to'] == 'Fernand'])
        st.markdown(f'''
        <div class="stats-card">
            <h3>👨</h3>
            <h2>{fernand_tasks}</h2>
            <p>Fernand's Tasks</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        yvonne_tasks = len([task for task in pending_tasks if task['assigned_to'] == 'Yvonne'])
        st.markdown(f'''
        <div class="stats-card">
            <h3>👩</h3>
            <h2>{yvonne_tasks}</h2>
            <p>Yvonne's Tasks</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <h3>📝</h3>
            <h2>{len(pending_tasks)}</h2>
            <p>Total Pending</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        total_tasks = len(all_tasks)
        completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        st.markdown(f'''
        <div class="stats-card">
            <h3>📈</h3>
            <h2>{completion_rate:.0f}%</h2>
            <p>Done This Period</p>
        </div>
        ''', unsafe_allow_html=True)

    # Current assignments in sheet format
    st.subheader("📋 Current Task Assignments")
    
    if pending_tasks:
        # Create a table-like display
        for task in pending_tasks:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 1.5, 1.5])
            
            with col1:
                st.markdown(f"**{task['task_name']}**")
                if task['description']:
                    st.caption(f"💡 {task['description']}")
            
            with col2:
                st.text(f"📍 {task['room']}")
                st.caption(f"🔄 {task['frequency']}")
            
            with col3:
                current_person = task['assigned_to']
                st.markdown(f"**👤 {current_person}**")
                
            with col4:
                next_person = "Yvonne" if current_person == "Fernand" else "Fernand"
                st.caption(f"Next: {next_person}")
            
            with col5:
                if st.button("✅ Done", key=f"done_{task['id']}", type="primary"):
                    if task_manager.complete_and_rotate_task(task['id']):
                        st.success(f"Task rotated to {next_person}!")
                        st.experimental_rerun()
            
            st.divider()
    else:
        st.info("No pending tasks! Add some recurring tasks to get started.")

def show_add_task(task_manager):
    st.header("➕ Add New Recurring Task")
    st.info("💡 These are recurring mental load tasks that rotate between Fernand and Yvonne each time they're completed.")
    
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name*", placeholder="e.g., Clean Aro's litter box")
            assigned_to = st.selectbox("Currently assigned to*", ["Fernand", "Yvonne"])
            room = st.selectbox("Location*", [
                "Living Room", "Kitchen", "Bedroom", "Bathroom", "Dining Room", 
                "Office", "Laundry Room", "Garage", "Garden", "Other"
            ])
        
        with col2:
            frequency = st.selectbox("How often*", [
                "Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"
            ])
            description = st.text_area("Notes (optional)", 
                                     placeholder="Any specific instructions or reminders...")
        
        submitted = st.form_submit_button("➕ Add Recurring Task", type="primary")
        
        if submitted:
            if task_name and assigned_to and room and frequency:
                if task_manager.create_task(task_name, assigned_to, room, frequency, description, None):
                    st.success(f"✅ Recurring task '{task_name}' added! Currently assigned to {assigned_to}.")
                    st.balloons()
                else:
                    st.error("Failed to add task. Please try again.")
            else:
                st.error("Please fill in all required fields marked with *")

def show_manage_tasks(task_manager):
    st.header("✅ Manage Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_person = st.selectbox("Filter by Person", ["All", "Fernand", "Yvonne"])
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    with col3:
        filter_room = st.selectbox("Filter by Room", ["All", "Living Room", "Kitchen", "Bedroom", "Bathroom", "Dining Room", "Office", "Laundry Room", "Garage", "Garden", "Other"])
    
    # Get and filter tasks
    all_tasks = task_manager.get_all_tasks()
    
    # Apply filters
    filtered_tasks = all_tasks
    if filter_person != "All":
        filtered_tasks = [task for task in filtered_tasks if task['assigned_to'] == filter_person]
    if filter_status != "All":
        status = filter_status.lower()
        filtered_tasks = [task for task in filtered_tasks if task['status'] == status]
    if filter_room != "All":
        filtered_tasks = [task for task in filtered_tasks if task['room'] == filter_room]
    
    st.subheader(f"Tasks ({len(filtered_tasks)} found)")
    
    if filtered_tasks:
        for task in filtered_tasks:
            # Determine card styling based on task status
            card_class = "task-card"
            if task['status'] == 'completed':
                card_class += " completed-task"
            
            # Create task card
            with st.container():
                st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    status_icon = "✅" if task['status'] == 'completed' else "📝"
                    st.markdown(f"**{status_icon} {task['task_name']}**")
                    current_assignee = task['assigned_to']
                    next_assignee = "Yvonne" if current_assignee == "Fernand" else "Fernand"
                    st.text(f"👤 {task['assigned_to']} | 🏠 {task['room']} | 🔄 {task['frequency']}")
                    if task['status'] == 'pending':
                        st.caption(f"🔄 Next turn: {next_assignee}")
                    if task['description']:
                        st.caption(task['description'])
                
                with col2:
                    if task['status'] == 'pending':
                        if st.button("✅ Mark Done", key=f"complete_{task['id']}", type="primary"):
                            # For recurring tasks, we mark as done and switch assignment
                            if task_manager.complete_and_rotate_task(task['id']):
                                st.success("Task marked done! Assignment rotated for next week.")
                                st.experimental_rerun()
                    else:
                        if st.button("🔄 Reset", key=f"reset_{task['id']}", type="secondary"):
                            if task_manager.reset_task(task['id']):
                                st.success("Task reset to pending!")
                                st.experimental_rerun()
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{task['id']}"):
                        st.session_state[f"editing_{task['id']}"] = True
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{task['id']}", type="secondary"):
                        if task_manager.delete_task(task['id']):
                            st.success("Task deleted!")
                            st.experimental_rerun()
                
                # Editing form (appears when edit button is clicked)
                if st.session_state.get(f"editing_{task['id']}", False):
                    st.divider()
                    with st.form(f"edit_form_{task['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_task_name = st.text_input("Task Name", value=task['task_name'])
                            new_assigned_to = st.selectbox("Currently assigned to", ["Fernand", "Yvonne"], 
                                                         index=0 if task['assigned_to'] == "Fernand" else 1)
                            new_room = st.selectbox("Room", [
                                "Living Room", "Kitchen", "Bedroom", "Bathroom", "Dining Room", 
                                "Office", "Laundry Room", "Garage", "Garden", "Other"
                            ], index=["Living Room", "Kitchen", "Bedroom", "Bathroom", "Dining Room", 
                                     "Office", "Laundry Room", "Garage", "Garden", "Other"].index(task['room']))
                        
                        with col2:
                            new_frequency = st.selectbox("Frequency", [
                                "Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"
                            ], index=["Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"].index(task['frequency']) if task['frequency'] in ["Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"] else 0)
                            
                            new_description = st.text_area("Description", value=task['description'] or "")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes", type="primary"):
                                updates = {
                                    "task_name": new_task_name,
                                    "assigned_to": new_assigned_to,
                                    "room": new_room,
                                    "frequency": new_frequency,
                                    "description": new_description
                                }
                                if task_manager.update_task(task['id'], updates):
                                    st.success("Task updated!")
                                    st.session_state[f"editing_{task['id']}"] = False
                                    st.experimental_rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"editing_{task['id']}"] = False
                                st.experimental_rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.divider()
    else:
        st.info("No tasks found matching your filters.")

def show_statistics(task_manager):
    st.header("📊 Task Statistics")
    
    all_tasks = task_manager.get_all_tasks()
    
    if not all_tasks:
        st.warning("No tasks available for statistics.")
        return
    
    df = pd.DataFrame(all_tasks)
    
    # Convert date columns
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['due_date'] = pd.to_datetime(df['due_date'])
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tasks by person
        st.subheader("📊 Tasks by Person")
        person_counts = df['assigned_to'].value_counts()
        fig_person = px.pie(values=person_counts.values, names=person_counts.index, 
                           title="Task Distribution by Person")
        st.plotly_chart(fig_person, use_container_width=True)
        
        # Tasks by status
        st.subheader("📈 Task Completion Status")
        status_counts = df['status'].value_counts()
        fig_status = px.bar(x=status_counts.index, y=status_counts.values, 
                           title="Tasks by Status")
        fig_status.update_layout(xaxis_title="Status", yaxis_title="Number of Tasks")
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Tasks by room
        st.subheader("🏠 Tasks by Room")
        room_counts = df['room'].value_counts()
        fig_room = px.bar(x=room_counts.values, y=room_counts.index, 
                         orientation='h', title="Tasks by Room")
        fig_room.update_layout(xaxis_title="Number of Tasks", yaxis_title="Room")
        st.plotly_chart(fig_room, use_container_width=True)
        
        # Tasks by frequency
        st.subheader("🔄 Tasks by Frequency")
        freq_counts = df['frequency'].value_counts()
        fig_freq = px.pie(values=freq_counts.values, names=freq_counts.index, 
                         title="Task Distribution by Frequency")
        st.plotly_chart(fig_freq, use_container_width=True)
    
    # Task completion timeline
    st.subheader("📅 Task Completion Timeline")
    completed_df = df[df['status'] == 'completed'].copy()
    if not completed_df.empty:
        completed_df['completed_date'] = completed_df['completed_at'].dt.date
        daily_completions = completed_df.groupby('completed_date').size().reset_index()
        daily_completions.columns = ['Date', 'Tasks Completed']
        
        fig_timeline = px.line(daily_completions, x='Date', y='Tasks Completed', 
                              title="Daily Task Completions")
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No completed tasks to show timeline.")
    
    # Summary statistics
    st.subheader("📋 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_tasks = len(df)
        completed_tasks = len(df[df['status'] == 'completed'])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col2:
        avg_tasks_per_person = df.groupby('assigned_to').size().mean()
        st.metric("Avg Tasks per Person", f"{avg_tasks_per_person:.1f}")
    
    with col3:
        overdue_tasks = len(df[(df['status'] == 'pending') & (df['due_date'] < datetime.now())])
        st.metric("Overdue Tasks", overdue_tasks)

def show_settings():
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Application Settings")
    
    # Database connection info
    st.subheader("🗄️ Database Connection")
    st.info("""
    **Database Setup Instructions:**
    
    1. **Create a Supabase project** at https://supabase.com
    2. **Create the following table** in your Supabase database:
    
    ```sql
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
    ```
    
    3. **Update your .env file** with your Supabase credentials:
       - SUPABASE_URL: Your project URL
       - SUPABASE_KEY: Your anon public key
    
    4. **Restart the application** after updating the .env file
    """)
    
    # App preferences
    st.subheader("👤 User Preferences")
    
    # You can add user-specific settings here
    st.selectbox("Default View", ["Dashboard", "Add Task", "Manage Tasks"])
    st.selectbox("Theme", ["Light", "Dark"])
    st.checkbox("Show notifications for overdue tasks")
    st.checkbox("Send daily summary emails")
    
    # Data management
    st.subheader("📊 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Completed Tasks", type="secondary"):
            st.warning("This will permanently delete all completed tasks. Are you sure?")
    
    with col2:
        if st.button("📤 Export All Data", type="secondary"):
            st.info("Data export functionality coming soon!")
    
    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **🏠 Cleaning Task Manager v1.0**
    
    A simple and efficient way to manage household cleaning tasks between couples.
    
    **Features:**
    - ✅ Task creation and management
    - 👥 Assignment to family members
    - 📅 Due date tracking
    - 📊 Progress statistics
    - 🏠 Room-based organization
    
    **Built with:** Streamlit + Supabase
    """)

if __name__ == "__main__":
    main()