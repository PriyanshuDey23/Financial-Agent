import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - YouTube Video Agent",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬")
st.header("Powered by Gemini 2.0 Flash Exp")

# Helper function to extract YouTube video ID
def get_video_id(youtube_url):
    try:
        if "youtu.be" in youtube_url:
            return youtube_url.split("/")[-1]
        elif "youtube.com" in youtube_url and "v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        else:
            raise ValueError("Invalid YouTube URL format. Please provide a valid link.")
    except Exception as e:
        raise ValueError(f"Error extracting video ID: {e}")


# Function to fetch the transcript from YouTube
def fetch_transcript(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except TranscriptsDisabled:
        st.error("Subtitles are disabled for this video. Unable to fetch the transcript.")
        return None
    except Exception as e:
        st.error(f"Failed to fetch transcript: {e}")
        return None

# Initialize Agent
@st.cache_resource
def initialize_agent():
    return Agent(
        name="YouTube Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )
# Instantiate the agent
multimodal_Agent = initialize_agent()



# Streamlit UI
youtube_link = st.text_input("Enter the YouTube Video Link:")

if youtube_link:
    try:
        video_id = get_video_id(youtube_link)
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        st.success(f"Video ID: {video_id}")
    except ValueError as e:
        st.error(str(e))

# Streamlit UI: User query input
user_query = st.text_area(
    "What insights are you seeking from the video?",
    placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
    help="Provide specific questions or insights you want from the video."
)

# Analyze button
if st.button("🔍 Analyze Video"):
    if not youtube_link:
        st.warning("Please provide a valid YouTube link.")
    elif not user_query:
        st.warning("Please enter a question or insight to analyze the video.")
    else:
        try:
            with st.spinner("Processing video and gathering insights..."):
                # Extract the transcript
                video_id = get_video_id(youtube_link)
                transcript = fetch_transcript(video_id)

                if transcript:
                    # Generate the prompt for analysis
                    analysis_prompt = f"""
                    You are an intelligent assistant with access to a YouTube video transcript and web search tools.
                    Your task is to answer the user's query by:
                    1. Understanding the video transcript.
                    2. Supplementing the response with relevant information from web searches.

                    Transcript:
                    {transcript}

                    User Query: {user_query}

                    Provide a clear, concise, and actionable response. Include references to both the transcript and additional web findings when needed.
                    """

                    # Process the prompt using the AI agent
                    response = multimodal_Agent.run(analysis_prompt)

                    # Display the results
                    st.subheader("Analysis Result")
                    st.markdown(response.content)
                else:
                    st.warning("Unable to analyze the video as no transcript was fetched.")
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

# Adjust textarea height with custom CSS
st.markdown(
    """
    <style>
    div.stTextArea textarea {
        height: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True
)