import gradio as gr
import json
import os
from openai import OpenAI
from custom_css import custom_css

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
            with gr.Row(elem_classes="header-container"):
                with gr.Column(elem_classes="logo-title-container"):
                    gr.Image(
                        value="avatar/brain_with_title.png",
                        show_label=False,
                        interactive=False,
                        elem_classes="title-image no-interaction"  
                    )   
            
            # Updated subtitle with new text and description
            gr.Markdown(
                "### Choose a digital adolescent to chat with", 
                elem_classes="selection-heading"
            )
            gr.Markdown(
                "*These digital adolescents are AI-powered digital twins of real-world teens sampled from the Youth Risk Behavior Surveillance System, enabling data-driven simulations of risk trajectories and intervention outcomes.*", 
                elem_classes="description-text"
            )
            
            # Create a responsive grid for all adolescents - 5 columns that adapt to screen size
            with gr.Column(elem_classes="character-grid"):
                # Loop through all 10 adolescents to create a 5-column grid
                for i in range(10):
                    student_id = f"student{i+1:03d}"
                    student_name = name_dict[student_id]
                    
                    with gr.Column(elem_classes="character-card"):
                        # Name header
                        gr.Markdown(f"{student_name}", elem_classes="card-header")
                        
                        # Avatar container
                        with gr.Column(elem_classes="avatar-container"):
                            gr.Image(
                                value=f"avatar/{student_id}.png",
                                show_label=False,
                                elem_classes="avatar-img"
                            )
                        
                        # Description
                        gr.Markdown(student_descriptions[student_id], elem_classes="student-description")
                        
                        # Empty model tag
                        gr.Markdown("", elem_classes="model-tag")
                        
                        # Define hidden student ID to pass into callback
                        hidden_student_id = gr.Textbox(value=student_id, visible=False, interactive=False, show_label=False)
                        
                        # Chat button with correct event binding
                        btn = gr.Button("Start Chat", elem_classes="chat-btn")
                        btn.click(
                            select_student_direct,
                            inputs=[hidden_student_id, history_dict_state],
                            outputs=[
                                selection_page, 
                                chat_page, 
                                selected_id_state, 
                                name_display, 
                                model_display,
                                chatbot  # ✅ 如果你在 select_student_direct 中更新 avatar_images，这里会自动刷新头像
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
