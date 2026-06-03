import streamlit as st
from chatbot import get_response
from database import create_tables, save_chat
from auth import create_user_table, register, login

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Remove default padding and margins */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 1200px;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        margin-top: 0;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    /* Compact header for chat interface */
    .compact-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        margin-top: 0;
        text-align: center;
    }
    
    .compact-header h1 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
    }
    
    .compact-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 0.25rem;
        font-size: 0.9rem;
        margin-bottom: 0;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    /* User message styling */
    div[data-testid="stChatMessage"][data-role="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Assistant message styling */
    div[data-testid="stChatMessage"][data-role="assistant"] {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        color: #333;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        color: white;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        transition: border-color 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: none;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stChatInput > div > div > textarea:focus {
        border-color: #667eea;
    }
    
    /* Success/Error message styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    
    .stSuccess {
        border-left-color: #28a745;
    }
    
    .stError {
        border-left-color: #dc3545;
    }
    
    /* Welcome card styling */
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .welcome-avatar {
        font-size: 2rem;
        background: rgba(255,255,255,0.2);
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
    }
    
    .welcome-text {
        flex: 1;
    }
    
    .welcome-greeting {
        display: block;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 0.2rem;
    }
    
    .username-highlight {
        display: block;
        font-size: 1.3rem;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Info box styling */
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #2196f3;
    }
    
    /* Feature grid styling */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        margin-bottom: 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Remove extra spacing from columns */
    .row-widget.stButton {
        margin-bottom: 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Reduce expander spacing */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        padding: 0.5rem;
    }
    
    /* Container spacing fixes */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database tables
create_tables()
create_user_table()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar content
with st.sidebar:
    st.markdown("### 🎓 AI Student Assistant")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        menu = st.selectbox(
            "Menu",
            ["Login", "Register"],
            format_func=lambda x: f"🔐 {x}" if x == "Login" else f"📝 {x}"
        )
    else:
        # Fixed indentation here - the welcome card was incorrectly indented
        st.markdown(f"""
        <div class='welcome-card'>
            <div class='welcome-avatar'>👋</div>
            <div class='welcome-text'>
                <span class='welcome-greeting'>Welcome back,</span>
                <span class='username-highlight'>{st.session_state.username}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.info(f"💬 Messages: {len(st.session_state.messages)}")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# Main content area
if not st.session_state.logged_in:
    # Landing page for non-logged in users
    st.markdown("""
    <div class='main-header'>
        <h1>🎓 AI-Powered Student Assistant</h1>
        <p>Your 24/7 companion for programming, AI/ML, career guidance, and interview preparation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication forms
    if menu == "Register":
        st.markdown("### 📝 Create New Account")
        st.markdown("Join us to start your learning journey!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_user = st.text_input("Username", placeholder="Choose a username")
            new_pass = st.text_input("Password", type="password", placeholder="Choose a strong password")
            
            if st.button("Register Account", use_container_width=True):
                if new_user and new_pass:
                    if register(new_user, new_pass):
                        st.success("✅ Registration Successful! Please login to continue.")
                    else:
                        st.error("❌ User already exists. Please choose a different username.")
                else:
                    st.warning("⚠️ Please fill in all fields.")
    
    elif menu == "Login":
        st.markdown("### 🔐 Login to Your Account")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login", use_container_width=True):
                if username and password:
                    if login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password.")

else:
    # Main chat interface for logged-in users
    # Use compact header to reduce white space
    st.markdown("""
    <div class='compact-header'>
        <h1>💬 AI Student Assistant</h1>
        <p>Ask me anything about programming, AI/ML, career, or interviews!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Info box - now more compact
    with st.expander("ℹ️ Quick Tips", expanded=False):
        st.markdown("""
        • **Be specific** with your questions  
        • **Provide context** when asking about code  
        • **Use code blocks** for code snippets  
        • **Ask one question at a time**
        """)
    
    # Create a container for chat with proper spacing
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages with proper spacing
        if st.session_state.messages:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        else:
            # Show welcome message when no messages
            st.info("💡 Start a conversation by typing your question below!")
    
    # Chat input with better placement
    user_query = st.chat_input(
        "Type your question here... (e.g., 'How to learn Python?', 'What is ML?')",
        key="chat_input"
    )
    
    if user_query:
        try:
            if user_query.strip() == "":
                st.warning("⚠️ Please enter a valid question.")
            else:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_query
                })
                
                with st.chat_message("user"):
                    st.markdown(user_query)
                
                # Get response
                with st.spinner("🤔 Thinking..."):
                    answer = get_response(user_query)
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                
                with st.chat_message("assistant"):
                    st.markdown(answer)
                
                # Save to database
                save_chat(st.session_state.username, user_query, answer)
                
                # Rerun to update the chat display
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please try again or rephrase your question.")
    
    # Quick question suggestions - only show if no messages
    if len(st.session_state.messages) == 0:
        st.markdown("---")
        st.markdown("### 📌 Quick Start Questions")
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        quick_questions = [
            ("💻", "Best Python libraries for data science?", col1),
            ("🤖", "Explain neural networks simply", col1),
            ("🎯", "How to prepare for technical interviews?", col2),
            ("🚀", "Best AI/ML learning resources?", col2)
        ]
        
        for icon, question, col in quick_questions:
            with col:
                if st.button(f"{icon} {question}", use_container_width=True, key=question):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": question
                    })
                    st.rerun()

# Footer - reduced top margin
st.markdown("""
<div class='footer'>
    <p>🎓 AI Student Assistant | Powered by Advanced AI | 24/7 Support</p>
    <p style='font-size: 0.8rem; margin-top: 0.25rem;'>Your guide for academic & career success</p>
</div>
""", unsafe_allow_html=True)