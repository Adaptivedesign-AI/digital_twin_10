import gradio as gr
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

class MonitoringDashboard:
    def __init__(self, db_path='monitoring.db'):
        self.db_path = db_path
    
    def get_db_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_basic_stats(self, days=7):
        """获取基本统计数据"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            # 总体统计
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
            
            # 处理NULL值
            for key, value in result.items():
                if pd.isna(value):
                    result[key] = 0
                    
            conn.close()
            return result
        except Exception as e:
            conn.close()
            print(f"获取基本统计数据时出错: {e}")
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'avg_response_time': 0,
                'active_students': 0
            }
    
    def get_student_popularity(self, days=7):
        """学生受欢迎程度"""
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
                # 映射学生ID到名字
                name_mapping = {
                    "student001": "Jaden", "student002": "Ethan", "student003": "Emily",
                    "student004": "Malik", "student005": "Aaliyah", "student006": "Brian",
                    "student007": "Grace", "student008": "Brianna", "student009": "Leilani",
                    "student010": "Tyler"
                }
                df['student_name'] = df['student_id'].map(name_mapping).fillna(df['student_id'])
                
                fig = px.bar(df, x='student_name', y='message_count',
                            title='学生聊天消息数量',
                            labels={'student_name': '学生姓名', 'message_count': '消息数量'},
                            color='message_count',
                            color_continuous_scale='viridis')
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("暂无学生对话数据")
        except Exception as e:
            conn.close()
            print(f"获取学生受欢迎程度时出错: {e}")
            return self._create_empty_figure("数据加载失败")
    
    def get_daily_usage(self, days=7):
        """每日使用情况"""
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
                    name='消息数量',
                    line=dict(color='#1f77b4')
                ))
                fig.add_trace(go.Scatter(
                    x=df['date'], 
                    y=df['session_count'],
                    mode='lines+markers', 
                    name='会话数量', 
                    yaxis='y2',
                    line=dict(color='#ff7f0e')
                ))
                
                fig.update_layout(
                    title='每日使用趋势',
                    xaxis_title='日期',
                    yaxis_title='消息数量',
                    yaxis2=dict(title='会话数量', overlaying='y', side='right'),
                    hovermode='x unified'
                )
                return fig
            else:
                return self._create_empty_figure("暂无每日使用数据")
        except Exception as e:
            conn.close()
            print(f"获取每日使用情况时出错: {e}")
            return self._create_empty_figure("数据加载失败")
    
    def get_response_time_analysis(self, days=7):
        """响应时间分析"""
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
                    title='API响应时间分布',
                    labels={'response_time_ms': '响应时间(毫秒)', 'count': '频次'},
                    color_discrete_sequence=['#2E8B57']
                )
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("暂无响应时间数据")
        except Exception as e:
            conn.close()
            print(f"获取响应时间分析时出错: {e}")
            return self._create_empty_figure("数据加载失败")
    
    def get_scene_usage(self, days=7):
        """场景使用统计"""
        conn = self.get_db_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            query = '''
                SELECT 
                    CASE 
                        WHEN scene_context = '' OR scene_context IS NULL THEN '默认场景'
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
                    title='场景使用分布',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                return fig
            else:
                return self._create_empty_figure("暂无场景使用数据")
        except Exception as e:
            conn.close()
            print(f"获取场景使用统计时出错: {e}")
            return self._create_empty_figure("数据加载失败")
    
    def get_user_actions_summary(self, days=7):
        """用户行为摘要"""
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
                # 中文化action_type
                action_mapping = {
                    'send_message': '发送消息',
                    'student_select': '选择学生',
                    'clear_chat': '清除聊天',
                    'scene_change': '切换场景',
                    'back_to_selection': '返回选择页'
                }
                df['action_name'] = df['action_type'].map(action_mapping).fillna(df['action_type'])
                
                fig = px.bar(
                    df, 
                    x='action_name', 
                    y='action_count',
                    title='用户行为统计',
                    labels={'action_name': '行为类型', 'action_count': '次数'},
                    color='action_count',
                    color_continuous_scale='blues'
                )
                fig.update_layout(showlegend=False)
                return fig
            else:
                return self._create_empty_figure("暂无用户行为数据")
        except Exception as e:
            conn.close()
            print(f"获取用户行为摘要时出错: {e}")
            return self._create_empty_figure("数据加载失败")
    
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
        return fig

def create_dashboard():
    """创建监控仪表板"""
    dashboard = MonitoringDashboard()
    
    with gr.Blocks(title="数字孪生监控仪表板", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🔍 数字孪生系统监控仪表板")
        gr.Markdown("*实时监控用户行为、对话质量和系统性能*")
        
        with gr.Row():
            days_input = gr.Slider(
                1, 30, 
                value=7, 
                step=1, 
                label="📅 查看过去几天的数据",
                info="选择要分析的时间范围"
            )
            refresh_btn = gr.Button("🔄 刷新数据", variant="primary", scale=0)
        
        # 基本统计卡片
        gr.Markdown("## 📊 基本统计")
        with gr.Row():
            total_sessions = gr.Number(
                label="👥 总会话数", 
                interactive=False,
                container=True
            )
            total_messages = gr.Number(
                label="💬 总消息数", 
                interactive=False,
                container=True
            )
            avg_response_time = gr.Number(
                label="⏱️ 平均响应时间(ms)", 
                interactive=False,
                container=True
            )
            active_students = gr.Number(
                label="🎭 活跃学生数", 
                interactive=False,
                container=True
            )
        
        # 图表区域
        gr.Markdown("## 📈 详细分析")
        with gr.Row():
            with gr.Column():
                student_plot = gr.Plot(label="🎯 学生受欢迎程度")
                response_time_plot = gr.Plot(label="⚡ 响应时间分析")
            with gr.Column():
                daily_plot = gr.Plot(label="📅 每日使用趋势")
                user_actions_plot = gr.Plot(label="🎮 用户行为统计")
        
        with gr.Row():
            scene_plot = gr.Plot(label="🎬 场景使用分布")
        
        def update_dashboard(days):
            """更新仪表板数据"""
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
                print(f"更新仪表板时出错: {e}")
                empty_fig = dashboard._create_empty_figure("数据加载失败")
                return (0, 0, 0, 0, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig)
        
        # 事件处理
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
        
        # 初始化加载
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
    print("🔍 启动监控仪表板...")
    print("📊 数据源: monitoring.db")
    print("🌐 访问地址: http://localhost:7861")
    
    dashboard_demo = create_dashboard()
    dashboard_demo.launch(
        server_port=7861, 
        share=False,
        server_name="0.0.0.0"
    )
