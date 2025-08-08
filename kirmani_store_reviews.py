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

# Image URLs or local paths for rating faces
rating_faces = [
    {"src": "https://i.imgur.com/Z9V4ZHF.png", "label": "Very Poor", "rating": 1},
    {"src": "https://i.imgur.com/72nQa9r.png", "label": "Poor", "rating": 2},
    {"src": "https://i.imgur.com/NFbBoFZ.png", "label": "Average", "rating": 3},
    {"src": "https://i.imgur.com/J4x6Wnt.png", "label": "Good", "rating": 4},
    {"src": "https://i.imgur.com/8GDzLro.png", "label": "Excellent", "rating": 5},
]

# Custom CSS
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 2rem;
        color: #2E4057;
    }
    .face-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .face-button {
        background: none;
        border: none;
        outline: none;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .face-button:hover {
        transform: scale(1.05);
    }
    .face-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid transparent;
    }
    .thank-you {
        text-align: center;
        font-size: 1.4rem;
        color: #2E7D32;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Save review to CSV
def save_review(rating, comment=""):
    review_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rating": rating,
        "comment": comment.strip()
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

# Title
st.markdown("<div class='title'>🏪 Kirmani's Store Reviews</div>", unsafe_allow_html=True)

# Main Rating Page
if not st.session_state.review_submitted:
    st.markdown("<div style='text-align:center;'>Tap a face to rate your experience:</div>", unsafe_allow_html=True)
    st.markdown('<div class="face-container">', unsafe_allow_html=True)

    cols = st.columns(len(rating_faces))
    for i, face in enumerate(rating_faces):
        with cols[i]:
            if st.button(" ", key=f"rating_{face['rating']}"):
                st.session_state.rating_selected = face['rating']
                save_review(face['rating'])
                st.session_state.review_submitted = True
                st.rerun()
            st.image(face['src'], width=80, caption=face['label'])

    st.markdown('</div>', unsafe_allow_html=True)

# Thank You + Comment Page
else:
    st.markdown("<div class='thank-you'>🙏 Thank you for your feedback!</div>", unsafe_allow_html=True)
    comment = st.text_area("Optional Comment", placeholder="Tell us more if you like...")
    if st.button("Submit Comment"):
        save_review(st.session_state.rating_selected, comment)
        st.success("Your comment was submitted.")
    if st.button("Submit Another Review"):
        st.session_state.rating_selected = None
        st.session_state.review_submitted = False
        st.rerun()
