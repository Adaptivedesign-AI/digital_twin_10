import gradio as gr
import json
import os
import sqlite3
import datetime
import uuid
from openai import OpenAI
from custom_css import custom_css  # Import the custom CSS from separate file
from typing import Dict, List, Any
import requests

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))

# 在你的 app.py 中，找到数据监控相关部分，替换为以下代码：

# ================================
# JSON数据监控系统
# ================================


class JSONDataMonitor:
    def __init__(self):
        self.data_file = 'monitoring_data.json'
        self.github_enabled = self.setup_github()
        self.data = self.load_data()
        
        # 定期保存计数器（每5次操作保存一次）
        self.operation_count = 0
        self.save_frequency = 5
    
    def setup_github(self):
        """设置GitHub数据同步（可选）"""
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.github_repo = os.environ.get("GITHUB_REPO")  # 格式: "username/repo"
        self.github_branch = os.environ.get("GITHUB_BRANCH", "main")
        
        enabled = bool(self.github_token and self.github_repo)
        if enabled:
            print("✅ GitHub sync enabled")
        else:
            print("📁 Using local file storage only")
        return enabled
    
    def load_data(self):
        """加载数据"""
        # 首先尝试从GitHub下载最新数据
        if self.github_enabled:
            self.download_from_github()
        
        # 加载本地数据
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded {len(data.get('conversations', []))} conversations from {self.data_file}")
                    return data
            except Exception as e:
                print(f"❌ Error loading data: {e}")
        
        # 返回空数据结构
        empty_data = {
            'sessions': {},
            'conversations': [],
            'user_actions': [],
            'system_metrics': [],
            'last_updated': datetime.datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # 创建初始文件
        self.save_data_to_file(empty_data)
        print("📝 Created new monitoring data file")
        return empty_data
    
    def save_data_to_file(self, data=None):
        """保存数据到文件"""
        if data is None:
            data = self.data
            
        data['last_updated'] = datetime.datetime.now().isoformat()
        
        try:
            # 保存到本地
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Data saved locally ({len(data.get('conversations', []))} conversations)")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def save_data(self, force_upload=False):
        """智能保存数据"""
        self.operation_count += 1
        
        # 总是保存到本地
        self.save_data_to_file()
        
        # 每隔几次操作或强制时上传到GitHub
        if self.github_enabled and (self.operation_count % self.save_frequency == 0 or force_upload):
            self.upload_to_github()
    
    def download_from_github(self):
        """从GitHub下载数据文件"""
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
                
                print("✅ Downloaded latest data from GitHub")
                return True
            elif response.status_code == 404:
                print("📁 No existing data file in GitHub (will create new)")
                return False
            else:
                print(f"⚠️ GitHub download failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Failed to download from GitHub: {e}")
        
        return False
    
    def upload_to_github(self):
        """上传数据文件到GitHub"""
        if not self.github_enabled:
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import base64
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            # 获取当前文件的SHA（如果存在）
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{self.data_file}"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            get_response = requests.get(url, headers=headers, timeout=10)
            sha = None
            if get_response.status_code == 200:
                sha = get_response.json()['sha']
            
            # 上传文件
            data = {
                'message': f'Update monitoring data - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'content': encoded_content,
                'branch': self.github_branch
            }
            
            if sha:
                data['sha'] = sha
            
            response = requests.put(url, headers=headers, json=data, timeout=15)
            if response.status_code in [200, 201]:
                print("✅ Uploaded data to GitHub")
                return True
            else:
                print(f"❌ GitHub upload failed: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"❌ Error uploading to GitHub: {e}")
        
        return False
    
    def create_session(self, request_info=None):
        """创建新的用户会话"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': session_id,
            'ip_address': request_info.get('ip', 'unknown') if request_info else 'unknown',
            'user_agent': request_info.get('user_agent', 'unknown') if request_info else 'unknown',
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': None,
            'total_messages': 0
        }
        
        self.data['sessions'][session_id] = session_data
        self.save_data()
        
        print(f"📝 New session created: {session_id}")
        return session_id
    
    def log_conversation(self, session_id, student_id, user_message, ai_response, 
                        scene_context="", response_time_ms=0):
        """记录对话数据"""
        conversation = {
            'id': len(self.data['conversations']) + 1,
            'session_id': session_id,
            'student_id': student_id,
            'user_message': user_message[:1000],  # 限制长度防止文件过大
            'ai_response': ai_response[:2000],
            'scene_context': scene_context,
            'timestamp': datetime.datetime.now().isoformat(),
            'response_time_ms': response_time_ms,
            'message_length': len(user_message)
        }
        
        self.data['conversations'].append(conversation)
        
        # 更新会话消息计数
        if session_id in self.data['sessions']:
            self.data['sessions'][session_id]['total_messages'] += 1
        
        self.save_data()
        print(f"💬 Conversation logged: {session_id} -> {student_id}")
    
    def log_user_action(self, session_id, action_type, action_data=None):
        """记录用户行为"""
        action = {
            'id': len(self.data['user_actions']) + 1,
            'session_id': session_id,
            'action_type': action_type,
            'action_data': action_data,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.data['user_actions'].append(action)
        self.save_data()
        print(f"🎯 User action logged: {action_type}")
    
    def log_system_metric(self, metric_type, metric_value, details=""):
        """记录系统指标"""
        metric = {
            'id': len(self.data['system_metrics']) + 1,
            'metric_type': metric_type,
            'metric_value': metric_value,
            'details': details,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.data['system_metrics'].append(metric)
        self.save_data()
        print(f"📊 System metric logged: {metric_type} = {metric_value}")
    
    def cleanup_old_data(self, days_to_keep=30):
        """清理旧数据（可选）"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
        
        # 清理旧对话
        original_count = len(self.data['conversations'])
        self.data['conversations'] = [
            conv for conv in self.data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) > cutoff_date
        ]
        
        cleaned_count = original_count - len(self.data['conversations'])
        if cleaned_count > 0:
            print(f"🧹 Cleaned {cleaned_count} old conversations")
            self.save_data(force_upload=True)

# 替换原来的monitor实例
monitor = JSONDataMonitor()



# ================================
# Original Application Logic
# ================================

# Load the shared prompt that will be used as a base for all student interactions
def load_shared_prompt():
    try:
        with open("shared_prompt.txt", "r") as f:
            return f.read().strip()
    except:
        # Fallback if file doesn't exist
        return "You are a helpful digital assistant roleplaying as a teen student."

shared_prompt = load_shared_prompt()

# Load individual student prompts and combine them with the shared prompt
def load_prompts():
    """
    Load all individual student prompts and combine them with the shared prompt.
    Returns a dictionary with student IDs as keys and complete prompts as values.
    """
    prompts = {}
    for i in range(1, 11):
        path = f"prompts/{i}.json"
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                    prompts[f"student{i:03d}"] = shared_prompt + "\n\n" + data["prompt"]
        except:
            # Fallback if file doesn't exist or can't be read
            prompts[f"student{i:03d}"] = shared_prompt + f"\n\nYou are student {i}."
    return prompts

# Initialize the prompts dictionary
all_prompts = load_prompts()

# Define student ID to name mapping for display purposes
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

# Define student descriptions to provide context about each persona
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

# Define detailed student profiles based on REAL data from CSV (no fictional hobbies)
student_profiles = {
    "student001": {  # Jaden
        "age": 14,
        "sex": "Male", 
        "race_ethnicity": "Hispanic/Latino, Black or African American",
        "grade": "9th grade",
        "emotional_health": "Experienced threats with weapons at school but did not engage in physical fights. Carries weapon for protection some days.",
        "mental_health": "No depression or suicidal ideation. Not bullied. Has some alcohol use (1-2 days/month). Started drinking early (age 9-10)."
    },
    "student002": {  # Ethan
        "age": 16,
        "sex": "Male",
        "race_ethnicity": "Hispanic/Latino, White", 
        "grade": "11th grade",
        "emotional_health": "Generally stable social relationships. No history of violence or threats.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. Moderate alcohol use (3-5 days/month)."
    },
    "student003": {  # Emily
        "age": 14,
        "sex": "Female",
        "race_ethnicity": "Asian",
        "grade": "9th grade",
        "emotional_health": "Experiences both school and electronic bullying. Socially vulnerable.",
        "mental_health": "Reports feeling sad or hopeless for extended periods. Experiences bullying both in-person and online."
    },
    "student004": {  # Malik
        "age": 13,
        "sex": "Male",
        "race_ethnicity": "Black or African American",
        "grade": "9th grade",
        "emotional_health": "Stable social environment, no bullying or violence exposure.",
        "mental_health": "No depression or suicidal ideation. Not bullied. Some alcohol use (1-2 days/month)."
    },
    "student005": {  # Aaliyah
        "age": 15,
        "sex": "Female", 
        "race_ethnicity": "Black or African American",
        "grade": "9th grade",
        "emotional_health": "Not bullied, stable peer relationships.",
        "mental_health": "Reports periods of sadness or hopelessness. No substance use reported."
    },
    "student006": {  # Brian
        "age": 17,
        "sex": "Male",
        "race_ethnicity": "Asian",
        "grade": "11th grade",
        "emotional_health": "Stable social environment, no violence or bullying.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    },
    "student007": {  # Grace
        "age": 16,
        "sex": "Female",
        "race_ethnicity": "Asian", 
        "grade": "10th grade",
        "emotional_health": "Stable peer relationships, no bullying or violence.",
        "mental_health": "No depression or suicidal ideation. Not bullied. No substance use reported."
    },
    "student008": {  # Brianna
        "age": 15,
        "sex": "Female",
        "race_ethnicity": "Mixed race (Black or African American, White)",
        "grade": "9th grade",
        "emotional_health": "Stable social environment, no bullying or threats.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    },
    "student009": {  # Leilani
        "age": 17,
        "sex": "Female",
        "race_ethnicity": "Mixed race (Native Hawaiian/Pacific Islander, White)",
        "grade": "12th grade",
        "emotional_health": "Stable peer relationships, no violence or bullying exposure.",
        "mental_health": "No depression or suicidal ideation. Not bullied. No substance use reported."
    },
    "student010": {  # Tyler
        "age": 16,
        "sex": "Male", 
        "race_ethnicity": "Mixed race (Native Hawaiian/Pacific Islander, White)",
        "grade": "10th grade",
        "emotional_health": "Stable social environment, no bullying or violence.",
        "mental_health": "No depression or suicidal thoughts. Not bullied. No substance use."
    }
}

# Predefined scene options for the scene description box
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
    "Custom scenario (describe below)"
]

# Create a function to initialize empty chat history for all students
def get_empty_history_dict():
    """
    Initialize an empty chat history dictionary for all students.
    This ensures we can track conversations with each student separately.
    """
    return {student_id: [] for student_id in name_dict.keys()}

# Core chat function that handles message processing and AI responses with monitoring
def chat(message, history, student_id, history_dict, scene_description, session_id):
    """
    Process user messages and generate AI responses with monitoring.
    
    Args:
        message: The user's input message
        history: Current chat history for the selected student
        student_id: ID of the currently selected student
        history_dict: Dictionary containing all students' chat histories
        scene_description: Current scene context for the conversation
        session_id: User session ID for monitoring
        
    Returns:
        Empty message input, updated history, and updated history_dict
    """
    start_time = datetime.datetime.now()
    
    # Check for empty messages
    if not message or not message.strip():
        return "", history, history_dict
    
    # Log user message sending action
    monitor.log_user_action(session_id, "send_message", {
        "student_id": student_id,
        "message_length": len(message),
        "scene": scene_description
    })
        
    # Get the appropriate system prompt for the selected student
    base_prompt = all_prompts.get(student_id, "You are a helpful assistant.")
    
    # Add scene context if provided
    if scene_description and scene_description.strip():
        system_prompt = base_prompt + f"\n\nCurrent scenario context: {scene_description.strip()}"
    else:
        system_prompt = base_prompt

    # Format messages for the OpenAI API
    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, bot_reply in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_reply})
    messages.append({"role": "user", "content": message})

    try:
        # Generate response using OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        
        # Calculate response time
        end_time = datetime.datetime.now()
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Log conversation to database
        monitor.log_conversation(
            session_id=session_id,
            student_id=student_id,
            user_message=message,
            ai_response=reply,
            scene_context=scene_description,
            response_time_ms=response_time_ms
        )
        
        # Log successful API call
        monitor.log_system_metric("api_call_success", response_time_ms, 
                                 f"Model: gpt-4o-mini, Student: {student_id}")
        
        # Update conversation history
        history.append([message, reply])
        history_dict[student_id] = history
        return "", history, history_dict
        
    except Exception as e:
        # Log API error
        monitor.log_system_metric("api_call_error", 0, str(e))
        
        # Handle API errors gracefully
        error_message = f"⚠️ Error: {str(e)}"
        history.append([message, error_message])
        history_dict[student_id] = history
        return "", history, history_dict

# Function to clear chat history for the current student
def clear_current_chat(student_id, history_dict, session_id):
    """
    Clear the chat history for the currently selected student.
    
    Args:
        student_id: ID of the currently selected student
        history_dict: Dictionary containing all students' chat histories
        session_id: User session ID for monitoring
        
    Returns:
        Empty history list and updated history_dict
    """
    # Log clear chat action
    monitor.log_user_action(session_id, "clear_chat", {"student_id": student_id})
    
    history_dict[student_id] = []
    return [], history_dict

# Function to update student profile display
def update_student_profile(student_id):
    """
    Update the student profile display based on selected student.
    
    Args:
        student_id: ID of the selected student
        
    Returns:
        Updated profile information
    """
    if student_id not in student_profiles:
        return "", "", ""
    
    student_name = name_dict.get(student_id, "Unknown")
    profile = student_profiles[student_id]
    
    # Create profile overview text
    profile_text = f"""
**Age:** {profile['age']}  
**Sex:** {profile['sex']}  
**Race/Ethnicity:** {profile['race_ethnicity']}  
**Grade:** {profile['grade']}  
**Emotional Health:** {profile['emotional_health']}  
**Mental Health:** {profile['mental_health']}
    """.strip()
    
    # Update student name and profile
    return f"# {student_name}", profile_text, f"avatar/{student_id}.png"

# Function to handle direct student selection and switch to chat interface
def select_student_direct(student_id, history_dict, session_id):
    """
    Handle direct student selection and switch to chat interface with monitoring.
    
    Args:
        student_id: ID of the selected student
        history_dict: Dictionary containing all students' chat histories
        session_id: User session ID for monitoring
        
    Returns:
        UI updates to show chat interface with selected student info
    """
    # If no session_id, create a new one
    if not session_id:
        session_id = monitor.create_session()
    
    # Log student selection action
    monitor.log_user_action(session_id, "student_select", {"student_id": student_id})
    
    student_history = history_dict.get(student_id, [])
    student_name, profile_text, profile_image = update_student_profile(student_id)
    
    # Debug print for server logs
    print(f"Selecting student: {student_id}, Name: {student_name}, Session: {session_id}")
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected student ID
        student_name,              # Update student name display
        profile_text,              # Update profile text
        profile_image,             # Update profile image
        student_history,           # Update chat history
        session_id                 # Return session_id
    )

# Function to return to the student selection page
def return_to_selection(session_id):
    """
    Return to the student selection page from the chat interface.
    
    Args:
        session_id: User session ID for monitoring
        
    Returns:
        UI updates to show selection page and hide chat page
    """
    # Log return to selection action
    monitor.log_user_action(session_id, "back_to_selection", {})
    
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

# Function to update scene description based on dropdown selection
def update_scene_description(selected_scene, custom_description, session_id):
    """
    Update scene description based on dropdown selection.
    
    Args:
        selected_scene: Selected scene from dropdown
        custom_description: Custom description if "Custom scenario" is selected
        session_id: User session ID for monitoring
        
    Returns:
        Updated scene description
    """
    # Log scene change action
    monitor.log_user_action(session_id, "scene_change", {
        "selected_scene": selected_scene,
        "is_custom": selected_scene == "Custom scenario (describe below)"
    })
    
    if selected_scene == "Custom scenario (describe below)":
        return custom_description
    elif selected_scene == "Posted a video on TikTok and received hateful comments":
        return "Posted a short video on TikTok. Anonymous users flooded the comments with anti-Asian slurs and told her to 'go back where you came from.' The twin deleted the post and now feels afraid to post anything."
    else:
        return selected_scene

# Function to initialize session
def initialize_session():
    """Create new user session"""
    session_id = monitor.create_session()
    print(f"New session created: {session_id}")
    return session_id

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(css=custom_css, title="Digital Twins") as demo:

    # Initialize state to track history and selected student
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    session_id_state = gr.State("")  # New: session ID state
    
    # Create both pages as components for switching between them
    selection_page = gr.Group(visible=True)
    chat_page = gr.Group(visible=False)
    
    # Define chat page components with two-column layout
    with chat_page:
        # Header with back button
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back to Selection", elem_classes="back-btn")
            gr.Markdown("# Digital Twin Chat Interface", elem_classes="page-title")
        
        # Main content: Two-column layout
        with gr.Row(elem_classes="main-chat-container"):
            # Left column: Chat interface (MUST BE FIRST)
            with gr.Column(scale=65, elem_classes="chat-column"):
                gr.Markdown("## Chat with Digital Twin", elem_classes="chat-title")
                
                # Chat area with avatars for user/bot distinction
                chatbot = gr.Chatbot(
                    label="Conversation",
                    avatar_images=("avatar/user.png", None),
                    height=850,  
                    elem_classes="character-ai-style chatbox-container",
                    show_label=True,
                    show_copy_button=True,
                    bubble_full_width=True,
                )
                
                # Input area with improved layout
                with gr.Row():
                    with gr.Column(scale=5):
                        msg = gr.Textbox(
                            placeholder="Type your message...",
                            label="",
                            elem_classes="message-input",
                        )
                    
                    with gr.Column(scale=1, elem_classes="button-container"):
                        send_btn = gr.Button("Send", elem_classes="send-btn")
                        clear_btn = gr.Button("Clear", elem_classes="clear-btn")
            
            # Right column: Student info and scene controls (MUST BE SECOND)
            with gr.Column(scale=35, elem_classes="info-column"):
                # Top box: Student profile
                with gr.Group(elem_classes="profile-box"):
                    student_name_display = gr.Markdown("# Student Name", elem_classes="profile-name")
                    with gr.Row():
                        with gr.Column(scale=2):
                            student_profile_image = gr.Image(
                                value="avatar/student001.png",
                                show_label=False,
                                elem_classes="profile-image",
                                height=120
                            )
                        with gr.Column(scale=3):
                            student_profile_text = gr.Markdown("Profile information will appear here.", elem_classes="profile-text")
                
                # Middle box: Instructions and disclaimer
                with gr.Group(elem_classes="instructions-box"):
                    gr.Markdown("### Instructions & Disclaimer", elem_classes="section-title")
                    instructions_text = gr.Markdown(
                        "You will be able to interact with **[Student Name]**, an AI-based digital adolescent. "
                        "We kindly ask you to please keep the conversation respectful and appropriate. "
                        "Remember that this is a simulation designed for research and educational purposes.",
                        elem_classes="instructions-text"
                    )
                
                # Bottom box: Scene description
                with gr.Group(elem_classes="scene-box"):
                    gr.Markdown("### Scene Context", elem_classes="section-title")
                    gr.Markdown("Set a scenario to provide context for your conversation:", elem_classes="scene-instruction")
                    
                    scene_dropdown = gr.Dropdown(
                        choices=scene_options,
                        value="Meet with a new friend for the first time",
                        label="Select a scenario",
                        elem_classes="scene-dropdown"
                    )
                    
                    custom_scene_input = gr.Textbox(
                        placeholder="Describe your custom scenario here...",
                        label="Custom Scenario (if selected above)",
                        elem_classes="custom-scene-input",
                        visible=False
                    )
                    
                    scene_description = gr.Textbox(
                        value="Meet with a new friend for the first time",
                        label="Current Scene Context",
                        elem_classes="scene-description",
                        interactive=False
                    )
    
    # Define selection page with responsive grid
    with selection_page:
        with gr.Column(elem_classes="container"):
            # Title image with transparent background
            with gr.Column(elem_classes="header-image-container"):
                gr.Image(
                    value="avatar/brain_with_title.png",
                    show_label=False,
                    elem_classes="header-image",
                    height=120,
                    container=False,
                )
            
            gr.Markdown("### Choose a digital adolescent to chat with", elem_classes="selection-heading")
            gr.Markdown("*These digital adolescents are AI-powered digital twins of real-world teens, designed to enable data-driven simulations of risk trajectories and intervention outcomes. The platform is developed and maintained by the UC Berkeley team. For inquiries or questions, please contact jingshenwang@berkeley.edu.*", elem_classes="project-description")
            
            # Create a responsive grid for all students
            with gr.Column(elem_classes="character-grid"):
                for i in range(0, 10):
                    student_id = f"student{i+1:03d}"
                    student_name = name_dict[student_id]
                    
                    with gr.Column(elem_classes="character-card"):
                        # Avatar container - circular and centered
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
                            )
                        
                        # Student name - prominent and bold
                        gr.Markdown(f"## {student_name}", elem_classes="student-name")
                        gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                        
                        chat_btn = gr.Button("Start Chat", elem_classes="chat-btn", elem_id=f"chat-btn-{student_id}")
                        chat_btn.click(
                            select_student_direct,
                            inputs=[
                                gr.Textbox(value=student_id, visible=False),
                                history_dict_state,
                                session_id_state
                            ],
                            outputs=[
                                selection_page, 
                                chat_page, 
                                selected_id_state, 
                                student_name_display,
                                student_profile_text,
                                student_profile_image,
                                chatbot,
                                session_id_state  # Update session_id
                            ]
                        )

    # Function to update avatar images in chatbot based on selected student
    def update_chatbot_avatars(student_id):
        """Update the avatar images in the chatbot based on the selected student."""
        user_avatar = "avatar/user.png"
        bot_avatar = f"avatar/{student_id}.png"
        return gr.update(avatar_images=(user_avatar, bot_avatar))
        
    # Function to update instructions text with student name
    def update_instructions_text(student_id):
        """Update the instructions text with the selected student's name."""
        student_name = name_dict.get(student_id, "the student")
        return f"You will be able to interact with **{student_name}**, an AI-based digital adolescent. We kindly ask you to please keep the conversation respectful and appropriate. Remember that this is a simulation designed for research and educational purposes."
    
    # Event handlers
    selected_id_state.change(
        update_chatbot_avatars,
        inputs=[selected_id_state],
        outputs=[chatbot]
    )
    
    selected_id_state.change(
        update_instructions_text,
        inputs=[selected_id_state],
        outputs=[instructions_text]
    )
    
    # Scene dropdown change handler
    def handle_scene_change(selected_scene):
        """Handle scene dropdown changes to show/hide custom input."""
        show_custom = selected_scene == "Custom scenario (describe below)"
        return gr.update(visible=show_custom)
    
    scene_dropdown.change(
        handle_scene_change,
        inputs=[scene_dropdown],
        outputs=[custom_scene_input]
    )
    
    # Update scene description when dropdown or custom input changes (with monitoring)
    scene_dropdown.change(
        update_scene_description,
        inputs=[scene_dropdown, custom_scene_input, session_id_state],
        outputs=[scene_description]
    )
    
    custom_scene_input.change(
        update_scene_description,
        inputs=[scene_dropdown, custom_scene_input, session_id_state],
        outputs=[scene_description]
    )
    
    # Chat event handlers (with monitoring)
    back_button.click(
        return_to_selection,
        inputs=[session_id_state],
        outputs=[selection_page, chat_page]
    )
    
    msg.submit(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state, scene_description, session_id_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    send_btn.click(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state, scene_description, session_id_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    clear_btn.click(
        clear_current_chat,
        inputs=[selected_id_state, history_dict_state, session_id_state],
        outputs=[chatbot, history_dict_state],
        queue=False
    )

    # JavaScript for UI enhancements
    demo.load(None, None, None, js="""
    function() {
        // Enhanced header image transparency fix
        function fixHeaderImage() {
            document.querySelectorAll('.header-image, .header-image-container, .header-image > div, .header-image img, .gradio-image, .gradio-image > div, [data-testid="image"], [data-testid="image"] > div').forEach(el => {
                if (el && el.closest('.header-image-container, .header-image')) {
                    el.style.backgroundColor = 'transparent';
                    el.style.border = 'none';
                    el.style.boxShadow = 'none';
                    el.style.padding = '0';
                    el.style.margin = '0';
                }
            });
        }
        
        // Make character cards clickable
        function makeCardsClickable() {
            document.querySelectorAll('.character-card').forEach(card => {
                if (!card.dataset.handlerAttached) {
                    card.dataset.handlerAttached = 'true';
                    card.style.cursor = 'pointer';
                    card.addEventListener('click', function(e) {
                        if (!e.target.classList.contains('chat-btn') && !e.target.closest('.chat-btn')) {
                            const chatBtn = this.querySelector('.chat-btn');
                            if (chatBtn) chatBtn.click();
                        }
                    });
                }
            });
        }
        
        // Style chat avatars
        function styleAvatars() {
            document.querySelectorAll('.gradio-chatbot .avatar img').forEach(img => {
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.borderRadius = '50%';
                img.style.objectFit = 'cover';
                if (img.parentElement) {
                    img.parentElement.style.width = '48px';
                    img.parentElement.style.height = '48px';
                    img.parentElement.style.borderRadius = '50%';
                    img.parentElement.style.overflow = 'hidden';
                    img.parentElement.style.border = '2px solid rgba(9, 64, 103, 0.85)';
                }
            });
        }
        
        // Apply fixes
        setTimeout(() => {
            fixHeaderImage();
            makeCardsClickable();
            styleAvatars();
        }, 500);
        
        // Set up mutation observer
        const observer = new MutationObserver(() => {
            fixHeaderImage();
            makeCardsClickable();
            styleAvatars();
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Periodic fixes
        setInterval(() => {
            fixHeaderImage();
            makeCardsClickable();
            styleAvatars();
        }, 2000);
    }
    """)

    # Initialize session on app load
    demo.load(
        initialize_session,
        inputs=[],
        outputs=[session_id_state]
    )

# Run the application
if __name__ == "__main__":
    # Ensure database is initialized
    print("🔍 Data monitoring system started")
    print("📊 Data will be saved to monitoring.db")
    print("💡 Tip: Run dashboard.py to view monitoring data visualization")
    
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        debug=True,
        favicon_path="avatar/brain_with_title.png",
        show_api=False
    )
