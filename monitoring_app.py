"""
Independent monitoring application for Digital Twins system
Uses JSON file as data source
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
    
    def get_response_time_analysis(self, days=7):
        """Response time analysis"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return self._create_empty_figure("No conversation data available")
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        response_times = [
            conv['response_time_ms'] for conv in data['conversations']
            if (datetime.datetime.fromisoformat(conv['timestamp']) >= since_date and 
                conv['response_time_ms'] > 0 and conv['response_time_ms'] < 30000)
        ]
        
        if not response_times:
            return self._create_empty_figure("No response time data available")
        
        fig = px.histogram(
            x=response_times,
            nbins=20,
            title='API Response Time Distribution',
            labels={'x': 'Response Time (ms)', 'y': 'Frequency'},
            color_discrete_sequence=['#2E8B57']
        )
        fig.update_layout(showlegend=False)
        return fig
    
    def get_scene_usage(self, days=7):
        """Scene usage statistics"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return self._create_empty_figure("No conversation data available")
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        scene_counts = Counter()
        for conv in data['conversations']:
            if datetime.datetime.fromisoformat(conv['timestamp']) >= since_date:
                scene = conv.get('scene_context', '')
                if not scene or scene == '':
                    scene = 'Default Scene'
                elif len(scene) > 30:
                    scene = scene[:30] + '...'
                scene_counts[scene] += 1
        
        if not scene_counts:
            return self._create_empty_figure("No scene usage data available")
        
        scenes = list(scene_counts.keys())[:8]  # Top 8
        counts = [scene_counts[scene] for scene in scenes]
        
        fig = px.pie(
            values=counts,
            names=scenes,
            title='Scene Usage Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    def get_user_actions_summary(self, days=7):
        """User actions statistics"""
        data = self.load_data()
        
        if not data.get('user_actions'):
            return self._create_empty_figure("No user action data available")
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        action_counts = Counter()
        for action in data['user_actions']:
            if datetime.datetime.fromisoformat(action['timestamp']) >= since_date:
                action_counts[action['action_type']] += 1
        
        if not action_counts:
            return self._create_empty_figure("No recent user action data")
        
        # Translate action types
        action_mapping = {
            'send_message': 'Send Message',
            'student_select': 'Select Student',
            'clear_chat': 'Clear Chat',
            'scene_change': 'Change Scene',
            'back_to_selection': 'Back to Selection'
        }
        
        action_names = [action_mapping.get(action, action) for action in action_counts.keys()]
        counts = list(action_counts.values())
        
        fig = px.bar(
            x=action_names,
            y=counts,
            title='User Action Statistics',
            labels={'x': 'Action Type', 'y': 'Count'},
            color=counts,
            color_continuous_scale='blues'
        )
        fig.update_layout(showlegend=False)
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
                response_time_plot = gr.Plot(label="⚡ Response Time Analysis")
            with gr.Column():
                daily_plot = gr.Plot(label="📅 Daily Usage Trends")
                user_actions_plot = gr.Plot(label="🎮 User Action Statistics")
        
        with gr.Row():
            scene_plot = gr.Plot(label="🎬 Scene Usage Distribution")
        
        def update_dashboard(days):
            """Update dashboard data"""
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
                    dashboard.get_response_time_analysis(days),
                    dashboard.get_scene_usage(days),
                    dashboard.get_user_actions_summary(days),
                    f"**Data Source:** JSON file with GitHub sync (Last updated: {last_update})"
                )
            except Exception as e:
                print(f"Error updating dashboard: {e}")
                empty_fig = dashboard._create_empty_figure("Data loading failed")
                return (0, 0, 0, 0, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, 
                       "**Data Source:** Error loading data")
        
        # Event handlers
        refresh_btn.click(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot,
                data_source_info
            ]
        )
        
        days_input.change(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot,
                data_source_info
            ]
        )
        
        # Initial load
        demo.load(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot,
                data_source_info
            ]
        )
    
    return demo

if __name__ == "__main__":
    print("🔍 Starting JSON-based monitoring dashboard...")
    print("📊 Data source: monitoring_data.json")
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
