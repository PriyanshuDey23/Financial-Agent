
# Phidata Multimodal AI Agent

## Overview

Phidata Multimodal AI Agent is a sophisticated Streamlit application powered by Gemini 2.0 Flash Exp. It offers three distinct functionalities:

1. **Financial Data Analysis**: Allows users to get insights into stock prices, company fundamentals, and financial news.
2. **Video Summarization**: Summarizes uploaded video content and answers user queries based on the video context.
3. **YouTube Video Insights**: Extracts and analyzes transcripts from YouTube videos, providing detailed insights and answers to user queries.

This app leverages advanced AI models and integrates multimodal inputs, providing a seamless experience across different use cases.

---

## Features

- **Financial Data Analysis**:
  - Get real-time stock prices and company news.
  - Analyze company fundamentals, including financial ratios and performance metrics.
  - Query-based financial insights with web search integration.

- **Video Summarization**:
  - Upload video files (MP4, MOV, AVI formats).
  - AI summarization and detailed analysis based on the video's content.
  - Analyze video content and gather additional insights via AI.

- **YouTube Video Insights**:
  - Provide a YouTube video link for transcript extraction and analysis.
  - Use the video's transcript to answer queries and derive insights from the content.

---

## Requirements

To run this app, you need to set up a few dependencies. Follow the steps below to get started.

### 1. Install the Required Libraries

You can install the necessary dependencies by running the following command:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should include the following dependencies:

```txt
streamlit
phi
google-generativeai
youtube-transcript-api
yfinance
python-dotenv
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory of your project and add your API keys. The `.env` file should look like this:

```env
GOOGLE_API_KEY=your_google_api_key
```

You can obtain a Google API key from [Google Cloud Console](https://aistudio.google.com/apikey).

### 3. Running the App

Once you have the dependencies installed and the `.env` file set up, you can run the app locally using the following command:

```bash
streamlit run app.py
```

This will start a local server and open the app in your web browser. You can now interact with the multimodal AI agent.

---

## Usage

### Financial Data Analysis

1. Select "Financial Data" from the sidebar.
2. Enter your query about stock prices, company fundamentals, or financial news.
3. Click the **🔍 Get Answer** button to receive the analysis from the AI agent.

### Video Summarization

1. Select "Video Summarizer" from the sidebar.
2. Upload your video file (MP4, MOV, or AVI format).
3. Enter your query regarding the video content and click the **🔍 Analyze Video** button for the AI to analyze and summarize the content.

### YouTube Video Insights

1. Select "YouTube Video Insights" from the sidebar.
2. Provide a valid YouTube video link.
3. Enter your query regarding the video and click the **🔍 Analyze Video** button to get the analysis from the transcript of the video.

---

## Directory Structure

```
/Phidata-Multimodal-AI-Agent
├── app.py                 # Main Streamlit application script
├── requirements.txt       # List of required Python packages
├── .env                   # Environment variables (API keys)
├── /assets                # Folder for images, videos, and other media (optional)
└── README.md              # This readme file
```

---

## Development

Feel free to fork this project and contribute. To set up a development environment:

1. Clone the repository:

    ```bash
    git clone https://github.com/PriyanshuDey23/Phidata-Multimodal-AI-Agent.git
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - **Windows**:

        ```bash
        venv\Scriptsctivate
        ```

    - **Mac/Linux**:

        ```bash
        source venv/bin/activate
        ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:

    ```bash
    streamlit run app.py
    ```

---

## License

This project is licensed under the MIT License.

