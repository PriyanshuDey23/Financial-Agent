import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

import os

API_KEY=os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Finance AI Agent",
    page_icon="📈",
    layout="wide",
)

st.title("Finance AI Agent 📈💹")
st.header("Powered by Gemini 2.0 Flash Exp")

@st.cache_resource
def initialize_agents():
    # Initialize a combined agent with both tools
    return Agent(
        name="Combined Finance and Web Search AI Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),  # Use Gemini explicitly
        tools=[
            YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True),  # Finance-related tools
            DuckDuckGo(),                    # Web search tool
        ],
        instructions=[
            "Use DuckDuckGo for web searches.",
            "Provide financial data in tabular format.",
            "Always include sources for any information provided.",
        ],
        show_tool_calls=True,
        markdown=True,
    )




multimodal_Agent=initialize_agents()

def main():
    st.write(
        "This application combines multiple AI agents to analyze financial data and answer your questions."
    )

    question = st.text_area(
        "Enter your question",
        placeholder="Ask about stock prices, company fundamentals, or financial news.",
        help="Provide a specific financial query for more accurate insights.",
    )

    if st.button("🔍 Get Answer"):
        if not question.strip():
            st.warning("Please enter a valid question.")
        else:
            try:
                with st.spinner("Processing your question..."):
                    # Run the agent and get a response
                    response = multimodal_Agent.run(question)

                    # Access the response content as text (assuming it's in the 'content' field)
                    response_text = response.content if hasattr(response, 'content') else str(response)

                    # Display the result
                    st.subheader("Analysis Result")
                    st.markdown(response_text)
            except Exception as e:
                st.error(f"An error occurred while processing your question: {e}")



def clean_agent_response(response):
    """
    Clean the raw response from the agent to display user-friendly content.
    """
    try:
        # Remove metadata like `content=` and other debug information
        if "content=" in response:
            response = response.split("content=", 1)[-1]

        # Strip unnecessary characters and clean formatting
        response = response.strip().strip('"').replace("\\n", "\n").replace("\\t", "\t")

        return response
    except Exception as e:
        return f"Error cleaning response: {e}"


# Run the app
if __name__ == "__main__":
    main()

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
