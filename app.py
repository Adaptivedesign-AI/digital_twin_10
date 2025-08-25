# app.py - Flask版本完全替换Gradio (增强版数据监控)
from flask import Flask, render_template, request, jsonify, session, redirect, Response
import json
import os
import datetime
import uuid
from openai import OpenAI
import requests
from flask_cors import CORS
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-here")

# 启用CORS支持
CORS(app)

# 初始化OpenAI客户端
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 添加调试信息
print(f"🔑 OpenAI API Key configured: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}")
print(f"🔐 Secret Key configured: {'Yes' if os.environ.get('SECRET_KEY') else 'No'}")
print(f"👤 Admin Password configured: {'Yes' if os.environ.get('ADMIN_PASSWORD') else 'No'}")
print(f"📊 GitHub Data Sync configured: {'Yes' if os.environ.get('GITHUB_TOKEN') else 'No'}")

# ================================
# 数据定义
# ================================

name_dict = {
    "student001": "Jaden",
    "student002": "Ethan",    
    "student003": "Emily",
    "student004": "Malik",     
    "student005": "Aaliyah",  
    "student006": "Brian",
    "student007": "Grace",
    "student008": "Brianna",
    "student009": "Leilani",
    "student010": "Tyler"
}

student_descriptions = {
    "student001": "14 years old. Bold and street-smart.",
    "student002": "16 years old. Detached and impulsive.",
    "student003": "14 years old. Sensitive and self-critical.",
    "student004": "13 years old. Tough-minded and emotionally guarded.",
    "student005": "15 years old. Introspective and emotionally aware.",
    "student006": "17 years old. Disciplined but emotionally withdrawn.",
    "student007": "16 years old. Goal-oriented and emotionally steady.",
    "student008": "15 years old. Friendly but cautious.",
    "student009": "17 years old. Thoughtful and quietly confident.",
    "student010": "16 years old. Restless and emotionally conflicted."
}

student_profiles = {
    "student001": {
        "age": 14,
        "sex": "Male", 
        "race_ethnicity": "Hispanic/Latino, Black or African American",
        "grade": "9th grade",
        "emotional_health": "Experienced threats with weapons at school but did not engage in physical fights. Carries weapon for protection some days.",
        "mental_health": "No depression or suicidal ideation. Not bullied. Has some alcohol use (1-2 days/month). Started drinking early (age 9-10)."
    },
    "student002": {
        "age": 16,
        "sex": "Male",
        "race_ethnicity": "Hispanic/Latino, White", 
        "grade": "11th grade",
        "emotional_health": "Generally stable social relationships. No history of violence or threats.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. Moderate alcohol use (3-5 days/month)."
    },
    "student003": {
        "age": 14,
        "sex": "Female",
        "race_ethnicity": "Asian",
        "grade": "9th grade",
        "emotional_health": "Experiences both school and electronic bullying. Socially vulnerable.",
        "mental_health": "Reports feeling sad or hopeless for extended periods. Experiences bullying both in-person and online."
    },
    "student004": {
        "age": 13,
        "sex": "Male",
        "race_ethnicity": "Black or African American",
        "grade": "9th grade",
        "emotional_health": "Stable social environment, no bullying or violence exposure.",
        "mental_health": "No depression or suicidal ideation. Not bullied. Some alcohol use (1-2 days/month)."
    },
    "student005": {
        "age": 15,
        "sex": "Female", 
        "race_ethnicity": "Black or African American",
        "grade": "9th grade",
        "emotional_health": "Not bullied, stable peer relationships.",
        "mental_health": "Reports periods of sadness or hopelessness. No substance use reported."
    },
    "student006": {
        "age": 17,
        "sex": "Male",
        "race_ethnicity": "Asian",
        "grade": "11th grade",
        "emotional_health": "Stable social environment, no violence or bullying.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    },
    "student007": {
        "age": 16,
        "sex": "Female",
        "race_ethnicity": "Asian", 
        "grade": "10th grade",
        "emotional_health": "Stable peer relationships, no bullying or violence.",
        "mental_health": "No depression or suicidal ideation. Not bullied. No substance use reported."
    },
    "student008": {
        "age": 15,
        "sex": "Female",
        "race_ethnicity": "Mixed race (Black or African American, White)",
        "grade": "9th grade",
        "emotional_health": "Stable social environment, no bullying or threats.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    },
    "student009": {
        "age": 17,
        "sex": "Female",
        "race_ethnicity": "Mixed race (Native Hawaiian/Pacific Islander, White)",
        "grade": "12th grade",
        "emotional_health": "Stable peer relationships, no violence or bullying exposure.",
        "mental_health": "No depression or suicidal ideation. Not bullied. No substance use reported."
    },
    "student010": {
        "age": 16,
        "sex": "Male", 
        "race_ethnicity": "Mixed race (Native Hawaiian/Pacific Islander, White)",
        "grade": "10th grade",
        "emotional_health": "Stable social environment, no bullying or violence.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    }
}

scene_options = [
    "Meet with a new friend for the first time",
    "Posted a video on TikTok and received hateful comments",
    "First day at a new school",
    "Failed an important test or assignment",
    "Had an argument with parents about independence",
    "Experiencing cyberbullying on social media",
    "Dealing with peer pressure to try drugs/alcohol",
    "Feeling left out from a friend group",
    "Struggling with body image and appearance",
    "Facing college application stress",
    "Custom scenario"
]

# ================================
# 增强版数据监控系统
# ================================

class EnhancedJSONDataMonitor:
    def __init__(self):
        self.data_file = 'monitoring_data.json'
        self.github_enabled = self.setup_github()
        self.data = self.load_data()
        self.operation_count = 0
        self.save_frequency = 1  # 每次对话都保存
    
    def setup_github(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.github_repo = os.environ.get("GITHUB_REPO")
        self.github_branch = os.environ.get("GITHUB_BRANCH", "main")
        enabled = bool(self.github_token and self.github_repo)
        if enabled:
            print("✅ GitHub sync enabled for data monitoring")
        else:
            print("📁 Using local file storage only")
        return enabled
    
    def load_data(self):
        if self.github_enabled:
            self.download_from_github()
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded monitoring data: {len(data.get('conversations', []))} conversations")
                    return data
            except Exception as e:
                print(f"❌ Error loading data: {e}")
        
        empty_data = {
            'sessions': {},
            'conversations': [],
            'user_actions': [],
            'system_metrics': [],
            'last_updated': datetime.datetime.now().isoformat(),
            'version': '2.0',
            'summary': {
                'total_conversations': 0,
                'total_users': 0,
                'most_active_student': None,
                'total_messages': 0
            }
        }
        
        self.save_data_to_file(empty_data)
        print("📝 Created new monitoring data file")
        return empty_data
    
    def get_student_name(self, student_id):
        return name_dict.get(student_id, "Unknown")
    
    def log_conversation(self, session_id, student_id, user_message, ai_response, 
                        scene_context="", response_time_ms=0):
        conversation = {
            'id': len(self.data['conversations']) + 1,
            'session_id': session_id,
            'student_id': student_id,
            'student_name': self.get_student_name(student_id),
            'user_message': user_message[:2000],
            'ai_response': ai_response[:3000],
            'scene_context': scene_context,
            'timestamp': datetime.datetime.now().isoformat(),
            'response_time_ms': response_time_ms,
            'message_length': len(user_message),
            'day_of_week': datetime.datetime.now().strftime('%A'),
            'hour': datetime.datetime.now().hour,
            'conversation_turn': self.get_conversation_turn(session_id, student_id)
        }
        
        self.data['conversations'].append(conversation)
        
        if session_id in self.data['sessions']:
            self.data['sessions'][session_id]['total_messages'] += 1
            self.data['sessions'][session_id]['last_activity'] = datetime.datetime.now().isoformat()
        
        self.update_summary()
        self.save_data()
    
    def get_conversation_turn(self, session_id, student_id):
        conversations = [c for c in self.data['conversations'] 
                        if c['session_id'] == session_id and c['student_id'] == student_id]
        return len(conversations) + 1
    
    def update_summary(self):
        conversations = self.data['conversations']
        if not conversations:
            return
            
        student_counts = {}
        for conv in conversations:
            student_id = conv['student_id']
            student_counts[student_id] = student_counts.get(student_id, 0) + 1
        
        most_active_student_id = max(student_counts.items(), key=lambda x: x[1])[0] if student_counts else None
        most_active_student = self.get_student_name(most_active_student_id) if most_active_student_id else None
        
        self.data['summary'] = {
            'total_conversations': len(conversations),
            'total_users': len(self.data['sessions']),
            'most_active_student': most_active_student,
            'total_messages': len(conversations),
            'last_24h_conversations': len([c for c in conversations 
                                         if (datetime.datetime.now() - datetime.datetime.fromisoformat(c['timestamp'])).days < 1])
        }
    
    def export_to_csv(self):
        output = StringIO()
        if self.data['conversations']:
            fieldnames = ['id', 'timestamp', 'student_name', 'session_id', 
                         'user_message', 'ai_response', 'scene_context', 
                         'response_time_ms', 'conversation_turn', 'day_of_week', 'hour']
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for conv in self.data['conversations']:
                row = {key: conv.get(key, '') for key in fieldnames}
                writer.writerow(row)
        
        return output.getvalue()
    
    def get_analytics_dashboard_data(self):
        conversations = self.data['conversations']
        if not conversations:
            return {
                'student_stats': {},
                'hourly_distribution': {},
                'total_conversations': 0,
                'total_sessions': 0,
                'summary': {}
            }
        
        student_stats = {}
        for conv in conversations:
            student = conv['student_name']
            if student not in student_stats:
                student_stats[student] = {
                    'total_conversations': 0,
                    'avg_response_time': 0,
                    'total_response_time': 0
                }
            
            student_stats[student]['total_conversations'] += 1
            student_stats[student]['total_response_time'] += conv.get('response_time_ms', 0)
        
        for student, stats in student_stats.items():
            if stats['total_conversations'] > 0:
                stats['avg_response_time'] = stats['total_response_time'] / stats['total_conversations']
        
        hourly_distribution = {}
        for conv in conversations:
            hour = conv.get('hour', 0)
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
        
        return {
            'student_stats': student_stats,
            'hourly_distribution': hourly_distribution,
            'total_conversations': len(conversations),
            'total_sessions': len(self.data['sessions']),
            'summary': self.data.get('summary', {})
        }
    
    def save_data_to_file(self, data=None):
        if data is None:
            data = self.data
        data['last_updated'] = datetime.datetime.now().isoformat()
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 Data saved: {len(data.get('conversations', []))} conversations")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def save_data(self, force_upload=False):
        self.operation_count += 1
        self.save_data_to_file()
        if self.github_enabled and (self.operation_count % self.save_frequency == 0 or force_upload):
            self.upload_to_github()
    
    def download_from_github(self):
        if not self.github_enabled:
            return False
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{self.data_file}"
            headers = {'Authorization': f'token {self.github_token}', 'Accept': 'application/vnd.github.v3+json'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.json()
                import base64
                file_content = base64.b64decode(content['content']).decode('utf-8')
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print("✅ Downloaded latest data from GitHub")
                return True
            elif response.status_code == 404:
                print("📁 No existing data file in GitHub")
                return False
        except Exception as e:
            print(f"⚠️ Failed to download from GitHub: {e}")
        return False
    
    def upload_to_github(self):
        if not self.github_enabled:
            return False
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                content = f.read()
            import base64
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{self.data_file}"
            headers = {'Authorization': f'token {self.github_token}', 'Accept': 'application/vnd.github.v3+json'}
            
            get_response = requests.get(url, headers=headers, timeout=10)
            sha = None
            if get_response.status_code == 200:
                sha = get_response.json()['sha']
            
            data = {
                'message': f'Update chat monitoring data - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'content': encoded_content,
                'branch': self.github_branch
            }
            if sha:
                data['sha'] = sha
            
            response = requests.put(url, headers=headers, json=data, timeout=15)
            if response.status_code in [200, 201]:
                print("✅ Data uploaded to GitHub successfully")
                return True
        except Exception as e:
            print(f"❌ Error uploading to GitHub: {e}")
        return False
    
    def create_session(self, request_info=None):
        session_id = str(uuid.uuid4())
        session_data = {
            'session_id': session_id,
            'ip_address': request.remote_addr if request else 'unknown',
            'user_agent': request.headers.get('User-Agent', 'unknown') if request else 'unknown',
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': None,
            'total_messages': 0,
            'last_activity': datetime.datetime.now().isoformat()
        }
        self.data['sessions'][session_id] = session_data
        self.save_data()
        print(f"📝 New session created: {session_id}")
        return session_id
    
    def log_user_action(self, session_id, action_type, action_data=None):
        action = {
            'id': len(self.data['user_actions']) + 1,
            'session_id': session_id,
            'action_type': action_type,
            'action_data': action_data,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.data['user_actions'].append(action)
        self.save_data()

monitor = EnhancedJSONDataMonitor()

# ================================
# 提示加载函数
# ================================

def load_shared_prompt():
    try:
        with open("shared_prompt.txt", "r") as f:
            return f.read().strip()
    except:
        return "You are a helpful digital assistant roleplaying as a teen student."

def load_prompts():
    shared_prompt = load_shared_prompt()
    prompts = {}
    for i in range(1, 11):
        path = f"prompts/{i}.json"
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                    prompts[f"student{i:03d}"] = shared_prompt + "\n\n" + data["prompt"]
        except:
            prompts[f"student{i:03d}"] = shared_prompt + f"\n\nYou are student {i}."
    return prompts

all_prompts = load_prompts()

# ================================
# Flask路由定义
# ================================

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = monitor.create_session()
    
    characters = []
    for student_id, name in name_dict.items():
        characters.append({
            'id': student_id,
            'name': name,
            'description': student_descriptions[student_id],
            'avatar': f"avatar/{student_id}.png"
        })
    
    return render_template('index.html', characters=characters)

@app.route('/chat/<student_id>')
def chat_page(student_id):
    if student_id not in name_dict:
        return redirect('/')
    
    if 'session_id' not in session:
        session['session_id'] = monitor.create_session()
    
    monitor.log_user_action(session['session_id'], "student_select", {"student_id": student_id})
    
    student = {
        'id': student_id,
        'name': name_dict[student_id],
        'profile': student_profiles.get(student_id, {}),
        'avatar': f"avatar/{student_id}.png"
    }
    
    return render_template('chat.html', 
                         student=student,
                         scene_options=scene_options)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.json
        message = data.get('message', '').strip()
        student_id = data.get('student_id', 'student001')
        scene_context = data.get('scene_context', '')
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        if not os.environ.get("OPENAI_API_KEY"):
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        session_id = session.get('session_id')
        if not session_id:
            session_id = monitor.create_session()
            session['session_id'] = session_id
        
        base_prompt = all_prompts.get(student_id, "You are a helpful assistant.")
        if scene_context:
            system_prompt = base_prompt + f"\n\nCurrent scenario context: {scene_context}"
        else:
            system_prompt = base_prompt
        
        chat_history = session.get(f'history_{student_id}', [])
        
        messages = [{"role": "system", "content": system_prompt}]
        for user_msg, bot_reply in chat_history[-10:]:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_reply})
        messages.append({"role": "user", "content": message})
        
        start_time = datetime.datetime.now()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip()
        response_time_ms = (datetime.datetime.now() - start_time).total_seconds() * 1000
        
        chat_history.append([message, reply])
        session[f'history_{student_id}'] = chat_history
        
        monitor.log_conversation(
            session_id=session_id,
            student_id=student_id,
            user_message=message,
            ai_response=reply,
            scene_context=scene_context,
            response_time_ms=response_time_ms
        )
        
        return jsonify({
            'success': True,
            'reply': reply,
            'student_name': name_dict.get(student_id, 'Student')
        })
        
    except Exception as e:
        error_msg = str(e)
        if 'session_id' in locals():
            monitor.log_user_action(session_id, "api_error", {"error": error_msg})
        
        if "insufficient_quota" in error_msg:
            user_error = "OpenAI API quota exceeded. Please check your API usage."
        elif "invalid_api_key" in error_msg:
            user_error = "Invalid OpenAI API key. Please check configuration."
        elif "rate_limit" in error_msg:
            user_error = "API rate limit exceeded. Please try again in a moment."
        else:
            user_error = f"Service temporarily unavailable: {error_msg}"
        
        return jsonify({'error': user_error}), 500

@app.route('/api/clear_chat', methods=['POST'])
def clear_chat():
    data = request.json
    student_id = data.get('student_id', 'student001')
    
    if 'session_id' in session:
        monitor.log_user_action(session['session_id'], "clear_chat", {"student_id": student_id})
    
    session[f'history_{student_id}'] = []
    return jsonify({'success': True})

@app.route('/api/test')
def test_api():
    return jsonify({
        'status': 'ok',
        'openai_configured': bool(os.environ.get("OPENAI_API_KEY")),
        'secret_key_configured': bool(os.environ.get("SECRET_KEY")),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/get_chat_history/<student_id>')
def get_chat_history(student_id):
    history = session.get(f'history_{student_id}', [])
    return jsonify({'history': history})

# ================================
# 管理员路由
# ================================

def generate_admin_dashboard_html(analytics_data):
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Chat Data Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { background: #4a90e2; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats { display: flex; flex-wrap: wrap; gap: 20px; }
        .stat-item { flex: 1; min-width: 200px; background: #e8f4fd; padding: 15px; border-radius: 5px; }
        .stat-number { font-size: 2em; font-weight: bold; color: #4a90e2; }
        .student-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .student-card { background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #4a90e2; }
        .btn { background: #4a90e2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 5px 0 0; }
        .btn:hover { background: #357abd; }
        .logout { float: right; background: #ff6b6b; }
        .logout:hover { background: #ff5252; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; font-weight: bold; }
        .message-preview { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Chat Data Monitor Dashboard</h1>
            <p>Real-time monitoring of all chat interactions</p>
            <a href="/admin/logout" class="btn logout">Logout</a>
        </div>
        
        <div class="card">
            <h2>📊 Overview Statistics</h2>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">''' + str(analytics_data['total_conversations']) + '''</div>
                    <div>Total Conversations</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">''' + str(analytics_data['total_sessions']) + '''</div>
                    <div>Total Sessions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">''' + str(analytics_data['summary'].get('last_24h_conversations', 0)) + '''</div>
                    <div>Last 24h Conversations</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">''' + str(analytics_data['summary'].get('most_active_student', 'N/A')) + '''</div>
                    <div>Most Active Student</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>👥 Student Activity</h2>
            <div class="student-stats">'''
    
    for student, stats in analytics_data['student_stats'].items():
        html_content += f'''
                <div class="student-card">
                    <h4>{student}</h4>
                    <p><strong>Conversations:</strong> {stats['total_conversations']}</p>
                    <p><strong>Avg Response Time:</strong> {stats['avg_response_time']:.0f}ms</p>
                </div>'''
    
    html_content += '''
            </div>
        </div>
        
        <div class="card">
            <h2>📈 Recent Conversations</h2>
            <table>
                <tr>
                    <th>Time</th>
                    <th>Student</th>
                    <th>User Message</th>
                    <th>AI Response</th>
                    <th>Scene</th>
                </tr>'''
    
    recent_conversations = sorted(monitor.data.get('conversations', []), 
                                key=lambda x: x['timestamp'], reverse=True)[:10]
    
    for conv in recent_conversations:
        timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%m/%d %H:%M')
        html_content += f'''
                <tr>
                    <td>{timestamp}</td>
                    <td>{conv['student_name']}</td>
                    <td class="message-preview">{conv['user_message'][:100]}...</td>
                    <td class="message-preview">{conv['ai_response'][:100]}...</td>
                    <td>{conv.get('scene_context', 'None')[:30]}</td>
                </tr>'''
    
    html_content += '''
            </table>
        </div>
        
        <div class="card">
            <h2>🔧 Data Export</h2>
            <p>Export all conversation data for analysis:</p>
            <a href="/admin/export/csv" class="btn">Download CSV</a>
            <a href="/admin/data/raw" class="btn">View Raw JSON</a>
            <a href="/admin/conversations" class="btn">View All Conversations</a>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

@app.route('/admin')
def admin_dashboard():
    if session.get('admin_authenticated') != True:
        return redirect('/admin/login')
    
    analytics_data = monitor.get_analytics_dashboard_data()
    return generate_admin_dashboard_html(analytics_data)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        
        if password == admin_password:
            session['admin_authenticated'] = True
            return redirect('/admin')
        else:
            error_message = "Invalid password. Please try again."
    else:
        error_message = ""
    
    login_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-form { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; width: 100%; }
        .login-form h2 { text-align: center; margin-bottom: 30px; color: #4a90e2; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { background: #4a90e2; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; }
        .btn:hover { background: #357abd; }
        .error { color: #ff6b6b; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>🔐 Admin Login</h2>
        <form method="post">
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Login</button>''' + (f'<p class="error">{error_message}</p>' if error_message else '') + '''
        </form>
    </div>
</body>
</html>'''
    
    return login_html

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect('/admin/login')

@app.route('/admin/export/csv')
def export_csv():
    if session.get('admin_authenticated') != True:
        return redirect('/admin/login')
    
    csv_data = monitor.export_to_csv()
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=chat_data_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )

@app.route('/admin/data/raw')
def raw_data():
    if session.get('admin_authenticated') != True:
        return redirect('/admin/login')
    
    return jsonify(monitor.data)

@app.route('/admin/conversations')
def view_conversations():
    if session.get('admin_authenticated') != True:
        return redirect('/admin/login')
    
    conversations = monitor.data.get('conversations', [])
    conversations.sort(key=lambda x: x['timestamp'], reverse=True)
    
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>All Conversations</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: #4a90e2; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .conversation { background: white; margin: 10px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .conv-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        .student-name { font-size: 18px; font-weight: bold; color: #4a90e2; }
        .timestamp { color: #666; font-size: 14px; }
        .message-pair { margin: 15px 0; }
        .user-message { background: #f0f8ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #4a90e2; }
        .ai-message { background: #f9f9f9; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; }
        .scene-context { background: #fff3cd; padding: 10px; border-radius: 4px; margin-top: 10px; font-style: italic; }
        .btn { background: #4a90e2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
        .btn:hover { background: #357abd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 All Conversations</h1>
            <a href="/admin" class="btn">← Back to Dashboard</a>
        </div>'''
    
    for conv in conversations:
        timestamp = datetime.datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        html_content += f'''
        <div class="conversation">
            <div class="conv-header">
                <span class="student-name">{conv['student_name']}</span>
                <span class="timestamp">{timestamp} | Session: {conv['session_id'][:8]}... | Turn: {conv.get('conversation_turn', 'N/A')}</span>
            </div>
            <div class="message-pair">
                <div class="user-message">
                    <strong>👤 User:</strong><br>{conv['user_message']}
                </div>
                <div class="ai-message">
                    <strong>🤖 {conv['student_name']}:</strong><br>{conv['ai_response']}
                </div>
                {f'<div class="scene-context"><strong>🎬 Scene:</strong> {conv["scene_context"]}</div>' if conv.get('scene_context') else ''}
            </div>
        </div>'''
    
    html_content += '''
    </div>
</body>
</html>'''
    
    return html_content

if __name__ == '__main__':
    print("🔍 Enhanced data monitoring system started")
    print("📊 Starting Flask server...")
    
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    
    if os.environ.get("RENDER"):
        print(f"🚀 Running in production mode on port {port}")
    else:
        print(f"🔧 Running in development mode on port {port}")
        app.run(host="0.0.0.0", port=port, debug=debug)
