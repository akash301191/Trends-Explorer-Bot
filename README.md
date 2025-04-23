# Trends Explorer Bot

Trends Explorer Bot is a smart Streamlit application that helps content creators discover trending content ideas, viral formats, and high-performing hashtags tailored to their niche, platform, and audience. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot performs real-time web searches to generate a well-structured, actionable trends report just for you.

## Folder Structure

```
Trends-Explorer-Bot/
├── trends-explorer-bot.py
├── README.md
└── requirements.txt
```

- **trends-explorer-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Content Strategy Input**  
  Provide details about your content topic, target platform, audience, preferred tone, and posting habits.

- **Real-Time Trend Research**  
  The Trends Researcher agent creates a focused Google search query based on your inputs and fetches relevant trend resources from the web using SerpAPI.

- **AI-Powered Trend Report**  
  The Trends Reporter agent analyzes the results and generates a structured report with trending content formats, hashtag suggestions, and proven creator strategies.

- **Structured Markdown Output**  
  Your trends report is delivered in a clean, skimmable format with proper section headers and bullet points.

- **Download Option**  
  Download the trend insights as a `.txt` file for future planning or sharing with your team.

- **Clean Streamlit UI**  
  Built with Streamlit for an intuitive, fast, and distraction-free creator experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Trends-Explorer-Bot.git
   cd Trends-Explorer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run trends-explorer-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys in the sidebar.
   - Fill out your content preferences and strategy.
   - Click **🔍 Generate Trends Report**.
   - View and download your personalized AI-generated trends report.

3. **Download Option**  
   Use the **📥 Download Trends Report** button to save your insights as a `.txt` file.

## Code Overview

- **`render_content_preferences()`**: Captures the user's content strategy inputs including niche, platform, tone, goals, and hashtags.
- **`render_sidebar()`**: Stores and manages OpenAI and SerpAPI keys in Streamlit session state.
- **`generate_trends_report()`**:  
  - Uses the `Trends Researcher` agent to search the web for relevant insights using SerpAPI.  
  - Sends search results to the `Trends Reporter` agent to compile a structured Markdown report.
- **`main()`**: Handles UI layout, collects inputs, manages user interaction, and displays final results.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your changes are clean, well-documented, and aligned with the app’s purpose.