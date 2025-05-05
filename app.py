import gradio as gr
import json
import os
from openai import OpenAI

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load the shared prompt that will be used as a base for all adolescent interactions
with open("shared_prompt.txt", "r") as f:
    shared_prompt = f.read().strip()

# Load individual adolescent prompts and combine them with the shared prompt
def load_prompts():
    """
    Load all individual adolescent prompts and combine them with the shared prompt.
    Returns a dictionary with adolescent IDs as keys and complete prompts as values.
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

# Define adolescent ID to name mapping for display purposes
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

# Define adolescent descriptions to provide context about each persona
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

# Create a function to initialize empty chat history for all adolescents
def get_empty_history_dict():
    """
    Initialize an empty chat history dictionary for all adolescents.
    This ensures we can track conversations with each adolescent separately.
    """
    return {student_id: [] for student_id in name_dict.keys()}

# Core chat function that handles message processing and AI responses
def chat(message, history, student_id, history_dict):
    """
    Process user messages and generate AI responses.
    
    Args:
        message: The user's input message
        history: Current chat history for the selected adolescent
        student_id: ID of the currently selected adolescent
        history_dict: Dictionary containing all adolescents' chat histories
        
    Returns:
        Empty message input, updated history, and updated history_dict
    """
    # Check for empty messages
    if not message or not message.strip():
        return "", history, history_dict
        
    # Get the appropriate system prompt for the selected adolescent
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

# Function to clear chat history for the current adolescent
def clear_current_chat(student_id, history_dict):
    """
    Clear the chat history for the currently selected adolescent.
    
    Args:
        student_id: ID of the currently selected adolescent
        history_dict: Dictionary containing all adolescents' chat histories
        
    Returns:
        Empty history list and updated history_dict
    """
    history_dict[student_id] = []
    return [], history_dict

# Function to get adolescent model information (currently returns empty string)
def get_student_model(student_id):
    """
    Get model information for the selected adolescent.
    Currently configured to return an empty string to hide model info.
    """
    return ""  # Return empty string instead of model info

# Function to handle direct adolescent selection and switch to chat interface
def select_student_direct(student_id, history_dict):
    """
    Handle direct adolescent selection and switch to chat interface.
    
    Args:
        student_id: ID of the selected adolescent
        history_dict: Dictionary containing all adolescents' chat histories
        
    Returns:
        UI updates to show chat interface with selected adolescent info
    """
    student_name = name_dict.get(student_id, "Unknown")
    student_history = history_dict.get(student_id, [])
    student_model = get_student_model(student_id)
    
    return (
        gr.update(visible=False),  # Hide selection page
        gr.update(visible=True),   # Show chat page
        student_id,                # Update selected adolescent ID
        f"# {student_name}",       # Update adolescent name display
        student_model,             # Update model display (now empty)
        student_history            # Update chat history
    )

# Function to return to the adolescent selection page
def return_to_selection():
    """
    Return to the adolescent selection page from the chat interface.
    
    Returns:
        UI updates to show selection page and hide chat page
    """
    return (
        gr.update(visible=True),   # Show selection page
        gr.update(visible=False)   # Hide chat page
    )

custom_css = """
/* Global styles with light blue background */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    background-color: #d8eefe; /* Light blue background */
}

/* Container for main content with light blue background */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    background-color: #d8eefe;
}

/* Header container styling */
.header-container {
    display: flex;
    align-items: center;
    width: 100%;
    background-color: #d8eefe; /* Navy blue from the palette */
    border-radius: 8px 8px 0 0;
    padding: 0;
    margin: 0;
}

/* Logo container in top-left corner */
.logo-container {
    width: 40px !important;
    flex: 0 0 40px !important;
    padding: 10px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Title container for the centered text */
.title-container {
    flex-grow: 1 !important;
    text-align: center !important;
    padding: 10px 0 !important;
}

/* Title text styling */
.title-text h1 {
    color: #fffffe !important; /* White text */
    margin: 0 !important;
    padding: 0 !important;
    text-align: center !important;
    font-size: 24px !important;
    font-weight: bold !important;
}

/* Selection heading styling */
.selection-heading {
    text-align: center;
    margin: 20px 0 10px;
    color: #d8eefe; /* Navy blue */
    font-size: 20px;
}

/* Description text styling */
.description-text {
    text-align: center;
    margin: 10px auto 20px;
    max-width: 800px;
    color: #5f6c7b; /* Paragraph color from palette */
    font-size: 14px;
    line-height: 1.5;
}

/* Character.ai style grid for selection page - 5 columns by default */
.character-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 15px;
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

/* Card styling with navy theme */
.character-card {
    background: #d8eefe; /* Navy blue */
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    border: 1px solid #5f6c7b; /* Border color from palette */
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    max-width: 220px;
    margin: 0 auto;
    color: #fffffe; /* White text */
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.15);
}

.card-header {
    background-color: #5f6c7b; /* Paragraph color from palette */
    color: #fffffe; /* White text */
    padding: 10px;
    text-align: center;
    font-weight: bold;
    font-size: 15px;
}

/* Adolescent info styling - improved for readability */
.student-name {
    font-size: 18px;
    font-weight: bold;
    margin: 10px 0 5px;
    text-align: center;
    color: #fffffe; /* White text */
}

.student-description {
    padding: 0 10px;
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 13px;
    min-height: 45px;
    overflow: hidden;
    flex-grow: 1;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

/* Hide model tag for cleaner interface */
.model-tag {
    display: none;
}

/* Avatar styling in selection cards - circular styling */
.avatar-container {
    width: 100px !important;
    height: 100px !important;
    overflow: hidden !important;
    margin: 15px auto !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 50% !important;
    background-color: #f0f0f0 !important;
}

.avatar-container img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    display: block !important;
}

/* Chat button styling with blue */
.chat-btn {
    background-color: #3da9fc !important; /* Button color from palette */
    color: #fffffe !important; /* White text */
    border: none !important;
    border-radius: 20px !important;
    padding: 6px 0 !important;
    margin: 6px auto 10px !important;
    width: 85% !important;
    display: block !important;
    font-weight: bold !important;
    cursor: pointer !important;
    font-size: 13px !important;
}

.chat-btn:hover {
    background-color: #90b4ce !important; /* Secondary color from palette */
}

/* Chat header */
.chat-header {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #90b4ce;
    background-color: #d8eefe; /* Navy blue */
    color: #fffffe; /* White text */
    border-radius: 8px 8px 0 0;
}

.back-btn {
    background-color: #5f6c7b !important; /* Paragraph color */
    border: none !important;
    color: #fffffe !important; /* White text */
    border-radius: 5px !important;
    margin-right: 15px !important;
    margin-left: 0 !important;
}

/* Input and buttons styling for better aesthetics */
.message-input {
    border-radius: 20px !important;
    padding: 10px 15px !important;
    border: 1px solid #90b4ce !important; /* Secondary color */
    background-color: #fffffe !important; /* White background */
}

/* Button container for vertical layout */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

/* Send button styling */
.send-btn {
    background-color: #3da9fc !important; /* Button color */
    color: #fffffe !important; /* White text */
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
}

/* Clear button styling */
.clear-btn {
    background-color: #5f6c7b !important; /* Paragraph color */
    color: #fffffe !important; /* White text */
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    width: 100% !important;
}

/* Character info styling in chat - simplified header without avatar */
.character-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 5px;
}

/* Adolescent name styling in header */
.student-name-header {
    font-size: 22px;
    font-weight: bold;
    margin: 0;
    color: #fffffe; /* White text */
}

/* Model display styling - hidden by default */
.model-display {
    display: none;
}

/* Character.ai style chat container */
.character-ai-style {
    border-radius: 12px;
    background-color: #fffffe; /* White */
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Custom styling for chat rows */
.chatbot-row {
    display: flex;
    margin-bottom: 20px;
}

/* Small avatars for chat bubbles - 8px size */
.gradio-chatbot .avatar {
    display: block !important;
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    margin-right: 4px !important;
    margin-top: 2px !important;
    flex-shrink: 0 !important;
    border: none !important;
    background-color: transparent !important;
}

/* Ensure avatars are visible and styled correctly */
.gradio-chatbot .message-wrap.user .avatar,
.gradio-chatbot .message-wrap.bot .avatar {
    display: inline-block !important;
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    overflow: hidden !important;
    margin-right: 4px !important;
    flex-shrink: 0 !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0 !important;
    background-color: transparent !important;
}

/* Character.ai style chat bubbles */
.gradio-chatbot .message {
    border-radius: 18px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    line-height: 1.5 !important;
    max-width: 80% !important;
    display: inline-block !important;
    margin-top: 5px !important;
    word-wrap: break-word !important;
}

/* User message styling with brand color */
.gradio-chatbot .message.user {
    background-color: #3da9fc !important; /* Button color */
    color: #fffffe !important; /* White text */
    border-bottom-right-radius: 4px !important;
    margin-left: auto !important;
}

/* Bot message styling with light background */
.gradio-chatbot .message.bot {
    background-color: #fffffe !important; /* White background */
    color: #d8eefe !important; /* Navy text */
    border-bottom-left-radius: 4px !important;
    margin-right: auto !important;
    border: 1px solid #90b4ce !important; /* Secondary color border */
}

/* Emotion tag styling for emotional context */
.emotion-tag {
    font-style: italic;
    display: block;
    margin-top: 5px;
    color: #5f6c7b; /* Paragraph color */
    font-size: 0.9em;
}

/* Custom styling for chat container */
.chatbox-container {
    padding: 20px !important;
    background-color: #d8eefe !important; /* Light blue background */
    border-radius: 12px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}

/* Override default gradio chatbot styling for avatars */
.gradio-container .prose img.avatar-image {
    display: inline-block !important;
    margin: 0 !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
}

/* Remove avatar boxes but keep larger avatar size */
.avatar-container {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.message-row .avatar-image, 
.message-wrap .avatar-image {
    width: 48px !important;
    height: 48px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
    display: block !important;
}

/* Target specific avatar container in messages */
.message-row > .svelte-1y9ctm5,
.message-wrap > .svelte-1y9ctm5 {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Target avatar in message bubbles */
.message-bubble .avatar-container,
.message .avatar-container {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

/* Disable rectangular borders around avatar images */
img.avatar-image {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
    padding: 0 !important;
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

/* Add more whitespace around messages for readability */
.gradio-chatbot .message-wrap {
    margin-bottom: 10px !important;
}

/* Adjust spacing for better alignment with tiny avatars */
.gradio-chatbot .message-wrap > div {
    display: flex !important;
    align-items: flex-start !important;
}

/* Remove any old classes that might conflict */
.main-title {
    display: none !important;
}
"""

# --------------------------------------------
# = UI BUILDING =
# --------------------------------------------
with gr.Blocks(css=custom_css) as demo:

    # Initialize state to track history and selected adolescent
    history_dict_state = gr.State(get_empty_history_dict())
    selected_id_state = gr.State("")
    
    # Create both pages as components for switching between them
    selection_page = gr.Group(visible=True)
    chat_page = gr.Group(visible=False)
    
    # Define chat page components first
    with chat_page:
        # Chat header with adolescent info - centered design without avatar
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
            # Adolescent information - centered, no avatar for cleaner look
            with gr.Column(elem_classes="center-header"):
                name_display = gr.Markdown("Digital Adolescent Name")
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
            # Updated title with brain icon and no hyphen
            with gr.Row(elem_classes="header-container"):
                with gr.Column(elem_classes="logo-container", scale=1):
                    gr.Image(value="avatar/brain.png", show_label=False, height=40, width=40)
                with gr.Column(elem_classes="title-container", scale=10):
                    gr.Markdown("# Generative Digital Adolescent Cohort", elem_classes="main-title")
            
            # Updated subtitle with new text and description
            gr.Markdown("### Choose a digital adolescent to chat with", elem_classes="selection-heading")
            gr.Markdown("*These digital adolescents are AI-powered digital twins of real-world teens sampled from the Youth Risk Behavior Surveillance System, enabling data-driven simulations of risk trajectories and intervention outcomes.*", elem_classes="description-text")
            
            # Create a responsive grid for all adolescents - 5 columns that adapt to screen size
            with gr.Column(elem_classes="character-grid"):
                # Loop through all 10 adolescents to create a 5-column grid
                for i in range(0, 10):
                    student_id = f"student{i+1:03d}"
                    student_name = name_dict[student_id]
                    
                    with gr.Column(elem_classes="character-card"):
                        # Changed from "Digital Twin" to actual name
                        gr.Markdown(f"{student_name}", elem_classes="card-header")
                        
                        # Avatar container - circular with student image
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
                            )
                            
                        # No need for name here as it's already in the header
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

    # Function to update avatar images in chatbot based on selected adolescent
    def update_chatbot_avatars(student_id):
        """
        Update the avatar images in the chatbot based on the selected adolescent.
        
        Args:
            student_id: ID of the selected adolescent
            
        Returns:
            Updated chatbot with appropriate avatars
        """
        user_avatar = "avatar/user.png"
        bot_avatar = f"avatar/{student_id}.png"
        return gr.update(avatar_images=(user_avatar, bot_avatar))
        
    # Event to update avatars when adolescent is selected
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
        function fixAvatarStyles() {
            // Find all avatar images and containers
            const avatarImages = document.querySelectorAll('img.avatar-image');
            const avatarContainers = document.querySelectorAll('.avatar-container, [class*="message"] .svelte-1y9ctm5');
            
            // Fix avatar images - remove borders and set consistent size
            avatarImages.forEach(img => {
                img.style.border = 'none';
                img.style.boxShadow = 'none';
                img.style.padding = '0';
                img.style.margin = '0';
                img.style.width = '48px';
                img.style.height = '48px';
                img.style.display = 'block';
                img.style.borderRadius = '50%';
                
                // Set parent elements as well for consistency
                if (img.parentElement) {
                    img.parentElement.style.border = 'none';
                    img.parentElement.style.boxShadow = 'none';
                    img.parentElement.style.padding = '0';
                    img.parentElement.style.margin = '0';
                    img.parentElement.style.backgroundColor = 'transparent';
                }
            });
            
            // Fix avatar containers - remove borders and backgrounds
            avatarContainers.forEach(container => {
                container.style.border = 'none';
                container.style.boxShadow = 'none';
                container.style.backgroundColor = 'transparent';
                container.style.padding = '0';
                container.style.margin = '0';
            });
            
            // Find message elements and fix avatar containers within them
            document.querySelectorAll('[class*="message"]').forEach(el => {
                // Find possible avatar containers within messages
                const possibleContainers = el.querySelectorAll('div:first-child');
                possibleContainers.forEach(container => {
                    if (container.querySelector('img')) {
                        container.style.border = 'none';
                        container.style.boxShadow = 'none';
                        container.style.backgroundColor = 'transparent';
                        container.style.padding = '0';
                        container.style.margin = '0';
                    }
                });
            });
            
            // Ensure selection page avatars remain properly sized and visible
            document.querySelectorAll('.avatar-container img').forEach(function(img) {
                if (img.closest('.character-card')) {
                    img.style.display = 'block';
                    img.style.width = '100%';
                    img.style.height = '100%';
                    img.style.objectFit = 'cover';
                }
            });
            
            // Format message bubbles with consistent styling
            document.querySelectorAll('.gradio-chatbot .message').forEach(function(msg) {
                msg.style.borderRadius = '18px';
                msg.style.padding = '12px 16px';
                msg.style.maxWidth = '80%';
                
                // Apply different styles for user vs bot messages
                if (msg.classList.contains('user')) {
                    msg.style.backgroundColor = '#4299e1';
                    msg.style.color = 'white';
                    msg.style.borderBottomRightRadius = '4px';
                } else {
                    msg.style.backgroundColor = '#f1f1f1';
                    msg.style.color = '#333';
                    msg.style.borderBottomLeftRadius = '4px';
                }
            });
            
            // Make entire character cards clickable for better UX
            document.querySelectorAll('.character-card').forEach(function(card) {
                card.style.cursor = 'pointer';
                card.addEventListener('click', function(e) {
                    // Find and click the button within this card
                    const button = this.querySelector('.chat-btn');
                    if (button && e.target !== button) {
                        button.click();
                    }
                });
            });
            
            // Hide any model tags that might appear
            document.querySelectorAll('.model-tag').forEach(function(tag) {
                tag.style.display = 'none';
            });
            
            // Fix message bubble alignment for consistent layout
            document.querySelectorAll('.gradio-chatbot .message-wrap').forEach(wrap => {
                // Ensure consistent alignment for all messages
                wrap.style.display = "flex";
                wrap.style.alignItems = "flex-start";
                wrap.style.gap = "8px"; // Controls spacing between avatar and message
            });
            
            // Set specific margins for bot and user messages
            document.querySelectorAll('.gradio-chatbot .message-wrap.bot').forEach(msg => {
                msg.style.marginLeft = "12px"; // Reduced from 58px for more compact layout
            });
            document.querySelectorAll('.gradio-chatbot .message-wrap.user').forEach(msg => {
                msg.style.marginRight = "12px"; // Reduced from 58px for more compact layout
            });
        }
        
        // Call the fix function initially to apply styles
        fixAvatarStyles();
        
        // Set up a mutation observer to watch for DOM changes and reapply styles
        const observer = new MutationObserver(function(mutations) {
            fixAvatarStyles();
        });
        
        // Start observing the entire document for changes to catch all UI updates
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Also periodically call the fix function for reliability
        setInterval(fixAvatarStyles, 1000);
    }
    """)

# Run the application when script is executed directly
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
