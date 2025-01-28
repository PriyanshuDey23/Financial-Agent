from phi.agent import Agent
from phi.model.google import Gemini
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from io import BytesIO
from phi.tools.tavily import TavilyTools
from tempfile import NamedTemporaryFile

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# System prompt for the agent
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

MAX_IMAGE_WIDTH = 300

# Function to resize the image for display
def resize_image_for_display(image_file):
    """Resize image for display purposes and return as bytes."""
    img = Image.open(image_file)
    aspect_ratio = img.height / img.width
    new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
    img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Agent
@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=TAVILY_API_KEY)],
        markdown=True,
    )

# Function to analyze the image
def analyze_image(image_path):
    agent = get_agent() # Call the agent
    with st.spinner('Analyzing image...'):
        response = agent.run(
            "Analyze the given image",
            images=[image_path],
        )
        st.markdown(response.content)

# Save uploaded file temporarily
def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return the file path."""
    with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
        f.write(uploaded_file.getbuffer())
        return f.name

# Main application
def main():
    st.title("🔍 Product Ingredient Analyzer")

    # Tab for uploading and analyzing images
    upload = st.tabs(["📤 Upload Image"])[0]

    with upload:
        uploaded_file = st.file_uploader(
            "Upload product image", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the product's ingredient list"
        )

        if uploaded_file:
            resized_image = resize_image_for_display(uploaded_file)
            st.image(resized_image, caption="Uploaded Image", width=MAX_IMAGE_WIDTH)

            if st.button("🔍 Analyze Uploaded Image", key="analyze_upload"):
                temp_path = save_uploaded_file(uploaded_file)
                analyze_image(temp_path)
                os.unlink(temp_path)

# Run the Streamlit application
if __name__ == "__main__":
    st.set_page_config(
        page_title="Product Ingredient Agent",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()