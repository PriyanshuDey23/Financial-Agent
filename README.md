# Multimodal AI Agent

A **Streamlit-based application** that integrates various functionalities including:
- Product ingredient analysis for health insights.
- Financial data analysis for stock prices and company fundamentals.
- Video insights analysis from uploaded videos.
- YouTube video analysis using transcripts.

This tool leverages **Gemini 2.0 Flash Exp** for intelligent analysis, combining AI agents with task-specific tools like Tavily, DuckDuckGo, and YFinance.

## Features

### 1. Product Ingredient Analysis
- Upload an image of a product's ingredient list.
- Analyze for:
  - Nutritional value (rated on a scale of 1-5).
  - Presence of artificial additives and preservatives.
  - Dietary restrictions (e.g., vegan, halal, kosher).
  - Health implications and concerns.
  - Evidence-based recommendations for healthier alternatives.

### 2. Financial Data Analysis
- Get insights on:
  - Stock prices.
  - Company fundamentals and financial news.
  - Analyst recommendations.
- Information is presented in a clear and concise tabular format.

### 3. Video Insights Analysis
- Upload video files (e.g., `.mp4`, `.mov`, `.avi`).
- Extract meaningful insights and contextual analysis.
- Supports supplementary web research for enhanced results.

### 4. YouTube Video Analysis
- Enter a YouTube video link.
- Fetch and analyze video transcripts for content and context.
- Address user queries based on video content.

## Requirements

- Python version: **>= 3.9**
- Supported OS: Windows, macOS, Linux

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PriyanshuDey23/Phidata-Multimodal-AI-Agent.git
   cd multimodal-ai-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Add your API keys:
     ```env
     GOOGLE_API_KEY=your_google_api_key
     TAVILY_API_KEY=your_tavily_api_key
     ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

### Navigating the Application
1. Select an option from the sidebar (e.g., Financial Data, Video Insights, etc.).
2. Follow the on-screen instructions to upload files, input links, or enter queries.
3. View results directly within the application.

## Key Technologies

- **Streamlit**: For building an interactive user interface.
- **Phi Agents**: Task-specific AI agents with Gemini 2.0.
- **YFinanceTools**: For real-time financial data.
- **DuckDuckGo API**: For web-based searches.
- **YouTube Transcript API**: To retrieve video transcripts.
- **Tavily Tools**: For ingredient list analysis.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

## Acknowledgments

- **Phi AI** for powerful multimodal AI capabilities.
- **Streamlit** for an easy-to-use application framework.
- **Contributors** for their dedication and effort.

---

For any issues or feature requests, please open an issue on [GitHub](https://github.com/your-repo/multimodal-ai-agent/issues).

