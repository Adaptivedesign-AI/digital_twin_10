"""
Independent monitoring application for Digital Twins system
Deploy this as a separate service on Render
"""

import gradio as gr
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

"""
Independent monitoring application for Digital Twins system
使用JSON文件作为数据源
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
        """设置GitHub数据同步"""
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
        """加载最新数据"""
        # 首先尝试从GitHub下载最新数据
        if self.github_enabled:
            self.download_from_github()
        
        # 加载本地数据
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded monitoring data: {len(data.get('conversations', []))} conversations")
                    return data
            except Exception as e:
                print(f"❌ Error loading data: {e}")
        
        # 返回空数据
        print("⚠️ No data file found")
        return {
            'sessions': {},
            'conversations': [],
            'user_actions': [],
            'system_metrics': [],
            'last_updated': datetime.datetime.now().isoformat()
        }
    
    def download_from_github(self):
        """从GitHub下载最新数据"""
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
        """获取基本统计数据"""
        data = self.load_data()
        
        if not data.get('conversations'):
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'avg_response_time': 0,
                'active_students': 0
            }
        
        since_date = datetime.datetime.now() - timedelta(days=days)
        
        # 过滤最近的数据
        recent_conversations = [
            conv for conv in data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) >= since_date
        ]
        
        recent_sessions = [
            session for session in data['sessions'].values()
            if datetime.datetime.fromisoformat(session['start_time']) >= since_date
        ]
        
        # 计算统计数据
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
        """学生受欢迎程度分析"""
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
        
        # 转换为DataFrame格式
        student_data = [
            {'student_id': student_id, 'message_count': count}
            for student_id, count in student_counts.most_common(10)
        ]
        
        if student_data:
            # 映射学生ID到名字
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
        """每日使用趋势"""
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
                
                # 计算会话数（避免重复）
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
        """响应时间分析"""
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
        """场景使用统计"""
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
        
        scenes = list(scene_counts.keys())[:8]  # 取前8个
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
        """用户行为统计"""
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
        
        # 翻译action类型
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
        """创建空图表"""
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
        return fig 'Response Time (ms)', 'count': 'Frequency'},
                    color_discrete_sequence=['#2E8B57']
                )
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("No response time data available")
        except Exception as e:
            conn.close()
            print(f"Error getting response time analysis: {e}")
            return self._create_empty_figure("Data loading failed")
    
    def get_scene_usage(self, days=7):
        """Scene usage statistics"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT 
                    CASE 
                        WHEN scene_context = '' OR scene_context IS NULL THEN 'Default Scene'
                        WHEN LENGTH(scene_context) > 30 THEN SUBSTR(scene_context, 1, 30) || '...'
                        ELSE scene_context 
                    END as scene,
                    COUNT(*) as usage_count
                FROM conversations 
                WHERE timestamp >= ?
                GROUP BY scene_context
                ORDER BY usage_count DESC
                LIMIT 8
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            conn.close()
            
            if len(df) > 0:
                fig = px.pie(
                    df, 
                    values='usage_count', 
                    names='scene',
                    title='Scene Usage Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                return fig
            else:
                return self._create_empty_figure("No scene usage data available")
        except Exception as e:
            conn.close()
            print(f"Error getting scene usage statistics: {e}")
            return self._create_empty_figure("Data loading failed")
    
    def get_user_actions_summary(self, days=7):
        """User actions summary"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT 
                    action_type,
                    COUNT(*) as action_count
                FROM user_actions 
                WHERE timestamp >= ?
                GROUP BY action_type
                ORDER BY action_count DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            conn.close()
            
            if len(df) > 0:
                # Translate action_type to English
                action_mapping = {
                    'send_message': 'Send Message',
                    'student_select': 'Select Student',
                    'clear_chat': 'Clear Chat',
                    'scene_change': 'Change Scene',
                    'back_to_selection': 'Back to Selection'
                }
                df['action_name'] = df['action_type'].map(action_mapping).fillna(df['action_type'])
                
                fig = px.bar(
                    df, 
                    x='action_name', 
                    y='action_count',
                    title='User Action Statistics',
                    labels={'action_name': 'Action Type', 'action_count': 'Count'},
                    color='action_count',
                    color_continuous_scale='blues'
                )
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("No user action data available")
        except Exception as e:
            conn.close()
            print(f"Error getting user actions summary: {e}")
            return self._create_empty_figure("Data loading failed")
    
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
    dashboard = MonitoringDashboard()
    
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
                return (
                    stats.get('total_sessions', 0),
                    stats.get('total_messages', 0),
                    round(stats.get('avg_response_time', 0), 2),
                    stats.get('active_students', 0),
                    dashboard.get_student_popularity(days),
                    dashboard.get_daily_usage(days),
                    dashboard.get_response_time_analysis(days),
                    dashboard.get_scene_usage(days),
                    dashboard.get_user_actions_summary(days)
                )
            except Exception as e:
                print(f"Error updating dashboard: {e}")
                empty_fig = dashboard._create_empty_figure("Data loading failed")
                return (0, 0, 0, 0, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig)
        
        # Event handlers
        refresh_btn.click(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot
            ]
        )
        
        days_input.change(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot
            ]
        )
        
        # Initial load
        demo.load(
            update_dashboard,
            inputs=[days_input],
            outputs=[
                total_sessions, total_messages, avg_response_time, active_students,
                student_plot, daily_plot, response_time_plot, scene_plot, user_actions_plot
            ]
        )
    
    return demo

def create_protected_dashboard():
    """创建带密码保护的监控仪表板"""
    
    # 从环境变量获取密码
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "your-secret-password-123")
    
    def check_password(password):
        """验证密码"""
        return password == ADMIN_PASSWORD
    
    def login_interface():
        """登录界面"""
        with gr.Blocks(title="Access Required") as login_demo:
            gr.Markdown("# 🔐 Access Required")
            gr.Markdown("Please enter the access password:")
            
            with gr.Row():
                password_input = gr.Textbox(
                    placeholder="Enter password...", 
                    type="password",
                    label="Password"
                )
                login_btn = gr.Button("Login", variant="primary")
            
            status_msg = gr.Markdown("")
            
            def handle_login(password):
                if check_password(password):
                    return "✅ Access granted! Redirecting to dashboard..."
                else:
                    return "❌ Invalid password. Please try again."
            
            login_btn.click(
                handle_login,
                inputs=[password_input],
                outputs=[status_msg]
            )
        
        return login_demo
    
    # 检查是否提供了密码参数
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == ADMIN_PASSWORD:
        # 直接启动监控面板
        return create_monitoring_dashboard()
    else:
        # 显示登录界面
        return login_interface()

if __name__ == "__main__":
    print("🔍 Starting protected monitoring dashboard...")
    print("📊 Data source: monitoring.db")
    print("🔐 Password protection enabled")
    
    port = int(os.environ.get("PORT", 7861))
    
    # 检查是否通过环境变量直接访问
    if os.environ.get("DIRECT_ACCESS") == "true":
        demo = create_monitoring_dashboard()
        print("🌐 Direct access mode - no password required")
    else:
        demo = create_protected_dashboard()
        print("🔐 Protected mode - password required")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,  # 不公开分享链接
        debug=False,
        show_api=False,
        auth=("admin", os.environ.get("ADMIN_PASSWORD", "your-secret-password-123"))  # HTTP基本认证
    )
