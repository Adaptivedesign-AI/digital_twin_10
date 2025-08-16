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

class MonitoringDashboard:
    def __init__(self, db_path='monitoring.db'):
        self.db_path = db_path
    
    def get_db_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_basic_stats(self, days=7):
        """Get basic statistics"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            # Overall statistics
            query = '''
                SELECT 
                    COUNT(DISTINCT s.session_id) as total_sessions,
                    COUNT(c.id) as total_messages,
                    AVG(c.response_time_ms) as avg_response_time,
                    COUNT(DISTINCT c.student_id) as active_students
                FROM user_sessions s
                LEFT JOIN conversations c ON s.session_id = c.session_id
                WHERE s.start_time >= ?
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            result = df.iloc[0].to_dict()
            
            # Handle NULL values
            for key, value in result.items():
                if pd.isna(value):
                    result[key] = 0
                    
            conn.close()
            return result
        except Exception as e:
            conn.close()
            print(f"Error getting basic statistics: {e}")
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'avg_response_time': 0,
                'active_students': 0
            }
    
    def get_student_popularity(self, days=7):
        """Student popularity analysis"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT student_id, COUNT(*) as message_count
                FROM conversations 
                WHERE timestamp >= ?
                GROUP BY student_id
                ORDER BY message_count DESC
                LIMIT 10
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            conn.close()
            
            if len(df) > 0:
                # Map student IDs to names
                name_mapping = {
                    "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
                    "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
                    "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
                    "student010": "Tyler"
                }
                df['student_name'] = df['student_id'].map(name_mapping).fillna(df['student_id'])
                
                fig = px.bar(df, x='student_name', y='message_count',
                            title='Student Message Count',
                            labels={'student_name': 'Student Name', 'message_count': 'Message Count'},
                            color='message_count',
                            color_continuous_scale='viridis')
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("No student conversation data available")
        except Exception as e:
            conn.close()
            print(f"Error getting student popularity: {e}")
            return self._create_empty_figure("Data loading failed")
    
    def get_daily_usage(self, days=7):
        """Daily usage analysis"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as message_count,
                    COUNT(DISTINCT session_id) as session_count
                FROM conversations 
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            conn.close()
            
            if len(df) > 0:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['date'], 
                    y=df['message_count'],
                    mode='lines+markers', 
                    name='Message Count',
                    line=dict(color='#1f77b4')
                ))
                fig.add_trace(go.Scatter(
                    x=df['date'], 
                    y=df['session_count'],
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
            else:
                return self._create_empty_figure("No daily usage data available")
        except Exception as e:
            conn.close()
            print(f"Error getting daily usage: {e}")
            return self._create_empty_figure("Data loading failed")
    
    def get_response_time_analysis(self, days=7):
        """Response time analysis"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT response_time_ms
                FROM conversations 
                WHERE timestamp >= ? AND response_time_ms > 0 AND response_time_ms < 30000
            '''
            
            df = pd.read_sql_query(query, conn, params=(since_date,))
            conn.close()
            
            if len(df) > 0:
                fig = px.histogram(
                    df, 
                    x='response_time_ms', 
                    nbins=20,
                    title='API Response Time Distribution',
                    labels={'response_time_ms': 'Response Time (ms)', 'count': 'Frequency'},
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

if __name__ == "__main__":
    print("🔍 Starting monitoring dashboard...")
    print("📊 Data source: monitoring.db")
    print("🌐 Monitoring dashboard ready")
    
    port = int(os.environ.get("PORT", 7861))
    monitoring_demo = create_monitoring_dashboard()
    monitoring_demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,  # Important for Render deployment
        debug=False,
        show_api=False
    )
