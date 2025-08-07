# LinkedIn & Gmail Bot with Model Context Protocol (MCP)

This project extends the MCP concept to create a LinkedIn and Gmail automation bot using the Model Context Protocol (MCP). It allows users to post content to LinkedIn and send emails through Gmail using AI-powered automation.

## Features

- 📝 **LinkedIn Posting**: Create and publish professional LinkedIn posts
- 📧 **Gmail Integration**: Send emails directly through Gmail
- 🤖 **AI-Powered**: Uses Google Gemini 2.5 Flash for intelligent content processing
- 🔄 **Flexible Actions**: Choose between LinkedIn posting, email sending, or both
- 📊 **Real-time Progress**: Live progress tracking with visual feedback
- 🎨 **User-friendly Interface**: Clean Streamlit-based UI

## Prerequisites

- Python 3.10+
- Google AI Studio API Key
- Pipedream URLs for LinkedIn and Gmail integrations

## Installation

1. Ensure you have the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, you'll need to set up:

1. **Google API Key**: For AI model access
2. **Pipedream URLs**:
   - LinkedIn URL (required)
   - Gmail URL (required)

## Running the Application

To start the LinkedIn & Gmail bot, run:
```bash
streamlit run linkedin_gmail_app.py
```

The application will be available at `http://localhost:8501` by default.

## Usage

### 1. Configuration Setup
- Enter your Google AI Studio API key in the sidebar
- Provide your Pipedream URLs for LinkedIn and Gmail
- Select the action type (LinkedIn Post, Send Email, or Both)

### 2. LinkedIn Posting
- **Post Content**: Write your LinkedIn post content
- **Hashtags**: Add relevant hashtags (optional)
- **Visibility**: Choose post visibility (Public, Connections, Private)

### 3. Email Sending
- **Recipient**: Enter the recipient's email address
- **Subject**: Write a clear email subject
- **Message**: Compose your email content
- **Priority**: Set email priority (Normal, High, Low)

### 4. Execute Actions
- Click "Execute Action" to process your request
- Monitor real-time progress updates
- View results and confirmations

## Project Structure

- `linkedin_gmail_app.py` - Main Streamlit application
- `linkedin_gmail_utils.py` - Utility functions and MCP integration
- `linkedin_gmail_prompt.py` - AI prompt template
- `README_linkedin_gmail.md` - This documentation

## Action Types

### LinkedIn Post
- Creates and publishes professional LinkedIn posts
- Supports hashtags and visibility settings
- Follows LinkedIn's community guidelines

### Send Email
- Sends emails through Gmail integration
- Supports priority levels and proper formatting
- Provides delivery confirmation

### Both Actions
- Executes LinkedIn posting and email sending sequentially
- Provides comprehensive confirmation for both actions

## Error Handling

The application includes robust error handling:
- API key validation
- URL validation
- Content validation
- Graceful error recovery
- Clear error messages

## Security Features

- Secure API key input (password field)
- Input validation and sanitization
- Error logging without exposing sensitive data

## Integration with Original Project

This implementation follows the same MCP pattern as the original learning path generator:
- Uses the same MCP client architecture
- Follows similar progress tracking patterns
- Maintains consistent UI/UX design
- Uses the same error handling approach

## Future Enhancements

Potential improvements could include:
- Scheduled posting capabilities
- Email templates
- Analytics and reporting
- Multi-account support
- Advanced content formatting options 