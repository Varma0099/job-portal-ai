import streamlit as st
from linkedin_gmail_utils import run_agent_sync

st.set_page_config(page_title="MCP AI Bot", page_icon="🤖", layout="wide")

st.title("Model Context Protocol (MCP) - Unified AI Bot")

# Initialize session state
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Sidebar
st.sidebar.header("Configuration")
google_api_key = st.sidebar.text_input("Google API Key", type="password")
linkedin_pipedream_url = st.sidebar.text_input("LinkedIn URL", placeholder="Enter your LinkedIn Pipedream URL")
gmail_pipedream_url = st.sidebar.text_input("Gmail URL", placeholder="Enter your Gmail Pipedream URL")

st.info("""
**How to Use:**
Type your instruction below like:
- "Send an email to abc@gmail.com with subject 'Meeting' and say 'Let’s connect tomorrow'"
- "Post on LinkedIn saying 'Excited to join the AI revolution!' with hashtags #AI #ML"
""")

# User Input (Single Chat Input)
user_instruction = st.text_area("Your instruction to the AI bot:", height=150, placeholder="Describe what you want the bot to do...")

# Progress bar
progress_bar = st.empty()

def update_progress(message: str):
    st.session_state.progress += 0.2
    st.session_state.progress = min(st.session_state.progress, 1.0)
    progress_bar.progress(st.session_state.progress)
    st.write(f"→ {message}")

# Execute Action
if st.button("Execute", type="primary", disabled=st.session_state.is_generating):
    if not google_api_key or not linkedin_pipedream_url or not gmail_pipedream_url:
        st.error("Please fill in all API keys and Pipedream URLs.")
    elif not user_instruction.strip():
        st.warning("Please enter an instruction.")
    else:
        st.session_state.is_generating = True
        st.session_state.progress = 0

        try:
            result = run_agent_sync(
                google_api_key=google_api_key,
                linkedin_pipedream_url=linkedin_pipedream_url,
                gmail_pipedream_url=gmail_pipedream_url,
                content_data={
                    "instruction": user_instruction.strip()
                },
                progress_callback=update_progress
            )

            st.header("Result")
            if result and "messages" in result:
                for msg in result["messages"]:
                    st.markdown(f"📧 {msg.content}")
            else:
                st.error("No response received. Try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            st.session_state.is_generating = False
