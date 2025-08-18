"""
Independent monitoring application for Digital Twins system
Uses JSON file as data source with detailed chat log viewing
"""

import gradio as gr
import json
import os
import datetime
import requests
from datetime import timedelta
from collections import Counter, defaultdict
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class JSONMonitoringDashboard:
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
            print("✅ GitHub sync enabled for monitoring")
        else:
            print("📁 Using local file only for monitoring")
        return enabled
    
    def load_data(self):
        """Load latest data"""
        # First try to download from GitHub
        if self.github_enabled:
            self.download_from_github()
        
        # Load local data
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded monitoring data: {len(data.get('conversations', []))} conversations")
                    return data
            except Exception as e:
                print(f"❌ Error loading data: {e}")
        
        # Return empty data
        print("⚠️ No data file found")
        return {
            'sessions': {},
            'conversations': [],
            'user_actions': [],
            'system_metrics': [],
            'last_updated': datetime.datetime.now().isoformat()
        }
    
    def download_from_github(self):
        """Download latest data from GitHub"""
        if not self.github_enabled:
            return False
        
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{self.data_file}"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.json()
                import base64
                file_content = base64.b64decode(content['content']).decode('utf-8')
                
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                print("✅ Downloaded latest monitoring data from GitHub")
                return True
            elif response.status_code == 404:
                print("📁 No data file found in GitHub repository")
            else:
                print(f"⚠️ GitHub download failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Failed to download from GitHub: {e}")
        
        return False
    
    def get_chat_conversations(self, days=7, student_filter="", search_keyword="", limit=50):
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
    
    def get_detailed_conversation(self, conversation_id):
        """Get full details of a specific conversation"""
        data = self.load_data()
        
        for conv in data.get('conversations', []):
            if conv['id'] == conversation_id:
                timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                
                name_mapping = {
                    "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
                    "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
                    "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
                    "student010": "Tyler"
                }
                
                student_name = name_mapping.get(conv['student_id'], conv['student_id'])
                
                details = f"""
## 💬 聊天记录详情 (ID: {conversation_id})

**🕐 时间:** {timestamp}
**👤 学生:** {student_name} ({conv['student_id']})
**📍 会话ID:** {conv['session_id']}
**🎭 场景:** {conv.get('scene_context', 'No scene context')}
**⏱️ 响应时间:** {conv.get('response_time_ms', 0)}ms
**📏 消息长度:** {conv.get('message_length', 0)} 字符

---

### 👤 用户消息:
{conv['user_message']}

---

### 🤖 AI回复:
{conv['ai_response']}
                """
                
                return details
        
        return "❌ 未找到该对话记录"
    
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
    
    def get_student_popularity(self, days=7):
        """Student popularity analysis"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return self._create_empty_figure("No conversation data available")
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        recent_conversations = [
            conv for conv in data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) >= since_date
        ]
        
        if not recent_conversations:
            return self._create_empty_figure("No recent conversation data")
        
        student_counts = Counter(conv['student_id'] for conv in recent_conversations)
        
        # Convert to data format
        student_data = [
            {'student_id': student_id, 'message_count': count}
            for student_id, count in student_counts.most_common(10)
        ]
        
        if student_data:
            # Map student IDs to names
            name_mapping = {
                "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
                "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
                "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
                "student010": "Tyler"
            }
            
            student_names = [name_mapping.get(item['student_id'], item['student_id']) for item in student_data]
            message_counts = [item['message_count'] for item in student_data]
            
            fig = px.bar(
                x=student_names, 
                y=message_counts,
                title='Student Message Count',
                labels={'x': 'Student Name', 'y': 'Message Count'},
                color=message_counts,
                color_continuous_scale='viridis'
            )
            fig.update_layout(showlegend=False)
            return fig
        else:
            return self._create_empty_figure("No student data available")
    
    def get_daily_usage(self, days=7):
        """Daily usage trends"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return self._create_empty_figure("No conversation data available")
        
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
            return self._create_empty_figure("No recent usage data")
        
        dates = sorted(daily_data.keys())
        message_counts = [daily_data[date]['message_count'] for date in dates]
        session_counts = [daily_data[date]['session_count'] for date in dates]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, 
            y=message_counts,
            mode='lines+markers', 
            name='Message Count',
            line=dict(color='#1f77b4')
        ))
        fig.add_trace(go.Scatter(
            x=dates, 
            y=session_counts,
            mode='lines+markers', 
            name='Session Count', 
            yaxis='y2',
            line=dict(color='#ff7f0e')
        ))
        
        fig.update_layout(
            title='Daily Usage Trends',
            xaxis_title='Date',
            yaxis_title='Message Count',
            yaxis2=dict(title='Session Count', overlaying='y', side='right'),
            hovermode='x unified'
        )
        return fig
    
    def _create_empty_figure(self, message):
        """Create empty figure"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white'
        )
        return fig

def create_monitoring_dashboard():
    """Create monitoring dashboard"""
    dashboard = JSONMonitoringDashboard()
    
    with gr.Blocks(title="Digital Twin Monitoring Dashboard", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🔍 Digital Twin System Monitoring Dashboard")
        gr.Markdown("*Real-time monitoring of user behavior, conversation quality, and system performance*")
        
        with gr.Tabs():
            # Tab 1: Overview Dashboard
            with gr.TabItem("📊 Overview Dashboard"):
                with gr.Row():
                    days_input = gr.Slider(
                        1, 30, 
                        value=7, 
                        step=1, 
                        label="📅 View data for the past N days",
                        info="Select the time range to analyze"
                    )
                    refresh_btn = gr.Button("🔄 Refresh Data", variant="primary", scale=0)
                
                # Data source info
                with gr.Row():
                    data_source_info = gr.Markdown("**Data Source:** JSON file with GitHub sync")
                
                # Basic statistics cards
                gr.Markdown("## 📊 Basic Statistics")
                with gr.Row():
                    total_sessions = gr.Number(
                        label="👥 Total Sessions", 
                        interactive=False,
                        container=True
                    )
                    total_messages = gr.Number(
                        label="💬 Total Messages", 
                        interactive=False,
                        container=True
                    )
                    avg_response_time = gr.Number(
                        label="⏱️ Avg Response Time (ms)", 
                        interactive=False,
                        container=True
                    )
                    active_students = gr.Number(
                        label="🎭 Active Students", 
                        interactive=False,
                        container=True
                    )
                
                # Chart areas
                gr.Markdown("## 📈 Detailed Analysis")
                with gr.Row():
                    with gr.Column():
                        student_plot = gr.Plot(label="🎯 Student Popularity")
                    with gr.Column():
                        daily_plot = gr.Plot(label="📅 Daily Usage Trends")
            
            # Tab 2: Chat Logs Viewer
            with gr.TabItem("💬 Chat Logs Viewer"):
                gr.Markdown("## 🔍 View Detailed Chat Conversations")
                
                # Filters
                with gr.Row():
                    chat_days_input = gr.Slider(
                        1, 30, 
                        value=7, 
                        step=1, 
                        label="📅 Days to look back"
                    )
                    student_filter = gr.Dropdown(
                        choices=["All Students", "student001", "student002", "student003", "student004", "student005", 
                                "student006", "student007", "student008", "student009", "student010"],
                        value="All Students",
                        label="👤 Filter by Student"
                    )
                    search_keyword = gr.Textbox(
                        placeholder="Search in messages...",
                        label="🔎 Search Keyword"
                    )
                
                with gr.Row():
                    search_btn = gr.Button("🔍 Search Conversations", variant="primary")
                    export_btn = gr.Button("📥 Export to CSV", variant="secondary")
                
                # Results
                with gr.Row():
                    search_summary = gr.Markdown("Search results will appear here...")
                
                # Chat table
                chat_table = gr.Dataframe(
                    headers=["ID", "Time", "Student", "Student ID", "User Message", "AI Response", "Scene", "Response Time"],
                    datatype=["number", "str", "str", "str", "str", "str", "str", "str"],
                    label="📋 Chat Conversations",
                    interactive=False,
                    height=400
                )
                
                # Detailed view
                gr.Markdown("## 📖 Conversation Details")
                conv_id_input = gr.Number(
                    label="💬 Enter Conversation ID to view details",
                    info="Click on any ID from the table above"
                )
                view_detail_btn = gr.Button("👁️ View Details", variant="primary")
                
                conversation_detail = gr.Markdown(
                    "Select a conversation ID above to view full details...",
                    elem_classes="conversation-detail"
                )
                
                # Export result
                export_result = gr.Markdown("")
        
        # Event handlers for Overview tab
        def update_overview_dashboard(days):
            """Update overview dashboard data"""
            try:
                stats = dashboard.get_basic_stats(days)
                last_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                return (
                    stats.get('total_sessions', 0),
                    stats.get('total_messages', 0),
                    round(stats.get('avg_response_time', 0), 2),
                    stats.get('active_students', 0),
                    dashboard.get_student_popularity(days),
                    dashboard.get_daily_usage(days),
                    f"**Data Source:** JSON file with GitHub sync (Last updated: {last_update})"
                )
            except Exception as e:
                print(f"Error updating dashboard: {e}")
                empty_fig = dashboard._create_empty_figure("Data loading failed")
                return (0, 0, 0, 0, empty_fig, empty_fig, "**Data Source:** Error loading data")
        
        # Event handlers for Chat Logs tab
        def search_conversations(days, student_filter, search_keyword):
            """Search and display conversations"""
            chat_data, summary = dashboard.get_chat_conversations(days, student_filter, search_keyword)
            return chat_data, summary
        
        def view_conversation_detail(conv_id):
            """View detailed conversation"""
            if conv_id:
                return dashboard.get_detailed_conversation(int(conv_id))
            return "Please enter a valid conversation ID"
        
        def export_conversations(days, student_filter, search_keyword):
            """Export conversations to CSV"""
            filename, result = dashboard.export_conversations_to_csv(days, student_filter, search_keyword)
            return result
        
        # Bind events - Overview tab
        refresh_btn.click(
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_plot, daily_plot, data_source_info]
        )
        
        days_input.change(
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_plot, daily_plot, data_source_info]
        )
        
        # Bind events - Chat Logs tab
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
            update_overview_dashboard,
            inputs=[days_input],
            outputs=[total_sessions, total_messages, avg_response_time, active_students, student_plot, daily_plot, data_source_info]
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
    print("💬 Now includes detailed chat log viewing!")
    print("🌐 Monitoring dashboard ready")
    
    port = int(os.environ.get("PORT", 7861))
    monitoring_demo = create_monitoring_dashboard()
    monitoring_demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,  # Don't share publicly
        debug=False,
        show_api=False
    )
