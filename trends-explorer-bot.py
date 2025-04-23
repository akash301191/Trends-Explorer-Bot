import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_content_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Content Basics
    with col1:
        st.subheader("📌 Content Basics")
        topic = st.text_input("What is your topic or niche?*", placeholder="e.g., skincare, fitness, finance")
        platform = st.selectbox(
            "Which platform are you targeting?*",
            ["Instagram", "YouTube", "TikTok", "Pinterest", "LinkedIn", "Other"]
        )
        content_type = st.selectbox(
            "What type of content are you planning to create?*",
            ["Reel / Short", "Carousel Post", "YouTube Video", "Infographic", "Live Stream", "Other"]
        )

    # Column 2: Audience & Style
    with col2:
        st.subheader("🎯 Audience & Style")
        audience = st.text_input("Who is your target audience?", placeholder="e.g., Gen Z students, working moms, tech enthusiasts")
        content_goal = st.selectbox(
            "What is the main goal of this content?*",
            ["Gain followers", "Boost engagement", "Educate", "Promote product", "Raise awareness", "Other"]
        )
        tone_style = st.multiselect(
            "Preferred content tone/style (select 1–3)*",
            ["Funny", "Inspirational", "Informative", "Trendy", "Minimal / Aesthetic", "Conversational"]
        )

    # Column 3: Posting & Preferences
    with col3:
        st.subheader("🗓️ Posting Habits & Preferences")
        post_frequency = st.selectbox(
            "How often do you post in this niche?",
            ["Daily", "Several times a week", "Weekly", "Occasionally"]
        )
        trend_timing = st.selectbox(
            "What kind of trends are you looking for?",
            ["Currently viral", "Emerging", "Evergreen", "Mix of all"]
        )
        want_hashtags = st.radio("Would you like hashtag suggestions?", ["Yes", "No"], horizontal=True, index=1)
        hashtag_count = st.selectbox(
            "How many hashtags do you typically use?",
            ["< 5", "5–10", "10–15"]
        ) if want_hashtags == "Yes" else None

    # Summary (optional return format or input to build search)
    user_content_preferences = f"""
    **Topic/Niche:** {topic}
    **Platform:** {platform}
    **Content Type:** {content_type}
    **Target Audience:** {audience if audience else 'Not specified'}
    **Goal:** {content_goal}
    **Tone/Style:** {', '.join(tone_style) if tone_style else 'Not specified'}
    **Posting Frequency:** {post_frequency}
    **Trend Timing Preference:** {trend_timing}
    **Hashtag Suggestions:** {want_hashtags}
    {"- Hashtag Count: " + hashtag_count if hashtag_count else ""}
    """

    return user_content_preferences

def generate_trends_report(user_content_preferences: str) -> str:
    # Step 1: Run Trends Researcher Agent
    trends_researcher = Agent(
            name="Trends Researcher",
            role="Finds trending content ideas, hashtags, and creator inspiration based on the user’s niche, platform, and content goals.",
            model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
            description=dedent("""
                You are a trend discovery expert. Given a content creator's detailed preferences—including their niche, target platform, content type, audience, and tone—
                your job is to research what's currently trending in that space.
                You'll generate a focused, real-world search query, conduct a web search using SerpAPI, and extract 10 of the most relevant content ideas or trend summaries.
            """),
            instructions=[
                "Carefully analyze the user preferences to understand their topic, platform, audience, content type, tone, and posting frequency.",
                "Based on this, generate ONE highly specific and timely Google search query. Example: 'trending Instagram reel ideas for skincare niche targeting Gen Z April 2025'.",
                "Use `search_google` with this query via SerpAPI to fetch web results.",
                "From the results, extract and return the top 10 most relevant links.",
                "For each result, provide only the **title** of the page and the **direct URL** — no summaries, no bullet points, and no extra formatting.",
                "Make sure the links are relevant to trending content ideas, hashtags, formats, or creator strategies.",
                "Prioritize fresh results (past week or month), avoiding vague or outdated advice, unless 'evergreen' trends are requested by the user.",
                "Do not make up trends or URLs. Only return actual titles and links from the search results."
            ],
            tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
            add_datetime_to_instructions=True,
        )
    
    research_response = trends_researcher.run(user_content_preferences)
    research_results = research_response.content 

    # Step 2: Run Trends Reporter Agent 
    trends_reporter = Agent(
            name="Trends Reporter",
            role="Generates a comprehensive trend insights report based on the user's content preferences and real web results.",
            model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
            description=dedent("""
                You are a content strategist and trends analyst.
                Your job is to study user preferences (like niche, platform, content type, and goals) and go through a list of URLs related to trending ideas, hashtags, and creator strategies.
                Based on your analysis, you'll generate a trend insights report tailored to the user’s needs.
            """),
            instructions=[
                "Begin by understanding the user's preferences: niche/topic, platform, content type, tone, goal, and audience.",
                "Carefully review all the provided search result titles and URLs.",
                "Extract real, actionable insights from these sources. Focus on:",
                "- Specific content formats trending (e.g., challenges, tutorials, POVs)",
                "- Effective or emerging hashtags",
                "- Creator trends or strategies (e.g., hook styles, post timing, engagement tricks)",
                "- Platform-specific trends (e.g., trending YouTube Shorts topics or Instagram carousel formats)",
                "- Noteworthy references to top-performing posts or campaigns",
                "",
                "Your response must be based only on verifiable content from the links. Do not make up trends.",
                "Present the output in a clean, structured markdown format like this:",
                "",
                "### 🔥 Trending Content Formats",
                "- **Format 1**: Description and why it's effective",
                "- **Format 2**: Description and usage example",
                "",
                "### 🏷️ Hashtags Gaining Momentum",
                "- **#hashtag1** – Use case or context",
                "- **#hashtag2** – What niche it's popular in",
                "",
                "### 👩‍🎤 Creator Strategies That Work",
                "- **Tip 1**: Short hook in first 3 seconds",
                "- **Tip 2**: Posting around X time works better",
                "",
                "### 🌍 References",
                "- [Source 1 Title](https://example.com)",
                "- [Source 2 Title](https://example.com)",
                "",
                "Keep your report focused, practical, and easy to act upon.",
                "Avoid repeating source titles in the body of the insights — use the 'Reference Content' section for listing sources."
            ],
            add_datetime_to_instructions=True
        )

    reporter_input = f"""
    User's Content Preferences: 
    {user_content_preferences}

    Research Results: 
    {research_results}

    Use these details to generate a comprehensive content trends report
    """

    reporter_response = trends_reporter.run(reporter_input)
    trends_report = reporter_response.content 

    return trends_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Trends Explorer Bot", page_icon="📈", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"], div[data-testid="stTextArea"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📈 Trends Explorer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to **Trends Explorer Bot** — your smart assistant for discovering viral content ideas, trending hashtags, and creator inspiration across platforms.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_content_preferences = render_content_preferences()

    st.markdown("---")

    # Call to generate the report
    if st.button("🔍 Generate Trends Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Fetching trending content ideas for you..."):
                trends_report = generate_trends_report(user_content_preferences=user_content_preferences)
                st.session_state.trends_report = trends_report

    # Display the report if it exists
    if "trends_report" in st.session_state:
        st.markdown("## 📊 Content Trends Report", unsafe_allow_html=True)
        st.markdown(st.session_state.trends_report, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Trends Report",
            data=st.session_state.trends_report,
            file_name="trends_report.txt",
            mime="text/plain"
        )

if __name__ == "__main__": 
    main()
