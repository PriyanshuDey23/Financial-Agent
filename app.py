import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.tavily import TavilyTools
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import tempfile
import os


# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Multimodal AI Agent 📈🎥💹")


# Initialize finance agent
@st.cache_resource
def initialize_finance_agent():
    return Agent(
        name="Finance AI Agent",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True),
               DuckDuckGo()],
        instructions=["Use DuckDuckGo for web searches.", "Provide financial data in tabular format.", "Always include sources for any information provided."],
        show_tool_calls=True,
        markdown=True,
    )


# Initialize YouTube video agent
@st.cache_resource
def initialize_youtube_agent():
    return Agent(
        name="YouTube Video Insights",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

# Initialize product ingredient analyzer agent
@st.cache_resource
def initialize_product_agent():
    SYSTEM_PROMPT = """
    You are an expert Food Product Analyst specialized in ingredient analysis and nutrition science. 
    Your role is to analyze product ingredients, provide health insights, and identify potential concerns by combining ingredient analysis with scientific research. 
    You utilize your nutritional knowledge and research works to provide evidence-based insights, making complex ingredient information accessible and actionable for users.
    Return your response in Markdown format. 
    """

    INSTRUCTIONS = """
    * Read ingredient list from product image 
    * Remember the user may not be educated about the product, break it down in simple words like explaining to a 10-year-old
    * Identify artificial additives and preservatives
    * Check against major dietary restrictions (vegan, halal, kosher). Include this in response. 
    * Rate nutritional value on a scale of 1-5
    * Highlight key health implications or concerns
    * Suggest healthier alternatives if needed
    * Provide brief evidence-based recommendations
    * Use the Search tool for getting context
    """

    return Agent(
        name="Product Ingredient Agent",
        model=Gemini(id="gemini-2.0-flash"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=TAVILY_API_KEY)],
        markdown=True,
    )

# Instantiate the agents
finance_agent = initialize_finance_agent()
youtube_agent = initialize_youtube_agent()
product_agent = initialize_product_agent()


# Function to resize image for display
def resize_image_for_display(image_file):
    MAX_IMAGE_WIDTH = 300
    img = Image.open(image_file)
    aspect_ratio = img.height / img.width
    new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
    img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Function to analyze the image
def analyze_image(image_path):
    with st.spinner('Analyzing image...'):
        response = product_agent.run(
            "Analyze the given image",
            images=[image_path],
        )
        st.markdown(response.content)

# Save uploaded file temporarily
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
        f.write(uploaded_file.getbuffer())
        return f.name

# Option selection
option = st.sidebar.radio("Choose an Analysis", ["Finance AI Agent",  "YouTube Video Insights", "Product Ingredient Analysis"])

# Finance Data Analysis
if option == "Finance AI Agent":
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

# Product Ingredient Analysis
elif option == "Product Ingredient Analysis":
    st.subheader("Product Ingredient Analysis 🔍")
    uploaded_file = st.file_uploader(
        "Upload product image", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of the product's ingredient list"
    )

    if uploaded_file:
        resized_image = resize_image_for_display(uploaded_file)
        st.image(resized_image, caption="Uploaded Image", width=300)

        if st.button("🔍 Analyze Uploaded Image"):
            temp_path = save_uploaded_file(uploaded_file)
            analyze_image(temp_path)
            os.unlink(temp_path)

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
