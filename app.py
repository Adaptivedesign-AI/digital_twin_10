import gradio as gr
import json
import os
from openai import OpenAI

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load the shared prompt that will be used as a base for all student interactions
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# Load individual student prompts and combine them with the shared prompt
def load_prompts():
    """
    Load all individual student prompts and combine them with the shared prompt.
    Returns a dictionary with student IDs as keys and complete prompts as values.
    """
    prompts = {}
    for i in range(1, 11):
        path = f"prompts/{i}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                prompts[f"student{i:03d}"] = shared_prompt + "\n\n" + data["prompt"]
    return prompts

# Initialize the prompts dictionary
all_prompts = load_prompts()

# Define student ID to name mapping for display purposes
name_dict = {
    "student001": "Jaden",
    "student002": "Elijah",
    "student003": "Caleb",
    "student004": "Aiden",
    "student005": "Ava",
    "student006": "Brooklyn",
    "student007": "Zoe",
    "student008": "Kayla",
    "student009": "Maya",
    "student010": "Isaiah"
}

# Define student descriptions to provide context about each persona
student_descriptions = {
    "student001": "14 years old. Conflicted but responsible.",
    "student002": "16 years old. Rebellious and reckless.",
    "student003": "12 years old. Extreme and unstable.",
    "student004": "18 years old. Mature and disciplined.",
    "student005": "15 years old. Emotional and introspective.",
    "student006": "16 years old. Moody and inconsistent.",
    "student007": "13 years old. Cheerful and active.",
    "student008": "18 years old. Focused and resilient.",
    "student009": "14 years old. Tense and guarded.",
    "student010": "15 years old. Energetic and driven."
}

# Create a function to initialize empty chat history for all students
def get_empty_history_dict():
    """
    Initialize an empty chat history dictionary for all students.
    This ensures we can track conversations with each student separately.
    """
    return {student_id: [] for student_id in name_dict.keys()}

# Core chat function that handles message processing and AI responses
def chat(message, history, student_id, history_dict):
    """
    Process user messages and generate AI responses.
    
    Args:
        message: The user's input message
        history: Current chat history for the selected student
        student_id: ID of the currently selected student
        history_dict: Dictionary containing all students' chat histories
        
    Returns:
        Empty message input, updated history, and updated history_dict
    """
    # Check for empty messages
    if not message or not message.strip():
        return "", history, history_dict
        
    # Get the appropriate system prompt for the selected student
    system_prompt = all_prompts.get(student_id, "You are a helpful assistant.")

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
        history.append([message, f"⚠️ Error: {str(e)}"])
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

# Function to get student model information (currently returns empty string)
def get_student_model(student_id):
    """
    Get model information for the selected student.
    Currently configured to return an empty string to hide model info.
    """
    return ""  # Return empty string instead of model info

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
    student_name = name_dict.get(student_id, "Unknown")
    student_history = history_dict.get(student_id, [])
    student_model = get_student_model(student_id)
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected student ID
        f"# {student_name}",       # Update student name display
        student_model,             # Update model display (now empty)
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

# Custom CSS with updated styling
custom_css = """
/* Global styles for the entire application */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #f9f9f9;
}

/* Header styling with updated brand color */
.main-title {
    background-color: #094067;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
}

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Responsive breakpoints for character grid at different screen sizes */
@media (max-width: 1200px) {
    .character-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (max-width: 992px) {
    .character-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .character-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .character-grid {
        grid-template-columns: 1fr;
    }
}

/* Card styling - updated with rounded edges */
.character-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #e0e0e0;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
}

.character-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

/* Card header with maximum emphasis for student names */
.card-header {
    background-color: #094067;
    color: white !important;
    padding: 10px;
    text-align: center;
    font-weight: 900 !important; /* Maximum bold weight */
    font-size: 18px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* Student info styling - compact and readable */
.student-name {
    font-size: 16px;
    font-weight: bold;
    margin: 8px 0 4px;
    text-align: center;
}

.student-description {
    padding: 0 12px;
    text-align: center;
    color: #555;
    font-size: 13px;
    min-height: 45px;
    overflow: hidden;
    flex-grow: 1;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

/* Hide model tag for cleaner interface */
.model-tag {
    display: none;
}

/* Avatar styling - updated with circular design */
.character-card .avatar-container {
    width: 120px!important;
    height: 120px!important;
    overflow: hidden!important;
    margin: 15px auto!important;
    border: 2px solid #094067!important;
    border-radius: 50%!important; /* Circular avatars */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1)!important;
}

.character-card .avatar-container img {
    width: 100%!important;
    height: 100%!important;
    object-fit: cover!important;
    display: block!important;
}

/* Chat button styling with updated brand color */
.chat-btn {
    background-color: #3da9fc !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 0 !important;
    margin: 10px auto 16px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 14px !important;
    transition: background-color 0.2s !important;
}

.chat-btn:hover {
    background-color: #2a93e0 !important;
}

/* Chat interface styling for better user experience */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #094067;
    color: white;
    border-radius: 12px 12px 0 0;
}

.back-btn {
    background-color: transparent !important;
    border: 1px solid #fffffe !important;
    color: #fffffe !important;
    border-radius: 5px !important;
    padding: 5px 10px !important;
    margin-right: 15px !important;
    margin-left: 0 !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.back-btn:hover {
    background-color: rgba(255,255,255,0.1) !important;
}

/* Input and buttons styling for better aesthetics */
.message-input textarea {
    background-color: #fffffe !important;
    border: 1px solid #90b4ce !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #094067 !important;
    resize: none !important;
}

/* Button container for vertical layout */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.send-btn {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.send-btn:hover {
    background-color: #2a93e0 !important;
}

.clear-btn {
    background-color: #094067 !important;
    color: #fffffe !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: background-color 0.2s !important;
}

.clear-btn:hover {
    background-color: #073050 !important;
}

/* Character info styling in chat - simplified header without avatar */
.character-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 5px;
}

/* Student name styling in header */
.student-name-header {
    color: #fffffe !important;
    font-size: 24px !important;
    font-weight: bold !important;
    margin: 0 auto !important;
    text-align: center !important;
}

/* Model display styling - hidden by default */
.model-display {
    display: none;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: #d8eefe !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Custom styling for chat rows */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}

/* Chat avatar styling */
.gradio-chatbot .avatar img {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    border: 2px solid #094067 !important;
    object-fit: cover !important;
}

/* Ensure avatars are visible and styled correctly */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 8px !important;
    flex-shrink: 0 !important;
    box-shadow: none !important;
    border: 2px solid #094067 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Chat bubbles: AI is blue, user is white */
.gradio-chatbot .message.bot {
    background-color: #3da9fc !important;
    color: #fffffe !important;
    border-bottom-left-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-right-radius: 18px !important;
    margin-left: 12px !important;
    margin-right: auto !important;
    max-width: 80%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

.gradio-chatbot .message.user {
    background-color: #fffffe !important;
    color: #094067 !important;
    border-bottom-right-radius: 6px !important;
    border-top-left-radius: 18px !important;
    border-top-right-radius: 18px !important;
    border-bottom-left-radius: 18px !important;
    margin-right: 12px !important;
    margin-left: auto !important;
    max-width: 80%;
    border: 1px solid #90b4ce !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    padding: 12px 16px !important;
    word-wrap: break-word !important;
}

/* Chat area overall background (light blue) */
.character-ai-style.chatbox-container {
    background-color: #d8eefe !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* Emotion tag styling for emotional context */
.emotion-tag {
    font-style: italic !important;
    font-size: 12px !important;
    color: #666 !important;
    margin-top: 4px !important;
    display: block !important;
}

/* Project description styling */
.project-description {
    text-align: center;
    margin: 0 auto 20px;
    max-width: 800px;
    color: #555;
    font-size: 14px;
    line-height: 1.5;
    padding: 0 20px;
    font-style: italic;
}

/* Chat avatar containers */
.gradio-chatbot .avatar-container {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    border: 2px solid #094067 !important;
    margin: 0 !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Ensure proper message wrapping and alignment */
.gradio-chatbot .message-wrap {
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: flex-start !important;
}

/* Selection heading styling for clear hierarchy */
.selection-heading {
    text-align: center;
    margin: 20px 0 10px;
    color: #094067;
    font-size: 22px;
    font-weight: bold;
}

/* Container for main content with reasonable max width */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Fix Gradio spacing issues */
.gradio-container {
    max-width: 100% !important;
}

/* Hide unnecessary margins in Gradio blocks */
.block {
    margin-bottom: 0 !important;
}

/* Center the name and model in the chat header */
.center-header {
    margin: 0 auto;
    text-align: center;
}

/* Input row: transparent background, vertically centered */
.gradio-container .row {
    background-color: transparent !important;
    align-items: center !important;
}
"""

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(css=custom_css) as demo:

    # Initialize state to track history and selected student
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    
    # Create both pages as components for switching between them
    selection_page = gr.Group(visible=True)
    chat_page = gr.Group(visible=False)
    
    # Define chat page components first
    with chat_page:
        # Chat header with student info - centered design without avatar
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
            # Student information - centered, no avatar for cleaner look
            with gr.Column(elem_classes="center-header"):
                name_display = gr.Markdown("Student Name")
                model_display = gr.Markdown("", elem_classes="model-tag")  # Empty model display
            
        # Chat area with avatars for user/bot distinction
        chatbot = gr.Chatbot(
            label="Conversation",
            avatar_images=("avatar/user.png", None),  # Will be updated dynamically
            height=450,
            elem_classes="character-ai-style chatbox-container",
            show_label=True,
            show_copy_button=True,
            bubble_full_width=False,
        )
        
        # Input area with improved layout - split into message and buttons
        with gr.Row():
            # Left column for text input
            with gr.Column(scale=5):
                msg = gr.Textbox(
                    placeholder="Type your message...",
                    label="",
                    elem_classes="message-input",
                )
            
            # Right column for buttons (stacked vertically)
            with gr.Column(scale=1, elem_classes="button-container"):
                send_btn = gr.Button("Send", elem_classes="send-btn")
                clear_btn = gr.Button("Clear", elem_classes="clear-btn")
    
    # Define selection page with responsive 5-column grid like Character.ai
    with selection_page:
        with gr.Column(elem_classes="container"):
            # Replace text title with image
            gr.Image(
                value="avatar/brain_with_title.png",
                show_label=False,
                elem_classes="header-image",
                height=120
            )
            
            gr.Markdown("### Choose a digital adolescent to chat with", elem_classes="selection-heading")
            gr.Markdown("*These digital adolescents are AI-powered digital twins of real-world teens sampled from the Youth Risk Behavior Surveillance System, enabling data-driven simulations of risk trajectories and intervention outcomes.*", elem_classes="project-description")
            
            # Create a responsive grid for all students - 5 columns that adapt to screen size
            with gr.Column(elem_classes="character-grid"):
                # Loop through all 10 students to create a 5-column grid
                for i in range(0, 10):
                    student_id = f"student{i+1:03d}"
                    student_name = name_dict[student_id]
                    
                    with gr.Column(elem_classes="character-card"):
                        # Replace "Digital Twin" with student's name in white bold font
                        gr.Markdown(f"**{student_name}**", elem_classes="card-header")
                        
                        # Avatar container - circular design
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
                            )
                            
                        gr.Markdown(f"### {student_name}", elem_classes="student-name", visible=False)  # Hidden as now shown in header
                        gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                        # Empty model tag (hidden)
                        gr.Markdown("", elem_classes="model-tag")
                        
                        # Chat button with click handler
                        btn = gr.Button("Start Chat", elem_classes="chat-btn")
                        btn.click(
                            select_student_direct,
                            inputs=[
                                gr.Textbox(value=student_id, visible=False),
                                history_dict_state
                            ],
                            outputs=[
                                selection_page, 
                                chat_page, 
                                selected_id_state, 
                                name_display, 
                                model_display,
                                chatbot
                            ]
                        )

    # Function to update avatar images in chatbot based on selected student
    def update_chatbot_avatars(student_id):
        """
        Update the avatar images in the chatbot based on the selected student.
        
        Args:
            student_id: ID of the selected student
            
        Returns:
            Updated chatbot with appropriate avatars
        """
        user_avatar = "avatar/user.png"
        bot_avatar = f"avatar/{student_id}.png"
        return gr.update(avatar_images=(user_avatar, bot_avatar))
        
    # Event to update avatars when student is selected
    selected_id_state.change(
        update_chatbot_avatars,
        inputs=[selected_id_state],
        outputs=[chatbot]
    )
    
    # Set up event handlers for UI interactions
    
    # Return to selection page when back button is clicked
    back_button.click(
        return_to_selection,
        inputs=[],
        outputs=[selection_page, chat_page]
    )
    
    # Handle message submission in the chat interface
    msg.submit(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    # Handle send button click in the chat interface
    send_btn.click(
        chat,
        inputs=[msg, chatbot, selected_id_state, history_dict_state],
        outputs=[msg, chatbot, history_dict_state],
    )
    
    # Handle clear button click to reset conversation
    clear_btn.click(
        clear_current_chat,
        inputs=[selected_id_state, history_dict_state],
        outputs=[chatbot, history_dict_state],
        queue=False
    )

    # JavaScript to ensure avatars display correctly across browsers and Gradio versions
    demo.load(None, None, None, js="""
    function() {
        // Define the style fix function to ensure consistent avatar rendering
        function fixChatStyles() {
            // Style chat avatars
            document.querySelectorAll('.gradio-chatbot .avatar img, .gradio-chatbot img.avatar-image').forEach(img => {
                img.style.width = '48px';
                img.style.height = '48px';
                img.style.borderRadius = '50%';
                img.style.border = 'none';
                img.style.objectFit = 'cover';
                img.style.padding = '0';
                img.style.margin = '0';
                
                // Style parent container
                if (img.parentElement) {
                    img.parentElement.style.width = '48px';
                    img.parentElement.style.height = '48px';
                    img.parentElement.style.border = '2px solid #094067';
                    img.parentElement.style.borderRadius = '50%';
                    img.parentElement.style.overflow = 'hidden';
                    img.parentElement.style.padding = '0';
                    img.parentElement.style.margin = '0';
                    img.parentElement.style.backgroundColor = 'transparent';
                    img.parentElement.style.boxShadow = 'none';
                }
            });
            
            // Apply maximum emphasis to student names in card headers
            document.querySelectorAll('.card-header').forEach(header => {
                // Maximum styling for card headers
                header.style.backgroundColor = '#094067';
                header.style.color = '#FFFFFF';
                header.style.fontWeight = '900'; // Maximum bold weight
                header.style.fontSize = '18px';
                header.style.textTransform = 'uppercase';
                header.style.letterSpacing = '0.5px';
                header.style.textShadow = '0 1px 2px rgba(0,0,0,0.2)';
                header.style.padding = '10px';
                
                // Add extra emphasis with HTML
                if (!header.innerHTML.includes('<strong>')) {
                    // Only modify if not already emphasized
                    let text = header.textContent.trim();
                    header.innerHTML = `<strong style="font-weight:900;">${text}</strong>`;
                }
            });
            
            // Fix avatar containers in messages
            document.querySelectorAll('.gradio-chatbot .avatar-container, .gradio-chatbot [class*="message"] > div:first-child').forEach(container => {
                if (!container.closest('.character-card')) {
                    container.style.width = '48px';
                    container.style.height = '48px'; 
                    container.style.borderRadius = '50%';
                    container.style.overflow = 'hidden';
                    container.style.border = '2px solid #094067';
                    container.style.padding = '0';
                    container.style.margin = '0';
                    container.style.boxShadow = 'none';
                    container.style.backgroundColor = 'transparent';
                    container.style.minWidth = '48px';
                    container.style.minHeight = '48px';
                    container.style.flexShrink = '0';
                }
            });
            
            // Style bot messages (blue)
            document.querySelectorAll('.gradio-chatbot .message.bot').forEach(msg => {
                msg.style.backgroundColor = '#3da9fc';
                msg.style.color = '#fffffe';
                msg.style.borderBottomLeftRadius = '6px';
                msg.style.borderTopLeftRadius = '18px';
                msg.style.borderTopRightRadius = '18px';
                msg.style.borderBottomRightRadius = '18px';
                msg.style.marginLeft = '12px';
                msg.style.marginRight = 'auto';
                msg.style.maxWidth = '80%';
                msg.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                msg.style.padding = '12px 16px';
                msg.style.wordWrap = 'break-word';
            });
            
            // Style user messages (white)
            document.querySelectorAll('.gradio-chatbot .message.user').forEach(msg => {
                msg.style.backgroundColor = '#fffffe';
                msg.style.color = '#094067';
                msg.style.borderBottomRightRadius = '6px';
                msg.style.borderTopLeftRadius = '18px';
                msg.style.borderTopRightRadius = '18px';
                msg.style.borderBottomLeftRadius = '18px';
                msg.style.marginRight = '12px';
                msg.style.marginLeft = 'auto';
                msg.style.maxWidth = '80%';
                msg.style.border = '1px solid #90b4ce';
                msg.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
                msg.style.padding = '12px 16px';
                msg.style.wordWrap = 'break-word';
            });
