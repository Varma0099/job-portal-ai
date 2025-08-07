import streamlit as st
import requests
import json

st.set_page_config(page_title="Simple LinkedIn & Gmail Bot", page_icon="📧", layout="wide")

st.title("Simple LinkedIn & Gmail Bot")

# Initialize session state for progress
if 'current_step' not in st.session_state:
    st.session_state.current_step = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'last_section' not in st.session_state:
    st.session_state.last_section = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# Sidebar for API and URL configuration
st.sidebar.header("Configuration")

# Pipedream URLs
st.sidebar.subheader("Pipedream URLs")
linkedin_pipedream_url = st.sidebar.text_input("LinkedIn URL (Required)", 
    placeholder="Enter your Pipedream LinkedIn URL")

gmail_pipedream_url = st.sidebar.text_input("Gmail URL (Required)", 
    placeholder="Enter your Pipedream Gmail URL")

# Action selection
action_type = st.sidebar.radio(
    "Select Action:",
    ["LinkedIn Post", "Send Email", "Both"]
)

# Quick guide
st.info("""
*Quick Guide:*
1. Enter your LinkedIn and Gmail Pipedream URLs (required)
2. Select the action you want to perform
3. Enter your content details:
   - For LinkedIn: Post content, hashtags, etc.
   - For Email: Recipient, subject, message content
   - For Both: Complete details for both actions
""")

# Main content area
st.header("Content Creation")

# LinkedIn Post Section
if action_type in ["LinkedIn Post", "Both"]:
    st.subheader("LinkedIn Post Details")
    linkedin_content = st.text_area("Post Content:", 
                                   placeholder="Write your LinkedIn post content here...",
                                   height=150)
    linkedin_hashtags = st.text_input("Hashtags (optional):", 
                                     placeholder="#ai #technology #innovation")
    linkedin_visibility = st.selectbox("Post Visibility:", 
                                      ["Public", "Connections", "Private"])

# Email Section
if action_type in ["Send Email", "Both"]:
    st.subheader("Email Details")
    email_recipient = st.text_input("Recipient Email:", 
                                   placeholder="recipient@example.com")
    email_subject = st.text_input("Email Subject:", 
                                 placeholder="Enter email subject")
    email_content = st.text_area("Email Message:", 
                                placeholder="Write your email message here...",
                                height=150)
    email_priority = st.selectbox("Email Priority:", 
                                 ["Normal", "High", "Low"])

# Progress area
progress_container = st.container()
progress_bar = st.empty()

def update_progress(message: str):
    """Update progress in the Streamlit UI"""
    st.session_state.current_step = message
    
    # Determine section and update progress
    if "Processing LinkedIn post" in message:
        section = "LinkedIn"
        st.session_state.progress = 0.3
    elif "Processing email" in message:
        section = "Email"
        st.session_state.progress = 0.6
    elif "Action completed successfully" in message:
        section = "Complete"
        st.session_state.progress = 1.0
        st.session_state.is_generating = False
    else:
        section = st.session_state.last_section or "Progress"
    
    st.session_state.last_section = section
    
    # Show progress bar
    progress_bar.progress(st.session_state.progress)
    
    # Update progress container with current status
    with progress_container:
        # Show section header if it changed
        if section != st.session_state.last_section and section != "Complete":
            st.write(f"*{section}*")
        
        # Show message with tick for completed steps
        if "Action completed successfully" in message:
            st.success("All steps completed! 🎉")
        else:
            prefix = "✓" if st.session_state.progress >= 0.6 else "→"
            st.write(f"{prefix} {message}")

def send_linkedin_post(url: str, content: str, hashtags: str, visibility: str):
    """Send LinkedIn post via Pipedream"""
    try:
        payload = {
            "content": content,
            "hashtags": hashtags,
            "visibility": visibility
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"LinkedIn post error: {str(e)}")
        return None

def send_email(url: str, recipient: str, subject: str, content: str, priority: str):
    """Send email via Pipedream"""
    try:
        payload = {
            "recipient": recipient,
            "subject": subject,
            "content": content,
            "priority": priority
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return None

# Execute Action button
if st.button("Execute Action", type="primary", disabled=st.session_state.is_generating):
    if not linkedin_pipedream_url:
        st.error("LinkedIn URL is required. Please enter your Pipedream LinkedIn URL in the sidebar.")
    elif not gmail_pipedream_url:
        st.error("Gmail URL is required. Please enter your Pipedream Gmail URL in the sidebar.")
    else:
        # Validate content based on action type
        if action_type == "LinkedIn Post" and not linkedin_content:
            st.warning("Please enter LinkedIn post content.")
        elif action_type == "Send Email" and (not email_recipient or not email_subject or not email_content):
            st.warning("Please fill in all email fields (recipient, subject, and message).")
        elif action_type == "Both" and (not linkedin_content or not email_recipient or not email_subject or not email_content):
            st.warning("Please fill in all required fields for both LinkedIn and email.")
        else:
            try:
                # Set generating flag
                st.session_state.is_generating = True
                
                # Reset progress
                st.session_state.current_step = ""
                st.session_state.progress = 0
                st.session_state.last_section = ""
                
                results = []
                
                # Process LinkedIn post
                if action_type in ["LinkedIn Post", "Both"]:
                    update_progress("Processing LinkedIn post...")
                    linkedin_result = send_linkedin_post(
                        linkedin_pipedream_url,
                        linkedin_content,
                        linkedin_hashtags,
                        linkedin_visibility
                    )
                    if linkedin_result:
                        results.append(f"✅ LinkedIn post sent successfully!")
                    else:
                        results.append("❌ LinkedIn post failed")
                
                # Process email
                if action_type in ["Send Email", "Both"]:
                    update_progress("Processing email...")
                    email_result = send_email(
                        gmail_pipedream_url,
                        email_recipient,
                        email_subject,
                        email_content,
                        email_priority
                    )
                    if email_result:
                        results.append(f"✅ Email sent successfully to {email_recipient}!")
                    else:
                        results.append("❌ Email failed")
                
                update_progress("Action completed successfully!")
                
                # Display results
                st.header("Action Results")
                for result in results:
                    st.markdown(f"📧 {result}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check your URLs and try again.")
                st.session_state.is_generating = False