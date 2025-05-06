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
    
    # Debug print for server logs
    print(f"Selecting student: {student_id}, Name: {student_name}")
    
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
    
    # Define chat page components first
    with chat_page:
        # Chat header with student info - centered design without avatar
        with gr.Row(elem_classes="chat-header"):
            back_button = gr.Button("← Back", elem_classes="back-btn")
            
            # Student information - centered, no avatar for cleaner look
            with gr.Column(elem_classes="center-header"):
                name_display = gr.Markdown("Student Name", elem_id="student-name-header")
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
            # Title image with transparent background
            with gr.Column(elem_classes="header-image-container"):
                gr.Image(
                    value="avatar/brain_with_title.png",
                    show_label=False,
                    elem_classes="header-image",
                    height=120,
                    container=False,  # This helps remove container styling
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
                        # Title case for student names (not all caps)
                        gr.Markdown(f"<strong style='color:white;font-weight:900;letter-spacing:1px;text-shadow:0 1px 2px rgba(0,0,0,0.3);'>{student_name}</strong>", elem_classes="card-header")
                        
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
                        
                        # Chat button with click handler - Create a unique ID for each button
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

    # Add troubleshooting JavaScript to fix navigation issues and style fixes
    demo.load(None, None, None, js="""
    function() {
        // Helper function to log UI state for debugging
        function logUIState() {
            console.log("Selection page visibility:", document.querySelector('.character-grid')?.closest('[class*="group"]')?.style.display);
            console.log("Chat page visibility:", document.querySelector('.chat-header')?.closest('[class*="group"]')?.style.display);
        }
        
        // Remove white background from header image
        function fixHeaderImage() {
            // Find all elements related to the header image and remove backgrounds
            document.querySelectorAll('.header-image, .header-image-container, .header-image > div, .header-image img').forEach(el => {
                if (el) {
                    el.style.backgroundColor = 'transparent';
                    el.style.border = 'none';
                    el.style.boxShadow = 'none';
                    el.style.padding = '0';
                    el.style.margin = '0';
                    
                    // Also remove parent containers' styling
                    if (el.parentElement) {
                        el.parentElement.style.backgroundColor = 'transparent';
                        el.parentElement.style.border = 'none';
                        el.parentElement.style.boxShadow = 'none';
                    }
                }
            });
            
            // Target the specific wrapper div that Gradio creates
            const imageWrappers = document.querySelectorAll('.gradio-image, .gradio-image > div, [data-testid="image"], [data-testid="image"] > div');
            imageWrappers.forEach(wrapper => {
                if (wrapper && wrapper.closest('.header-image-container, .header-image')) {
                    wrapper.style.backgroundColor = 'transparent';
                    wrapper.style.border = 'none';
                    wrapper.style.boxShadow = 'none';
                    wrapper.style.padding = '0';
                    wrapper.style.margin = '0';
                }
            });
        }
        
        // Make the entire character card clickable (not just the button)
        function makeCardsClickable() {
            document.querySelectorAll('.character-card').forEach(card => {
                card.style.cursor = 'pointer';
                // Only add click handler if not already added
                if (!card.dataset.handlerAttached) {
                    card.dataset.handlerAttached = 'true';
                    card.addEventListener('click', function(e) {
                        // Don't trigger if clicking on the button itself (to avoid double events)
                        if (!e.target.classList.contains('chat-btn') && !e.target.closest('.chat-btn')) {
                            // Find the button inside this card and click it
                            const chatBtn = this.querySelector('.chat-btn');
                            if (chatBtn) {
                                console.log("Card clicked, triggering button click");
                                chatBtn.click();
                                
                                // Manual UI visibility update
                                setTimeout(() => {
                                    try {
                                        const selectionGroup = document.querySelector('.character-grid').closest('[class*="group"]');
                                        const chatGroup = document.querySelector('.chat-header').closest('[class*="group"]');
                                        
                                        if (selectionGroup && chatGroup) {
                                            selectionGroup.style.display = 'none';
                                            chatGroup.style.display = 'block';
                                            console.log("Manual visibility update applied");
                                        }
                                    } catch (err) {
                                        console.error("Error in visibility update:", err);
                                    }
                                }, 300);
                            }
                        }
                    });
                }
            });
        }
        
        // Add explicit click handlers to chat buttons
        function fixChatButtons() {
            document.querySelectorAll('.chat-btn').forEach(btn => {
                // Only add click handler if not already added
                if (!btn.dataset.fixedHandler) {
                    btn.dataset.fixedHandler = 'true';
                    
                    // Store the original click handlers
                    const originalClickHandlers = [...btn.listeners?.('click') || []];
                    
                    // Remove and re-add event listeners to ensure our handler runs last
                    btn.removeEventListener('click', btn.onclick);
                    btn.addEventListener('click', function(e) {
                        console.log("Chat button clicked");
                        
                        // Call original handlers
                        if (originalClickHandlers && originalClickHandlers.length) {
                            originalClickHandlers.forEach(handler => {
                                if (typeof handler === 'function') {
                                    handler.call(this, e);
                                }
                            });
                        }
                        
                        // Ensure visibility state changes properly
                        setTimeout(() => {
                            try {
                                const selectionGroup = document.querySelector('.character-grid').closest('[class*="group"]');
                                const chatGroup = document.querySelector('.chat-header').closest('[class*="group"]');
                                
                                if (selectionGroup && chatGroup) {
                                    selectionGroup.style.display = 'none';
                                    chatGroup.style.display = 'block';
                                    console.log("Manual button visibility update applied");
                                }
                            } catch (err) {
                                console.error("Error in button visibility update:", err);
                            }
                        }, 300);
                    });
                }
            });
        }
        
        // Add debug click handler to back button
        function fixBackButton() {
            const backBtn = document.querySelector('.back-btn');
            if (backBtn && !backBtn.dataset.fixedHandler) {
                backBtn.dataset.fixedHandler = 'true';
                backBtn.addEventListener('click', function() {
                    console.log("Back button clicked");
                    
                    // Force visibility update after a short delay
                    setTimeout(() => {
                        try {
                            const selectionGroup = document.querySelector('.character-grid').closest('[class*="group"]');
                            const chatGroup = document.querySelector('.chat-header').closest('[class*="group"]');
                            
                            if (selectionGroup && chatGroup) {
                                selectionGroup.style.display = 'block';
                                chatGroup.style.display = 'none';
                                console.log("Manual back button visibility update applied");
                            }
                        } catch (err) {
                            console.error("Error in back button visibility update:", err);
                        }
                    }, 300);
                });
            }
        }
        
        // Style chat avatars to fill entire container
        function styleAvatars() {
            document.querySelectorAll('.gradio-chatbot .avatar img, .gradio-chatbot img.avatar-image').forEach(img => {
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.borderRadius = '50%';
                img.style.border = 'none';
                img.style.objectFit = 'cover';
                img.style.padding = '0';
                img.style.margin = '0';
                
                // Style parent container
                if (img.parentElement) {
                    img.parentElement.style.width = '48px';
                    img.parentElement.style.height = '48px';
                    img.parentElement.style.border = '2px solid rgba(9, 64, 103, 0.85)';
                    img.parentElement.style.borderRadius = '50%';
                    img.parentElement.style.overflow = 'hidden';
                    img.parentElement.style.padding = '0';
                    img.parentElement.style.margin = '0';
                    img.parentElement.style.backgroundColor = 'transparent';
                    img.parentElement.style.boxShadow = 'none';
                }
            });
        }
        
        // Apply all fixes initially
        setTimeout(() => {
            fixHeaderImage();
            makeCardsClickable();
            fixChatButtons();
            fixBackButton();
            styleAvatars();
            logUIState();
        }, 500);
        
        // Set up a mutation observer to watch for DOM changes and reapply fixes
        const observer = new MutationObserver(function(mutations) {
            fixHeaderImage();
            makeCardsClickable();
            fixChatButtons();
            fixBackButton();
            styleAvatars();
        });
        
        // Start observing the entire document for changes to catch all UI updates
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Also periodically call the fixes for better reliability
        setInterval(() => {
            fixHeaderImage();
            makeCardsClickable();
            fixChatButtons();
            fixBackButton();
            styleAvatars();
        }, 2000);
    }
    """)

# Run the application when script is executed directly
if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 7860))
    
    # Launch the application with appropriate server configuration
    demo.launch(
        server_name="0.0.0.0",  # Make the server publicly available
        server_port=port,       # Use the specified port
        share=False,            # Don't create a public share link (handled by hosting platform)
        debug=True,             # Enable debug mode to help with troubleshooting
        favicon_path="avatar/brain_with_title.png",  # Set favicon for browser tab
        show_api=False          # Hide API documentation
    )
