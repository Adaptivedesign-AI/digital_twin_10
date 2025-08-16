"""
Data Monitoring Module - Independent monitoring functionality module
If you want to separate monitoring functionality from app.py, you can use this file
"""

import sqlite3
import datetime
import uuid
import json
import os

class DataMonitor:
    """Data monitoring class - responsible for collecting and storing user behavior data"""
    
    def __init__(self, db_path='monitoring.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                ip_address TEXT,
                user_agent TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                total_actions INTEGER DEFAULT 0
            )
        ''')
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                student_id TEXT,
                user_message TEXT,
                ai_response TEXT,
                scene_context TEXT,
                timestamp TIMESTAMP,
                response_time_ms INTEGER,
                message_length INTEGER,
                ai_response_length INTEGER,
                FOREIGN KEY (session_id) REFERENCES user_sessions (session_id)
            )
        ''')
        
        # User actions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                action_type TEXT,
                action_data TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES user_sessions (session_id)
            )
        ''')
        
        # System metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT,
                metric_value REAL,
                details TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        # Error logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                error_type TEXT,
                error_message TEXT,
                stack_trace TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialization completed: {self.db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_session(self, request_info=None):
        """Create new user session"""
        session_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_sessions (session_id, ip_address, user_agent, start_time)
                VALUES (?, ?, ?, ?)
            ''', (
                session_id,
                request_info.get('ip', 'unknown') if request_info else 'unknown',
                request_info.get('user_agent', 'unknown') if request_info else 'unknown',
                datetime.datetime.now()
            ))
            conn.commit()
            print(f"📝 New session created: {session_id}")
        except Exception as e:
            print(f"❌ Failed to create session: {e}")
        finally:
            conn.close()
        
        return session_id
    
    def end_session(self, session_id):
        """End session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE user_sessions 
                SET end_time = ?
                WHERE session_id = ?
            ''', (datetime.datetime.now(), session_id))
            conn.commit()
            print(f"🔚 Session ended: {session_id}")
        except Exception as e:
            print(f"❌ Failed to end session: {e}")
        finally:
            conn.close()
    
    def log_conversation(self, session_id, student_id, user_message, ai_response, 
                        scene_context="", response_time_ms=0):
        """Log conversation data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO conversations 
                (session_id, student_id, user_message, ai_response, scene_context, 
                 timestamp, response_time_ms, message_length, ai_response_length)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                student_id,
                user_message,
                ai_response,
                scene_context,
                datetime.datetime.now(),
                response_time_ms,
                len(user_message) if user_message else 0,
                len(ai_response) if ai_response else 0
            ))
            
            # Update session message count
            cursor.execute('''
                UPDATE user_sessions 
                SET total_messages = total_messages + 1 
                WHERE session_id = ?
            ''', (session_id,))
            
            conn.commit()
            print(f"💬 Conversation logged: {session_id} -> {student_id}")
        except Exception as e:
            print(f"❌ Failed to log conversation: {e}")
        finally:
            conn.close()
    
    def log_user_action(self, session_id, action_type, action_data=None):
        """Log user action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_actions (session_id, action_type, action_data, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                session_id,
                action_type,
                json.dumps(action_data) if action_data else None,
                datetime.datetime.now()
            ))
            
            # Update session action count
            cursor.execute('''
                UPDATE user_sessions 
                SET total_actions = total_actions + 1 
                WHERE session_id = ?
            ''', (session_id,))
            
            conn.commit()
            print(f"🎯 User action logged: {action_type}")
        except Exception as e:
            print(f"❌ Failed to log user action: {e}")
        finally:
            conn.close()
    
    def log_system_metric(self, metric_type, metric_value, details=""):
        """Log system metric"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO system_metrics (metric_type, metric_value, details, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                metric_type,
                metric_value,
                details,
                datetime.datetime.now()
            ))
            conn.commit()
            print(f"📊 System metric logged: {metric_type} = {metric_value}")
        except Exception as e:
            print(f"❌ Failed to log system metric: {e}")
        finally:
            conn.close()
    
    def log_error(self, session_id, error_type, error_message, stack_trace=""):
        """Log error"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO error_logs (session_id, error_type, error_message, stack_trace, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                session_id,
                error_type,
                error_message,
                stack_trace,
                datetime.datetime.now()
            ))
            conn.commit()
            print(f"🚨 Error logged: {error_type}")
        except Exception as e:
            print(f"❌ Failed to log error: {e}")
        finally:
            conn.close()
    
    def get_session_summary(self, session_id):
        """Get session summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Basic session information
            cursor.execute('''
                SELECT * FROM user_sessions WHERE session_id = ?
            ''', (session_id,))
            session_info = cursor.fetchone()
            
            # Conversation statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as message_count,
                    COUNT(DISTINCT student_id) as students_interacted,
                    AVG(response_time_ms) as avg_response_time
                FROM conversations 
                WHERE session_id = ?
            ''', (session_id,))
            conversation_stats = cursor.fetchone()
            
            # Action statistics
            cursor.execute('''
                SELECT action_type, COUNT(*) as count
                FROM user_actions 
                WHERE session_id = ?
                GROUP BY action_type
            ''', (session_id,))
            action_stats = cursor.fetchall()
            
            return {
                'session_info': session_info,
                'conversation_stats': conversation_stats,
                'action_stats': action_stats
            }
        except Exception as e:
            print(f"❌ Failed to get session summary: {e}")
            return None
        finally:
            conn.close()
    
    def export_data(self, output_dir="exports", days=30):
        """Export data to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        since_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        conn = self.get_connection()
        
        try:
            import pandas as pd
            
            # Export session data
            sessions_df = pd.read_sql_query('''
                SELECT * FROM user_sessions 
                WHERE start_time >= ?
            ''', conn, params=(since_date,))
            sessions_df.to_csv(f"{output_dir}/sessions_{days}days.csv", index=False)
            
            # Export conversation data
            conversations_df = pd.read_sql_query('''
                SELECT * FROM conversations 
                WHERE timestamp >= ?
            ''', conn, params=(since_date,))
            conversations_df.to_csv(f"{output_dir}/conversations_{days}days.csv", index=False)
            
            # Export user action data
            actions_df = pd.read_sql_query('''
                SELECT * FROM user_actions 
                WHERE timestamp >= ?
            ''', conn, params=(since_date,))
            actions_df.to_csv(f"{output_dir}/user_actions_{days}days.csv", index=False)
            
            print(f"📁 Data export completed: {output_dir}/")
            return output_dir
        except Exception as e:
            print(f"❌ Data export failed: {e}")
            return None
        finally:
            conn.close()

# Convenience functions
def create_monitor(db_path='monitoring.db'):
    """Create monitor instance"""
    return DataMonitor(db_path)

# Usage example
if __name__ == "__main__":
    # Test monitoring system
    monitor = create_monitor()
    
    # Create test session
    session = monitor.create_session({'ip': '127.0.0.1', 'user_agent': 'test'})
    
    # Log test actions
    monitor.log_user_action(session, 'test_action', {'test': True})
    monitor.log_conversation(session, 'student001', 'Hello', 'Hi there!', 'test scene', 1500)
    monitor.log_system_metric('test_metric', 100, 'test details')
    
    # Get session summary
    summary = monitor.get_session_summary(session)
    print("Session summary:", summary)
    
    print("✅ Monitoring system test completed")
