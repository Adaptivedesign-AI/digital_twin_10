"""
Enhanced Digital Twin Monitoring Dashboard with Real-time Chat Viewing
Fixed for Gradio compatibility issues
"""

import gradio as gr
import json
import os
import datetime
import requests
from datetime import timedelta
from collections import Counter, defaultdict
import pandas as pd

# Try importing plotly, fallback if not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️ Plotly not available, charts will be disabled")

class EnhancedJSONMonitoringDashboard:
    def __init__(self):
        self.data_file = 'monitoring_data.json'
        self.github_enabled = self.setup_github()
        
    def setup_github(self):
        """Setup GitHub data sync"""
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.github_repo = os.environ.get("GITHUB_REPO")
        self.github_branch = os.environ.get("GITHUB_BRANCH", "main")
        
        enabled = bool(self.github_token and self.github_repo)
        if enabled:
            print(f"✅ GitHub sync enabled: {self.github_repo}")
        else:
            print("📁 Using local file only for monitoring")
        return enabled
    
    def load_data(self):
        """Load latest data with better error handling"""
        # Always try to download from GitHub first
        if self.github_enabled:
            download_success = self.download_from_github()
            if download_success:
                print("✅ Successfully downloaded fresh data from GitHub")
        
        # Load local data
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conv_count = len(data.get('conversations', []))
                    session_count = len(data.get('sessions', {}))
                    print(f"✅ Loaded data: {conv_count} conversations, {session_count} sessions")
                    return data
            except Exception as e:
                print(f"❌ Error loading data: {e}")
        
        # Return empty data
        print("⚠️ No data file found - returning empty structure")
        return {
            'sessions': {},
            'conversations': [],
            'user_actions': [],
            'system_metrics': [],
            'last_updated': datetime.datetime.now().isoformat()
        }
    
    def download_from_github(self):
        """Download latest data from GitHub with improved error handling"""
        if not self.github_enabled:
            return False
        
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{self.data_file}"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            print(f"🔄 Downloading from GitHub: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                content = response.json()
                import base64
                file_content = base64.b64decode(content['content']).decode('utf-8')
                
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                print("✅ Downloaded latest data from GitHub")
                return True
            elif response.status_code == 404:
                print("📁 No data file found in GitHub repository")
            else:
                print(f"⚠️ GitHub download failed: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"⚠️ Failed to download from GitHub: {e}")
        
        return False
    
    def get_recent_chat_conversations(self, limit=20):
        """Get most recent chat conversations for real-time viewing"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return [], "No conversation data available", []
        
        # Get all conversations and sort by timestamp (newest first)
        all_conversations = data['conversations']
        sorted_conversations = sorted(
            all_conversations, 
            key=lambda x: x['timestamp'], 
            reverse=True
        )
        
        # Take the most recent ones
        recent_conversations = sorted_conversations[:limit]
        
        # Format for display
        chat_data = []
        name_mapping = {
            "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
            "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
            "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
            "student010": "Tyler"
        }
        
        for conv in recent_conversations:
            timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%m-%d %H:%M')
            student_name = name_mapping.get(conv['student_id'], conv['student_id'])
            
            # Truncate messages for table view
            user_msg_short = conv['user_message'][:60] + ('...' if len(conv['user_message']) > 60 else '')
            ai_msg_short = conv['ai_response'][:60] + ('...' if len(conv['ai_response']) > 60 else '')
            
            chat_data.append([
                conv['id'],
                timestamp,
                student_name,
                user_msg_short,
                ai_msg_short,
                f"{conv.get('response_time_ms', 0)}ms"
            ])
        
        summary = f"📊 Showing {len(recent_conversations)} most recent conversations (Total: {len(all_conversations)})"
        
        # Also return raw data for detailed view
        return chat_data, summary, recent_conversations
    
    def get_chat_conversations_filtered(self, days=7, student_filter="", search_keyword="", limit=50):
        """Get detailed chat conversations with filtering"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return [], "No conversation data available"
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        # Filter conversations
        filtered_conversations = []
        for conv in data['conversations']:
            conv_date = datetime.datetime.fromisoformat(conv['timestamp'])
            
            # Date filter
            if conv_date < since_date:
                continue
            
            # Student filter
            if student_filter and student_filter != "All Students" and conv['student_id'] != student_filter:
                continue
            
            # Keyword search
            if search_keyword:
                search_text = f"{conv['user_message']} {conv['ai_response']}".lower()
                if search_keyword.lower() not in search_text:
                    continue
            
            filtered_conversations.append(conv)
        
        # Sort by timestamp (newest first)
        filtered_conversations.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Limit results
        limited_conversations = filtered_conversations[:limit]
        
        # Format for display
        chat_data = []
        name_mapping = {
            "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
            "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
            "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
            "student010": "Tyler"
        }
        
        for conv in limited_conversations:
            timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            student_name = name_mapping.get(conv['student_id'], conv['student_id'])
            
            chat_data.append([
                conv['id'],
                timestamp,
                student_name,
                conv['student_id'],
                conv['user_message'][:100] + ('...' if len(conv['user_message']) > 100 else ''),
                conv['ai_response'][:100] + ('...' if len(conv['ai_response']) > 100 else ''),
                conv.get('scene_context', 'No scene')[:50] + ('...' if len(conv.get('scene_context', '')) > 50 else ''),
                f"{conv.get('response_time_ms', 0)}ms"
            ])
        
        summary = f"Found {len(filtered_conversations)} conversations (showing {len(limited_conversations)})"
        return chat_data, summary
    
    def get_detailed_conversation_display(self, conversation_id, conversations_list=None):
        """Get conversation details formatted for display"""
        data = self.load_data()
        
        # First try from the passed list (for real-time view)
        if conversations_list:
            for conv in conversations_list:
                if conv['id'] == conversation_id:
                    return self._format_conversation_detail(conv)
        
        # Fallback to loading from data
        for conv in data.get('conversations', []):
            if conv['id'] == conversation_id:
                return self._format_conversation_detail(conv)
        
        return "❌ Conversation not found"
    
    def _format_conversation_detail(self, conv):
        """Format a single conversation for detailed view"""
        timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
        name_mapping = {
            "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
            "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
            "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
            "student010": "Tyler"
        }
        
        student_name = name_mapping.get(conv['student_id'], conv['student_id'])
        
        details = f"""
## 💬 Conversation Details (ID: {conv['id']})

**🕐 Time:** {timestamp}
**👤 Student:** {student_name} ({conv['student_id']})
**📍 Session ID:** {conv['session_id']}
**🎭 Scene Context:** {conv.get('scene_context', 'No scene context')}
**⏱️ Response Time:** {conv.get('response_time_ms', 0)}ms
**📏 Message Length:** {conv.get('message_length', len(conv['user_message']))} characters

---

### 👤 User Message:
{conv['user_message']}

---

### 🤖 AI Response:
{conv['ai_response']}

---
*💡 Click other conversation IDs in the table above to view more conversations*
        """
        
        return details
    
    def get_basic_stats(self, days=7):
        """Get basic statistics"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'avg_response_time': 0,
                'active_students': 0
            }
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        # Filter recent data
        recent_conversations = [
            conv for conv in data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) >= since_date
        ]
        
        recent_sessions = [
            session for session in data['sessions'].values()
            if datetime.datetime.fromisoformat(session['start_time']) >= since_date
        ]
        
        # Calculate statistics
        total_sessions = len(recent_sessions)
        total_messages = len(recent_conversations)
        
        response_times = [
            conv['response_time_ms'] for conv in recent_conversations
            if conv['response_time_ms'] > 0
        ]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        active_students = len(set(conv['student_id'] for conv in recent_conversations))
        
        return {
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'avg_response_time': avg_response_time,
            'active_students': active_students
        }
    
    def get_student_popularity_text(self, days=7):
        """Get student popularity as text (fallback when plotly unavailable)"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return "No conversation data available"
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        recent_conversations = [
            conv for conv in data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) >= since_date
        ]
        
        if not recent_conversations:
            return "No recent conversation data"
        
        student_counts = Counter(conv['student_id'] for conv in recent_conversations)
        
        name_mapping = {
            "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
            "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
            "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
            "student010": "Tyler"
        }
        
        text_result = "## 🎯 Student Popularity (Message Count)\n\n"
        for student_id, count in student_counts.most_common(10):
            student_name = name_mapping.get(student_id, student_id)
            text_result += f"**{student_name}:** {count} messages\n"
        
        return text_result
    
    def get_daily_usage_text(self, days=7):
        """Get daily usage as text (fallback when plotly unavailable)"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return "No conversation data available"
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        daily_data = defaultdict(lambda: {'message_count': 0, 'session_count': 0})
        processed_sessions = set()
        
        for conv in data['conversations']:
            conv_date = datetime.datetime.fromisoformat(conv['timestamp'])
            if conv_date >= since_date:
                date_str = conv_date.date().isoformat()
                daily_data[date_str]['message_count'] += 1
                
                # Count sessions (avoid duplicates)
                session_date_key = f"{conv['session_id']}_{date_str}"
                if session_date_key not in processed_sessions:
                    daily_data[date_str]['session_count'] += 1
                    processed_sessions.add(session_date_key)
        
        if not daily_data:
            return "No recent usage data"
        
        text_result = "## 📅 Daily Usage Trends\n\n"
        for date_str in sorted(daily_data.keys()):
            data_point = daily_data[date_str]
            text_result += f"**{date_str}:** {data_point['message_count']} messages, {data_point['session_count']} sessions\n"
        
        return text_result
    
    def export_conversations_to_csv(self, days=7, student_filter="", search_keyword=""):
        """Export conversations to CSV"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return None, "No conversation data to export"
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        # Filter and prepare data
        filtered_conversations = []
        for conv in data['conversations']:
            conv_date = datetime.datetime.fromisoformat(conv['timestamp'])
            
            if conv_date < since_date:
                continue
            
            if student_filter and student_filter != "All Students" and conv['student_id'] != student_filter:
                continue
            
            if search_keyword:
                search_text = f"{conv['user_message']} {conv['ai_response']}".lower()
                if search_keyword.lower() not in search_text:
                    continue
            
            filtered_conversations.append(conv)
        
        if not filtered_conversations:
            return None, "No conversations match the filter criteria"
        
        # Create DataFrame
        df = pd.DataFrame(filtered_conversations)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp', ascending=False)
        
        # Save to CSV
        filename = f"chat_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        return filename, f"✅ Exported {len(filtered_conversations)} conversations to {filename}"

def create_enhanced_monitoring_dashboard():
    """Create enhanced monitoring dashboard"""
    dashboard = EnhancedJSONMonitoringDashboard()
    
    # Store conversation data for real-time view
    recent_conversations_data = gr.State([])
    
    with gr.Blocks(title="Digital Twin Enhanced Monitoring") as demo:
        gr.Markdown("# 🔍 Digital Twin Enhanced Monitoring Dashboard")
        gr.Markdown("*Real-time monitoring of user behavior, conversation quality, and system performance*")
        
        with gr.Tabs():
            # Tab 1: Real-time Chat Viewer
            with gr.TabItem("🔴 Live Chat Viewer"):
                gr.Markdown("## 📱 Recent Conversation Records (Real-time Updates)")
                gr.Markdown("*View the latest conversations between users and digital twins*")
                
                with gr.Row():
                    refresh_realtime_btn = gr.Button("🔄 Refresh Latest Chats", variant="primary")
                
                realtime_summary = gr.Markdown("Loading...")
                
                # Recent conversations table (simplified)
                realtime_table = gr.Dataframe(
                    label="📋 Latest Conversations",
                    interactive=False
                )
                
                # Detailed conversation view
                gr.Markdown("## 📖 Conversation Details")
                with gr.Row():
                    realtime_conv_id = gr.Number(
                        label="💬 Click table ID or enter conversation ID",
                        placeholder="Enter conversation ID..."
                    )
                    view_realtime_btn = gr.Button("👁️ View Details", variant="secondary")
                
                realtime_detail = gr.Markdown(
                    "💡 Click on a conversation ID in the table above or manually enter an ID to view full conversation content"
                )
            
            # Tab 2: Overview Dashboard
            with gr.TabItem("📊 Data Overview"):
                with gr.Row():
                    days_input = gr.Slider(
                        1, 30, 
                        value=7, 
                        step=1, 
                        label="📅 View data for the past N days"
                    )
                    refresh_btn = gr.Button("🔄 Refresh Data", variant="primary")
                
                # Data source info
                data_source_info = gr.Markdown("**Data Source:** JSON file with GitHub sync")
                
                # Basic statistics cards
                gr.Markdown("## 📊 Basic Statistics")
                with gr.Row():
                    total_sessions = gr.Number(
                        label="👥 Total Sessions", 
                        interactive=False
                    )
                    total_messages = gr.Number(
                        label="💬 Total Messages", 
                        interactive=False
                    )
                    avg_response_time = gr.Number(
                        label="⏱️ Avg Response Time (ms)", 
                        interactive=False
                    )
                    active_students = gr.Number(
                        label="🎭 Active Students", 
                        interactive=False
                    )
                
                # Analysis (text-based for compatibility)
                gr.Markdown("## 📈 Detailed Analysis")
                with gr.Row():
                    with gr.Column():
                        student_analysis = gr.Markdown("Loading student popularity...")
                    with gr.Column():
                        daily_analysis = gr.Markdown("Loading daily usage...")
            
            # Tab 3: Advanced Chat Search
            with gr.TabItem("🔍 Advanced Chat Search"):
                gr.Markdown("## 🔍 Search and Filter Chat Records")
                
                # Filters
                with gr.Row():
                    chat_days_input = gr.Slider(
                        1, 30, 
                        value=7, 
                        step=1, 
                        label="📅 Search Days"
                    )
                    student_filter = gr.Dropdown(
                        choices=["All Students", "student001", "student002", "student003", "student004", "student005", 
                                "student006", "student007", "student008", "student009", "student010"],
                        value="All Students",
                        label="👤 Filter by Student"
                    )
                    search_keyword = gr.Textbox(
                        placeholder="Search keywords in messages...",
                        label="🔎 Keyword Search"
                    )
                
                with gr.Row():
                    search_btn = gr.Button("🔍 Search Conversations", variant="primary")
                    export_btn = gr.Button("📥 Export to CSV", variant="secondary")
                
                # Results
                search_summary = gr.Markdown("Search results will appear here...")
                
                # Chat table (simplified)
                chat_table = gr.Dataframe(
                    label="📋 Search Results",
                    interactive=False
                )
                
                # Detailed view
                gr.Markdown("## 📖 Conversation Details")
                conv_id_input = gr.Number(
                    label="💬 Enter conversation ID to view details"
                )
                view_detail_btn = gr.Button("👁️ View Details", variant="primary")
                
                conversation_detail = gr.Markdown(
                    "Select a conversation ID to view full content..."
                )
                
                # Export result
                export_result = gr.Markdown("")
        
        # Event handlers
        def update_realtime_chats():
            """Update real-time chat display"""
            chat_data, summary, conversations_raw = dashboard.get_recent_chat_conversations(limit=30)
            return chat_data, summary, conversations_raw
        
        def view_realtime_detail(conv_id, conversations_raw):
            """View detailed conversation from real-time data"""
            if conv_id:
                return dashboard.get_detailed_conversation_display(int(conv_id), conversations_raw)
            return "Please enter a valid conversation ID"
        
        def update_overview_dashboard(days):
            """Update overview dashboard data"""
            try:
                stats = dashboard.get_basic_stats(days)
                last_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get text-based analysis
                student_text = dashboard.get_student_popularity_text(days)
                daily_text = dashboard.get_daily_usage_text(days)
                
                return (
                    stats.get('total_sessions', 0),
                    stats.get('total_messages', 0),
                    round(stats.get('avg_response_time', 0), 2),
                    stats.get('active_students', 0),
                    student_text,
                    daily_text,
                    f"**Data Source:** JSON file with GitHub sync (Last updated: {last_update})"
                )
            except Exception as e:
                print(f"Error updating dashboard: {e}")
                return (0, 0, 0, 0, "Error loading student data", "Error loading daily data", "**Data Source:** Error loading data")
        
        def search_conversations(days, student_filter, search_keyword):
            """Search and display conversations"""
            chat_data, summary = dashboard.get_chat_conversations_filtered(days, student_filter, search_keyword)
            return chat_data, summary
        
        def view_conversation_detail(conv_id):
            """View detailed conversation"""
            if conv_id:
                return dashboard.get_detailed_conversation_display(int(conv_id))
            return "Please enter a valid conversation ID"
        
        def export_conversations(days, student_filter, search_keyword):
            """Export conversations to CSV"""
            filename, result = dashboard.export_conversations_to_csv(days, student_filter, search_keyword)
            return result
        
        # Bind events - Real-time tab
        refresh_realtime_btn.click(
            update_realtime_chats,
            outputs=[realtime_table, realtime_summary, recent_conversations_data]
        )
        
        view_realtime_btn.click(
            view_realtime_detail,
            inputs=[realtime_conv_id, recent_conversations_data],
            outputs=[realtime_detail]
        )
        
        # Bind events - Overview tab
        refresh_btn.click(
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_analysis, daily_analysis, data_source_info]
        )
        
        days_input.change(
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_analysis, daily_analysis, data_source_info]
        )
        
        # Bind events - Advanced search tab
        search_btn.click(
            search_conversations,
            inputs=[chat_days_input, student_filter, search_keyword],
            outputs=[chat_table, search_summary]
        )
        
        view_detail_btn.click(
            view_conversation_detail,
            inputs=[conv_id_input],
            outputs=[conversation_detail]
        )
        
        export_btn.click(
            export_conversations,
            inputs=[chat_days_input, student_filter, search_keyword],
            outputs=[export_result]
        )
        
        # Auto-search when filters change
        chat_days_input.change(
            search_conversations,
            inputs=[chat_days_input, student_filter, search_keyword],
            outputs=[chat_table, search_summary]
        )
        
        student_filter.change(
            search_conversations,
            inputs=[chat_days_input, student_filter, search_keyword],
            outputs=[chat_table, search_summary]
        )
        
        # Initial load
        demo.load(
            update_realtime_chats,
            outputs=[realtime_table, realtime_summary, recent_conversations_data]
        )
        
        demo.load(
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_analysis, daily_analysis, data_source_info]
        )
        
        demo.load(
            search_conversations,
            inputs=[chat_days_input, student_filter, search_keyword],
            outputs=[chat_table, search_summary]
        )
    
    return demo

if __name__ == "__main__":
    print("🔍 Starting Enhanced JSON-based monitoring dashboard...")
    print("📊 Data source: monitoring_data.json")
    print("💬 Features: Real-time chat viewing + Advanced search + Export")
    print("🌐 Enhanced monitoring dashboard ready")
    
    port = int(os.environ.get("PORT", 7861))
    monitoring_demo = create_enhanced_monitoring_dashboard()
    monitoring_demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        debug=False,
        show_api=False
    )
