# 🏠 Mental Load Manager

A Streamlit web application for couples to manage recurring household tasks and mental load efficiently using Supabase as the backend database. Perfect for tracking whose turn it is for recurring chores like cleaning the cat litter, taking out trash, or other household responsibilities.

## ✨ Features

- **📋 This Week's View**: See whose turn it is for each recurring task
- **🔄 Automatic Rotation**: When a task is marked done, it automatically switches to the other person
- **➕ Recurring Task Setup**: Create permanent tasks that don't disappear when completed
- **✅ Mental Load Management**: Focus on whose turn rather than one-time completion
- **👥 Couple-Focused**: Designed specifically for Fernand & Yvonne (easily customizable)
- **🏠 Location Organization**: Categorize tasks by different areas of your home
- **📅 Due Date Tracking**: Optional reminders for time-sensitive tasks
- **🔄 Frequency Management**: Set how often tasks need attention

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- A Supabase account (free tier available)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Supabase Database

1. Create a free account at [Supabase](https://supabase.com)
2. Create a new project
3. Go to the SQL Editor and run this query to create the required table:

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

### 3. Configure Environment Variables

1. Copy your Supabase URL and anon key from your project settings
2. Update the `.env` file:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📱 Usage Guide

### Adding Tasks
1. Navigate to "➕ Add Task"
2. Fill in the task details:
   - **Task Name**: What needs to be done (e.g., "Vacuum living room")
   - **Assign to**: Choose between Husband or Wife
   - **Room**: Select the relevant room
   - **Frequency**: How often the task should be done
   - **Due Date**: Optional deadline
   - **Description**: Additional details

### Managing Tasks
1. Go to "✅ Manage Tasks"
2. Use filters to find specific tasks
3. Complete tasks by clicking the ✅ button
4. Edit or delete tasks as needed

### Viewing Statistics
- Check the "📊 Statistics" page for visual insights
- See task distribution by person, room, and frequency
- Track completion rates and overdue tasks

## 🏗️ Project Structure

```
myMental/
├── app.py                 # Main Streamlit application
├── task_manager.py        # Database operations and business logic
├── database.py           # Supabase client configuration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Customization

### Adding More Users
Currently set up for couples (Husband/Wife), but you can easily modify the user options in the `assigned_to` selectbox in `app.py`.

### Adding More Rooms
Modify the room options in the selectbox to match your home layout.

### Custom Frequencies
Adjust the frequency options to match your cleaning schedule preferences.

## 🎨 Features in Detail

### Dashboard
- Real-time statistics cards
- Upcoming task notifications
- Recent completion history
- Overdue task warnings

### Task Management
- Bulk operations with filters
- In-line editing capabilities
- Status tracking (Pending/Completed)
- Smart due date highlighting

### Statistics & Analytics
- Task distribution charts
- Completion rate metrics
- Timeline visualizations
- Room-based analytics

## 🔒 Security Notes

- Keep your `.env` file secure and never commit it to version control
- The Supabase anon key is safe for frontend use but consider Row Level Security (RLS) for production use
- For enhanced security, you can implement user authentication through Supabase Auth

## 🐛 Troubleshooting

### Database Connection Issues
- Verify your Supabase URL and key are correct
- Check that the `cleaning_tasks` table exists
- Ensure your Supabase project is active

### Missing Dependencies
- Run `pip install -r requirements.txt` to install all required packages
- Make sure you're using Python 3.8 or higher

### Streamlit Issues
- Try refreshing the page if the app seems stuck
- Check the terminal for error messages
- Restart the Streamlit server: `Ctrl+C` then `streamlit run app.py`

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Happy cleaning! 🧹✨