import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration for mobile
st.set_page_config(
    page_title="Kirmani's Store Reviews",
    page_icon="🏪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    .main > div {
        padding: 1rem 0.5rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 3rem;
        border: none;
        border-radius: 50%;
        margin: 5px;
        cursor: pointer;
    }
    
    .emoji-button {
        width: 100%;
        height: 80px;
        font-size: 3rem;
        border: 3px solid transparent;
        border-radius: 50%;
        margin: 10px 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #2E4057;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: #666;
    }
    
    .rating-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .thank-you {
        text-align: center;
        font-size: 1.5rem;
        color: #4CAF50;
        margin: 2rem 0;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 1.1rem;
        min-height: 100px;
    }
    
    @media (max-width: 768px) {
        .title {
            font-size: 2rem;
        }
        .emoji-button {
            width: 60px;
            height: 60px;
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rating_selected' not in st.session_state:
    st.session_state.rating_selected = None
if 'review_submitted' not in st.session_state:
    st.session_state.review_submitted = False
if 'show_thank_you' not in st.session_state:
    st.session_state.show_thank_you = False

def save_review(rating, comment=""):
    """Save review to CSV file"""
    review_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'rating': rating,
        'comment': comment.strip()
    }
    
    filename = "reviews.csv"
    
    # Create DataFrame
    df = pd.DataFrame([review_data])
    
    # Append to existing file or create new one
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(filename, index=False)

def reset_form():
    """Reset the form after submission"""
    st.session_state.rating_selected = None
    st.session_state.review_submitted = False
    st.session_state.show_thank_you = False

# Main app
def main():
    # Title
    st.markdown('<div class="title">🏪 Kirmani\'s Store Reviews</div>', unsafe_allow_html=True)
    
    if not st.session_state.show_thank_you:
        st.markdown('<div class="subtitle">How was your experience with us today?</div>', unsafe_allow_html=True)
        
        # Rating selection with emojis
        st.markdown("### Rate Your Experience:")
        
        # Create columns for emoji buttons
        cols = st.columns(5)
        
        emojis = ["😞", "😟", "😐", "😊", "😄"]
        ratings = [1, 2, 3, 4, 5]
        colors = ["#E53E3E", "#FF8C00", "#FFD700", "#9AE6B4", "#68D391"]
        labels = ["Very Poor", "Poor", "Average", "Good", "Excellent"]
        
        for i, (col, emoji, rating, color, label) in enumerate(zip(cols, emojis, ratings, colors, labels)):
            with col:
                if st.button(emoji, key=f"rating_{rating}", help=label):
                    st.session_state.rating_selected = rating
        
        # Show selected rating
        if st.session_state.rating_selected:
            selected_idx = st.session_state.rating_selected - 1
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0; font-size: 1.2rem;">
                You selected: {emojis[selected_idx]} {labels[selected_idx]}
            </div>
            """, unsafe_allow_html=True)
        
        # Optional comment section
        st.markdown("### Additional Comments (Optional):")
        comment = st.text_area("Tell us more about your experience...", height=100, placeholder="Your feedback helps us improve!")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Review", type="primary", disabled=st.session_state.rating_selected is None):
                if st.session_state.rating_selected:
                    save_review(st.session_state.rating_selected, comment)
                    st.session_state.show_thank_you = True
                    st.rerun()
    
    else:
        # Thank you message
        st.markdown("""
        <div class="thank-you">
            <h2>🙏 Thank You!</h2>
            <p>Your feedback has been recorded.</p>
            <p>We appreciate you taking the time to share your experience!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # New review button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Another Review", type="primary"):
                reset_form()
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #888; font-size: 0.9rem;">Powered by Streamlit</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()