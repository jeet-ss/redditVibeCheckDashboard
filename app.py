import streamlit as st
import requests
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

st.title("The Subreddit Vibe Check DashBoard 📊")
st.write("Analyze the sentiment of the top 50 'Hot' posts without an API key!")

# Input control
# Create a list of default options for the user
subreddit_options = [
    "python",
    "ResinArt",
    "technology",
    "worldnews",
    "Other (Type your own...)"
]

# Display the dropdown menu
selected_sub = st.selectbox("Choose a Subreddit", subreddit_options)

# If they choose "Other", show a text box so they can type anything
if selected_sub == "Other (Type your own...)":
    sub_name = st.text_input("Enter custom subreddit name:", value="news")
else:
    # Otherwise, use the one they selected from the dropdown
    sub_name = selected_sub
# sub_name = st.text_input("Subreddit name", value="python")

if st.button("Check Vibe"):
    
    clean_sub_name = sub_name.strip().replace("r/", "")
    
    with st.spinner(f"Fetching posts from r/{clean_sub_name}..."):
        try:
            # Fetch Data
            url = f"https://www.reddit.com/r/{clean_sub_name}/hot.rss?limit=50"
            
            # web browser User-Agent 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                st.stop()
                
            # Parse XML Feed
            feed = feedparser.parse(response.content)
            posts = feed.entries
            if not posts:
                st.warning("No posts found or subreddit is private.")
                st.stop()

            # Process Data
            posts_data = []
            total_score = 0
            pos, neg, neu = 0, 0, 0
            
            for idx, post in enumerate(posts, start=1):
                # Store the post name in 'title' attribute
                title = post.title
                # Get scores
                score = analyzer.polarity_scores(title)['compound']
                total_score += score
                # Analyze based on scores
                if score > 0.05:
                    pos += 1
                elif score < -0.05:
                    neg += 1
                else:
                    neu += 1
                # Create data to show 
                posts_data.append({
                    "#": idx, 
                    "Score": round(score, 2), 
                    "Title": title
                })

            # Calculate Summary Metrics
            avg_score = total_score / len(posts_data)
            # Good, Neutral, Bad
            if avg_score > 0.05:
                vibe = "Positive 😊"
            elif avg_score < -0.05:
                vibe = "Negative 😠"
            else:
                vibe = "Neutral 😐"
            
            # Render the Results
            st.header(f"Overall Vibe: {vibe}")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Average Score", round(avg_score, 2))
            col2.metric("Positive Posts", pos)
            col3.metric("Negative Posts", neg)
            col4.metric("Neutral Posts", neu)

            st.dataframe(posts_data, width="stretch", hide_index=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")