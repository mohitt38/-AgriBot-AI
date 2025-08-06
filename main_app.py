import streamlit as st
import os
import sys
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Import your orchestrator (adjust path as needed)
try:
    from orchestrator import SimpleAgenticOrchestrator
except ImportError:
    st.error("Could not import SimpleAgenticOrchestrator. Please ensure the file is in the same directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🌾 AgriBot AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI - Compatible with both light and dark themes
st.markdown("""
<style>
    /* Main header with theme-aware colors */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #4CAF50, #81C784);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Feature cards with theme-aware backgrounds */
    .feature-card {
        background: var(--background-color, rgba(255, 255, 255, 0.15));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid rgba(76, 175, 80, 0.4);
        border-left: 4px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        color: var(--text-color);
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        border-color: rgba(76, 175, 80, 0.6);
        background: rgba(76, 175, 80, 0.1);
    }
    
    .feature-card h3 {
        color: #4CAF50 !important;
        margin-bottom: 1rem !important;
        font-weight: bold !important;
    }
    
    .feature-card p {
        margin-bottom: 0.8rem !important;
        line-height: 1.5 !important;
    }
    
    .feature-card strong {
        color: #66BB6A !important;
        font-weight: bold !important;
    }
    
    /* Agent status badges */
    .agent-status {
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: bold;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.9rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .agent-active {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .agent-inactive {
        background: linear-gradient(135deg, #F44336, #EF5350);
        color: white;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .agent-status:hover {
        transform: scale(1.05);
    }
    
    /* Chat messages with better contrast */
    .chat-message {
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        border-left: 4px solid #4CAF50;
        backdrop-filter: blur(5px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .chat-message:hover {
        transform: translateX(3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    /* User message - Blue theme */
    .user-message {
        background: rgba(33, 150, 243, 0.1);
        border-left-color: #2196F3;
        border: 1px solid rgba(33, 150, 243, 0.2);
    }
    
    /* Bot message - Green theme */
    .bot-message {
        background: rgba(76, 175, 80, 0.1);
        border-left-color: #4CAF50;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Dark theme specific adjustments */
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background: rgba(40, 40, 40, 0.9) !important;
            border: 2px solid rgba(76, 175, 80, 0.5) !important;
            border-left: 4px solid #4CAF50 !important;
            color: #E8F5E8 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        }
        
        .feature-card:hover {
            background: rgba(50, 50, 50, 0.95) !important;
            border-color: rgba(76, 175, 80, 0.7) !important;
            box-shadow: 0 6px 25px rgba(76, 175, 80, 0.3) !important;
        }
        
        .feature-card h3 {
            color: #81C784 !important;
        }
        
        .feature-card p {
            color: #E8F5E8 !important;
        }
        
        .feature-card strong {
            color: #A5D6A7 !important;
        }
        
        .user-message {
            background: rgba(33, 150, 243, 0.2) !important;
            color: #E3F2FD !important;
            border: 1px solid rgba(33, 150, 243, 0.4) !important;
        }
        
        .bot-message {
            background: rgba(76, 175, 80, 0.2) !important;
            color: #E8F5E8 !important;
            border: 1px solid rgba(76, 175, 80, 0.4) !important;
        }
        
        .metric-card {
            background: rgba(40, 40, 40, 0.9) !important;
            border: 1px solid rgba(76, 175, 80, 0.3) !important;
            color: #E8F5E8 !important;
        }
    }
    
    /* Light theme specific adjustments */
    @media (prefers-color-scheme: light) {
        .feature-card {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(76, 175, 80, 0.4) !important;
            color: #2E7D32 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        
        .feature-card:hover {
            background: rgba(248, 255, 248, 1) !important;
            border-color: rgba(76, 175, 80, 0.6) !important;
        }
        
        .feature-card h3 {
            color: #388E3C !important;
        }
        
        .feature-card p {
            color: #2E7D32 !important;
        }
        
        .feature-card strong {
            color: #4CAF50 !important;
        }
        
        .user-message {
            background: rgba(227, 242, 253, 0.9) !important;
            color: #1565C0 !important;
            border: 1px solid rgba(33, 150, 243, 0.3) !important;
        }
        
        .bot-message {
            background: rgba(241, 248, 233, 0.9) !important;
            color: #2E7D32 !important;
            border: 1px solid rgba(76, 175, 80, 0.3) !important;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            color: #2E7D32 !important;
        }
    }
    
    /* Streamlit specific overrides for better theme compatibility */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #66BB6A) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: bold !important;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4) !important;
        background: linear-gradient(135deg, #66BB6A, #4CAF50) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(76, 175, 80, 0.1) !important;
        border: 2px dashed rgba(76, 175, 80, 0.4) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border: 2px solid rgba(76, 175, 80, 0.3) !important;
        border-radius: 15px !important;
        padding: 0.8rem 1rem !important;
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(76, 175, 80, 0.05) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1) !important;
        border: 1px solid rgba(76, 175, 80, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.1) !important;
        border: 1px solid rgba(244, 67, 54, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.1) !important;
        border: 1px solid rgba(255, 152, 0, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Spinner overlay */
    .stSpinner > div {
        border-color: #4CAF50 transparent #4CAF50 transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = SimpleAgenticOrchestrator()
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'user_context' not in st.session_state:
    st.session_state.user_context = {}

# Sidebar
with st.sidebar:
    st.markdown("## 🤖 System Status")
    
    # Agent status display
    agents = st.session_state.orchestrator.agents
    st.markdown("### Available Agents")
    
    agent_names = {
        'crop_advisor': '🌱 Crop Advisor',
        'market_broker': '🤝 Market Broker', 
        'disease_detector': '🔬 Disease Detector',
        'alert_system': '⚠️ Alert System'
    }
    
    for agent_key, agent_name in agent_names.items():
        status = "active" if agent_key in agents else "inactive"
        status_class = "agent-active" if agent_key in agents else "agent-inactive"
        st.markdown(f'<div class="agent-status {status_class}">{agent_name}</div>', 
                   unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User context display
    st.markdown("### 📋 Your Profile")
    if st.session_state.user_context:
        for key, value in st.session_state.user_context.items():
            if key == 'interests':
                st.write("*Interests:*")
                for interest, count in value.items():
                    st.write(f"• {interest.title()}: {count} queries")
            else:
                st.write(f"{key.title()}:** {value}")
    else:
        st.write("No profile data yet. Start chatting to build your profile!")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    total_queries = len(st.session_state.chat_history)
    st.metric("Total Queries", total_queries)
    
    if st.session_state.chat_history:
        with_images = sum(1 for chat in st.session_state.chat_history if chat.get('had_image'))
        st.metric("Image Analyses", with_images)
    
    # Clear chat button
    if st.button("🗑 Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.user_context = {}
        st.rerun()

# Main content
st.markdown('<h1 class="main-header">🌾 AgriBot AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your intelligent farming companion powered by multiple AI agents</p>', unsafe_allow_html=True)

# Feature overview (show only if no chat history)
if not st.session_state.chat_history:
    st.markdown("## 🚀 What I Can Help You With")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🌱 Crop Advisory</h3>
            <p>Get personalized crop recommendations based on your soil type, location, and climate conditions.</p>
            <p><strong>Try:</strong> "What crops should I grow in red soil in Rajasthan?"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🤝 Market Intelligence</h3>
            <p>Find the best places to sell your crops and get current market pricing information.</p>
            <p><strong>Try:</strong> "Where can I sell wheat in Punjab?"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔬 Disease Detection</h3>
            <p>Upload crop images to identify diseases, pests, and get treatment recommendations.</p>
            <p><strong>Try:</strong> Upload a photo of diseased leaves</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>⚠️ Disease Alerts</h3>
            <p>Get alerts about disease outbreaks and pest problems in your area.</p>
            <p><strong>Try:</strong> "Any disease alerts in my area?"</p>
        </div>
        """, unsafe_allow_html=True)

# Chat interface
st.markdown("## 💬 Chat with AI Assistant")

# Display chat history
chat_container = st.container()
with chat_container:
    for i, chat in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👨‍🌾 You:</strong> {chat['user_input']}
            {f"<br><small>📷 Image attached</small>" if chat.get('had_image') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # Bot response
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Smart Crop AI:</strong><br>
            {chat['response']}
            <br><small style="color: #666;">
                🎯 Intent: {chat.get('intent', 'N/A')} | 
                🤖 Agents: {', '.join(chat.get('agents_called', []))} |
                ⏰ {datetime.fromisoformat(chat['timestamp']).strftime('%H:%M:%S')}
            </small>
        </div>
        """, unsafe_allow_html=True)

# Initialize example query state
if 'example_query' not in st.session_state:
    st.session_state.example_query = ""

# Example questions
st.markdown("### 💡 Quick Examples")
example_col1, example_col2, example_col3, example_col4 = st.columns(4)

with example_col1:
    if st.button("🌱 Crop Advice", help="Get crop recommendations"):
        st.session_state.example_query = "What crops should I grow in black soil in Maharashtra?"

with example_col2:
    if st.button("🔬 Disease Help", help="Get disease information"):
        st.session_state.example_query = "My wheat crop has yellow spots on leaves"

with example_col3:
    if st.button("🤝 Market Info", help="Get market information"):
        st.session_state.example_query = "Where can I sell rice in Punjab?"

with example_col4:
    if st.button("⚠️ Alerts", help="Check disease alerts"):
        st.session_state.example_query = "Any disease alerts in Rajasthan?"

# Input section
st.markdown("---")
input_col1, input_col2 = st.columns([3, 1])

with input_col1:
    # Use the example query as default value if available
    default_value = st.session_state.example_query if st.session_state.example_query else ""
    user_input = st.text_input(
        "Ask me anything about farming...",
        value=default_value,
        placeholder="e.g., 'My tomato leaves have brown spots' or 'Best crops for sandy soil?'",
        key="user_input_field"
    )

with input_col2:
    uploaded_file = st.file_uploader(
        "Upload crop image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image for disease detection"
    )

# Process input
send_button = st.button("🚀 Send Message", type="primary")

# Simple processing without complex state management
if send_button:
    if user_input and user_input.strip():
        # Clear the example query immediately to prevent reprocessing
        st.session_state.example_query = ""
            
        with st.spinner("🧠 AI agents are analyzing your query..."):
            try:
                # Process the request
                response = st.session_state.orchestrator.process_request(
                    user_input, 
                    image_file=uploaded_file
                )
                
                # Add to chat history
                chat_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "user_input": user_input,
                    "response": response,
                    "had_image": uploaded_file is not None
                }
                
                # Get additional info from orchestrator's history
                if st.session_state.orchestrator.conversation_history:
                    last_conversation = st.session_state.orchestrator.conversation_history[-1]
                    chat_entry.update({
                        "intent": last_conversation.get("intent"),
                        "agents_called": last_conversation.get("agents_called", []),
                        "primary_task": last_conversation.get("primary_task")
                    })
                
                st.session_state.chat_history.append(chat_entry)
                
                # Update user context
                st.session_state.user_context = st.session_state.orchestrator.user_context
                
                # Show success message
                st.success("✅ Response generated successfully!")
                
                # Rerun to show the new chat
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing your request: {str(e)}")
                st.error("Please check if all agents are properly loaded and try again.")
                # Clear states on error
                st.session_state.example_query = ""
                
    else:
        st.warning("Please enter a question or upload an image!")
        # Clear any pending example query
        st.session_state.example_query = ""

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌾 AgriBot AI - Grow Smarter , Farm Better .</p>
    <p>Built with ❤ for the farming community</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for real-time updates (optional)
if st.session_state.chat_history:
    st.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")