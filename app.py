import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from pathlib import Path
import tempfile
import time
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Multimodal AI Agent 📈🎥💹")
st.header("Powered by Gemini 2.0 Flash Exp")

# Initialize finance agent
@st.cache_resource
def initialize_finance_agent():
    return Agent(
        name="Finance AI Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True),
               DuckDuckGo()],
        instructions=["Use DuckDuckGo for web searches.", "Provide financial data in tabular format.", "Always include sources for any information provided."],
        show_tool_calls=True,
        markdown=True,
    )

# Initialize video summarizer agent
@st.cache_resource
def initialize_video_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

# Initialize YouTube video agent
@st.cache_resource
def initialize_youtube_agent():
    return Agent(
        name="YouTube Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

# Instantiate the agents
finance_agent = initialize_finance_agent()
video_agent = initialize_video_agent()
youtube_agent = initialize_youtube_agent()

# Option selection
option = st.sidebar.radio("Choose an Analysis", ["Financial Data", "Video Insights", "YouTube Video Insights"])

# Finance Data Analysis
if option == "Financial Data":
    st.subheader("Finance AI Agent 📈")
    question = st.text_area(
        "Enter your question",
        placeholder="Ask about stock prices, company fundamentals, or financial news."
    )
    if st.button("🔍 Get Answer"):
        if not question.strip():
            st.warning("Please enter a valid question.")
        else:
            try:
                with st.spinner("Processing your question..."):
                    response = finance_agent.run(question)
                    response_text = response.content if hasattr(response, 'content') else str(response)
                    st.subheader("Analysis Result")
                    st.markdown(response_text)
            except Exception as e:
                st.error(f"An error occurred while processing your question: {e}")

# Video Summarizer
elif option == "Video Insights":
    st.subheader("Video Insights 🎥")
    video_file = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name
        st.video(video_path, format="video/mp4", start_time=0)
        user_query = st.text_area("What insights are you seeking from the video?")
        if st.button("🔍 Analyze Video"):
            if not user_query:
                st.warning("Please enter a question or insight to analyze the video.")
            else:
                try:
                    with st.spinner("Processing video and gathering insights..."):
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)
                        analysis_prompt = f"Analyze the uploaded video for content and context. Respond to the following query using video insights and supplementary web research: {user_query}"
                        response = video_agent.run(analysis_prompt, videos=[processed_video])
                    st.subheader("Analysis Result")
                    st.markdown(response.content)
                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
                finally:
                    Path(video_path).unlink(missing_ok=True)

# YouTube Video Insights
elif option == "YouTube Video Insights":
    st.subheader("YouTube Video AI Insights 🎥")
    youtube_link = st.text_input("Enter the YouTube Video Link:")
    if youtube_link:
        try:
            video_id = youtube_link.split("/")[-1] if "youtu.be" in youtube_link else youtube_link.split("v=")[1].split("&")[0]
            st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
            st.success(f"Video ID: {video_id}")
        except ValueError as e:
            st.error(str(e))
    
    user_query = st.text_area("What insights are you seeking from the video?")
    if st.button("🔍 Analyze Video"):
        if not youtube_link:
            st.warning("Please provide a valid YouTube link.")
        elif not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript_text = " ".join([item["text"] for item in transcript])
                    analysis_prompt = f"Analyze the following YouTube video transcript: {transcript_text} and answer the user query: {user_query}"
                    response = youtube_agent.run(analysis_prompt)
                    st.subheader("Analysis Result")
                    st.markdown(response.content)
            except TranscriptsDisabled:
                st.error("Subtitles are disabled for this video. Unable to fetch the transcript.")
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

# Custom CSS for text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
