import gradio as gr
import json
import os
from openai import OpenAI
from custom_css import custom_css  # Import the custom CSS from separate file

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))

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

# Define detailed student profiles for the new interface
student_profiles = {
    "student001": {
        "age": 14,
        "sex": "Male",
        "race_ethnicity": "African American",
        "hobbies": "Basketball, hip-hop music, video games",
        "emotional_health": "Struggles with anger management and trust issues",
        "mental_health": "Mild anxiety in social situations, difficulty expressing emotions"
    },
    "student002": {
        "age": 16,
        "sex": "Male",
        "race_ethnicity": "Caucasian",
        "hobbies": "Skateboarding, alternative music, graphic design",
        "emotional_health": "Emotionally detached, impulsive decision-making",
        "mental_health": "Reports feeling disconnected from peers, occasional mood swings"
    },
    "student003": {
        "age": 14,
        "sex": "Female",
        "race_ethnicity": "Caucasian",
        "hobbies": "Reading, creative writing, painting",
        "emotional_health": "Highly sensitive, self-critical, perfectionist tendencies",
        "mental_health": "Mild depression symptoms, low self-esteem, overthinking"
    },
    "student004": {
        "age": 13,
        "sex": "Male",
        "race_ethnicity": "Latino/Hispanic",
        "hobbies": "Soccer, family gatherings, cooking",
        "emotional_health": "Emotionally guarded, tough exterior to protect vulnerability",
        "mental_health": "Family-related stress, pressure to succeed academically"
    },
    "student005": {
        "age": 15,
        "sex": "Female",
        "race_ethnicity": "African American",
        "hobbies": "Poetry, social justice activism, yoga",
        "emotional_health": "Highly introspective, emotionally aware and articulate",
        "mental_health": "Anxiety about social issues, occasional overwhelm from empathy"
    },
    "student006": {
        "age": 17,
        "sex": "Male",
        "race_ethnicity": "Asian American",
        "hobbies": "Academic competitions, chess, classical music",
        "emotional_health": "Disciplined but emotionally withdrawn, difficulty connecting",
        "mental_health": "High-functioning anxiety, perfectionist stress, social isolation"
    },
    "student007": {
        "age": 16,
        "sex": "Female",
        "race_ethnicity": "Caucasian",
        "hobbies": "Student government, debate team, volunteering",
        "emotional_health": "Goal-oriented, emotionally steady, natural leader",
        "mental_health": "Generally stable, occasional stress from high expectations"
    },
    "student008": {
        "age": 15,
        "sex": "Female",
        "race_ethnicity": "Mixed race (African American/Caucasian)",
        "hobbies": "Dance, photography, social media",
        "emotional_health": "Friendly but cautious, struggles with identity",
        "mental_health": "Body image concerns, social comparison anxiety"
    },
    "student009": {
        "age": 17,
        "sex": "Female",
        "race_ethnicity": "Pacific Islander",
        "hobbies": "Marine biology, surfing, environmental activism",
        "emotional_health": "Thoughtful, quietly confident, calm demeanor",
        "mental_health": "Generally well-adjusted, environmental anxiety"
    },
    "student010": {
        "age": 16,
        "sex": "Male",
        "race_ethnicity": "Native American",
        "hobbies": "Traditional crafts, hiking, storytelling",
        "emotional_health": "Restless, emotionally conflicted, seeking identity",
        "mental_health": "Cultural identity struggles, feelings of not belonging"
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

# Core chat function that handles message processing and AI responses
def chat(message, history, student_id, history_dict, scene_description):
    """
    Process user messages and generate AI responses.
    
    Args:
        message: The user's input message
        history: Current chat history for the selected student
        student_id: ID of the currently selected student
        history_dict: Dictionary containing all students' chat histories
        scene_description: Current scene context for the conversation
        
    Returns:
        Empty message input, updated history, and updated history_dict
    """
    # Check for empty messages
    if not message or not message.strip():
        return "", history, history_dict
        
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
        
        # Update conversation history
        history.append([message, reply])
        history_dict[student_id] = history
        return "", history, history_dict
    except Exception as e:
        # Handle API errors gracefully
        error_message = f"⚠️ Error: {str(e)}"
        history.append([message, error_message])
        history_dict[student_id] = history
        return "", history, history_dict

# Function to clear chat history for the current student
def clear_current_chat(student_id, history_dict):
    """
    Clear the chat history for the currently selected student.
    
    Args:
        student_id: ID of the currently selected student
        history_dict: Dictionary containing all students' chat histories
        
    Returns:
        Empty history list and updated history_dict
    """
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
**Hobbies:** {profile['hobbies']}  
**Emotional Health:** {profile['emotional_health']}  
**Mental Health:** {profile['mental_health']}
    """.strip()
    
    # Update student name and profile
    return f"# {student_name}", profile_text, f"avatar/{student_id}.png"

# Function to handle direct student selection and switch to chat interface
def select_student_direct(student_id, history_dict):
    """
    Handle direct student selection and switch to chat interface.
    
    Args:
        student_id: ID of the selected student
        history_dict: Dictionary containing all students' chat histories
        
    Returns:
        UI updates to show chat interface with selected student info
    """
    student_history = history_dict.get(student_id, [])
    student_name, profile_text, profile_image = update_student_profile(student_id)
    
    # Debug print for server logs
    print(f"Selecting student: {student_id}, Name: {student_name}")
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected student ID
        student_name,              # Update student name display
        profile_text,              # Update profile text
        profile_image,             # Update profile image
        student_history            # Update chat history
    )

# Function to return to the student selection page
def return_to_selection():
    """
    Return to the student selection page from the chat interface.
    
    Returns:
        UI updates to show selection page and hide chat page
    """
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

# Function to update scene description based on dropdown selection
def update_scene_description(selected_scene, custom_description):
    """
    Update scene description based on dropdown selection.
    
    Args:
        selected_scene: Selected scene from dropdown
        custom_description: Custom description if "Custom scenario" is selected
        
    Returns:
        Updated scene description
    """
    if selected_scene == "Custom scenario (describe below)":
        return custom_description
    elif selected_scene == "Posted a video on TikTok and received hateful comments":
        return "Posted a short video on TikTok. Anonymous users flooded the comments with anti-Asian slurs and told her to 'go back where you came from.' The twin deleted the post and now feels afraid to post anything."
    else:
        return selected_scene

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(css=custom_css, title="Digital Twins") as demo:

    # Initialize state to track history and selected student
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    
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
            # Left column: Chat interface
            with gr.Column(scale=6, elem_classes="chat-column"):
                # Chat area with avatars for user/bot distinction
                chatbot = gr.Chatbot(
                    label="Conversation",
                    avatar_images=("avatar/user.png", None),
                    height=600,  
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
            
            # Right column: Student info and scene controls
            with gr.Column(scale=4, elem_classes="info-column"):
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
                        # Remove the header markdown that was creating the blue bar
                        
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
                            )
                            
                        gr.Markdown(f"### {student_name}", elem_classes="student-name")
                        gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                        
                        chat_btn = gr.Button("Start Chat", elem_classes="chat-btn", elem_id=f"chat-btn-{student_id}")
                        chat_btn.click(
                            select_student_direct,
                            inputs=[
                                gr.Textbox(value=student_id, visible=False),
                                history_dict_state
                            ],
                            outputs=[
                                selection_page, 
                                chat_page, 
                                selected_id_state, 
                                student_name_display,
                                student_profile_text,
                                student_profile_image,
                                chatbot
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
    
    # Update scene description when dropdown or custom input changes
    scene_dropdown.change(
        update_scene_description,
        inputs=[scene_dropdown, custom_scene_input],
        outputs=[scene_description]
    )
    
    custom_scene_input.change(
        update_scene_description,
        inputs=[scene_dropdown, custom_scene_input],
        outputs=[scene_description]
    )
    
    # Chat event handlers
    back_button.click(
        return_to_selection,
        inputs=[],
        outputs=[selection_page, chat_page]
    )
    
    msg.submit(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state, scene_description],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    send_btn.click(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state, scene_description],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    clear_btn.click(
        clear_current_chat,
        inputs=[selected_id_state, history_dict_state],
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
                    img.parentElement.style.border = '2px solid rgba(46, 40, 92, 0.85)';
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

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        debug=True,
        favicon_path="avatar/brain_with_title.png",
        show_api=False
    )
