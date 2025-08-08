import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Kirmani's Store Reviews",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom mobile-first CSS
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
    }
    .title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        color: #2E4057;
        margin-bottom: 1.5rem;
    }
    .emoji-grid {
        display: flex;
        justify-content: space-evenly;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    .emoji-button {
        width: 80px;
        height: 80px;
        font-size: 2.5rem;
        border: none;
        border-radius: 50%;
        margin: 10px;
        background-color: #fff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .emoji-button:hover {
        transform: scale(1.1);
        cursor: pointer;
    }
    .thank-you {
        text-align: center;
        font-size: 1.5rem;
        color: #2E7D32;
        margin-top: 2rem;
    }
    .textarea-class textarea {
        font-size: 1.1rem;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Rating submission logic
def save_review(rating, comment=""):
    review_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'rating': rating,
        'comment': comment.strip()
    }
    filename = "reviews.csv"
    df = pd.DataFrame([review_data])
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(filename, index=False)

# Initialize session state
if 'rating_selected' not in st.session_state:
    st.session_state.rating_selected = None
if 'review_submitted' not in st.session_state:
    st.session_state.review_submitted = False

# App title
st.markdown("""<div class='title'>🏪 Kirmani's Store Reviews</div>""", unsafe_allow_html=True)

# Main Screen: Emoji selection and immediate submission
if not st.session_state.review_submitted:
    if st.session_state.rating_selected is None:
        st.markdown('<div style="text-align:center;">Tap an emoji to rate your experience:</div>', unsafe_allow_html=True)
        emojis = ["😞", "😟", "😐", "😊", "😄"]
        ratings = [1, 2, 3, 4, 5]
        labels = ["Very Poor", "Poor", "Average", "Good", "Excellent"]

        st.markdown('<div class="emoji-grid">', unsafe_allow_html=True)
        for emoji, rating, label in zip(emojis, ratings, labels):
            if st.button(emoji, key=f"rating_{rating}", help=label):
                st.session_state.rating_selected = rating
                save_review(rating)
                st.session_state.review_submitted = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Thank you screen + Optional comment
else:
    st.markdown('<div class="thank-you">🙏 Thank you for your feedback!</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-top:10px;">Want to leave a comment? (Optional)</div>', unsafe_allow_html=True)
    comment = st.text_area("", placeholder="Write your comment here...", key="comment_input")
    if st.button("Submit Comment"):
        save_review(st.session_state.rating_selected, comment)
        st.success("Your comment has been submitted.")
    if st.button("Submit Another Review"):
        st.session_state.rating_selected = None
        st.session_state.review_submitted = False
        st.rerun()