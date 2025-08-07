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

# Custom CSS for mobile-friendly design with HUGE buttons
st.markdown("""
<style>
    .main > div {
        padding: 1rem 0.5rem;
    }
    
    .stButton > button {
        width: 100% !important;
        height: 140px !important;
        font-size: 4.5rem !important;
        border: 3px solid #ddd !important;
        border-radius: 20px !important;
        margin: 15px 0 !important;
        cursor: pointer !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
        border-color: #4CAF50 !important;
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
        font-size: 1.3rem;
        margin-bottom: 2rem;
        color: #666;
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
        .subtitle {
            font-size: 1.1rem;
        }
        .stButton > button {
            height: 120px !important;
            font-size: 3.5rem !important;
            margin: 10px 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_thank_you' not in st.session_state:
    st.session_state.show_thank_you = False
if 'show_comment_option' not in st.session_state:
    st.session_state.show_comment_option = False
if 'current_rating' not in st.session_state:
    st.session_state.current_rating = None

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
    st.session_state.show_thank_you = False
    st.session_state.show_comment_option = False
    st.session_state.current_rating = None

# Main app
def main():
    # Title
    st.markdown('<div class="title">🏪 Kirmani\'s Store Reviews</div>', unsafe_allow_html=True)
    
    emojis = ["😞", "😟", "😐", "😊", "😄"]
    labels = ["Very Poor", "Poor", "Average", "Good", "Excellent"]
    
    # Main rating screen - NO comment section here
    if not st.session_state.show_thank_you and not st.session_state.show_comment_option:
        st.markdown('<div class="subtitle">Tap to rate your experience with us today!</div>', unsafe_allow_html=True)
        
        # BIG emoji buttons - each submits immediately
        # Order: Best to worst for better UX
        if st.button("😄 Excellent", key="rating_5"):
            save_review(5)
            st.session_state.current_rating = 5
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😊 Good", key="rating_4"):
            save_review(4)
            st.session_state.current_rating = 4
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😐 Average", key="rating_3"):
            save_review(3)
            st.session_state.current_rating = 3
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😟 Poor", key="rating_2"):
            save_review(2)
            st.session_state.current_rating = 2
            st.session_state.show_thank_you = True
            st.rerun()
            
        if st.button("😞 Very Poor", key="rating_1"):
            save_review(1)
            st.session_state.current_rating = 1
            st.session_state.show_thank_you = True
            st.rerun()
    
    # Comment page (optional)
    elif st.session_state.show_comment_option:
        st.markdown('<div class="subtitle">Want to tell us more?</div>', unsafe_allow_html=True)
        
        # Show their rating
        if st.session_state.current_rating:
            selected_idx = st.session_state.current_rating - 1
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0; font-size: 1.8rem;">
                Your rating: {emojis[selected_idx]} {labels[selected_idx]}
            </div>
            """, unsafe_allow_html=True)
        
        # Comment section
        st.markdown("### Tell us more:")
        comment = st.text_area("What made your experience special?", height=120, 
                              placeholder="Your detailed feedback helps us improve!")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏭️ Skip", type="secondary"):
                reset_form()
                st.rerun()
        with col2:
            if st.button("✅ Submit Comment", type="primary"):
                if comment.strip():
                    # Update the existing review with the comment
                    filename = "reviews.csv"
                    if os.path.exists(filename):
                        df = pd.read_csv(filename)
                        # Update the last row with the comment
                        if len(df) > 0:
                            df.iloc[-1, df.columns.get_loc('comment')] = comment.strip()
                            df.to_csv(filename, index=False)
                reset_form()
                st.rerun()
    
    # Thank you screen
    else:
        selected_idx = (st.session_state.current_rating - 1) if st.session_state.current_rating else 0
        st.markdown(f"""
        <div class="thank-you">
            <h1>🙏 Thank You!</h1>
            <h2>You rated us: {emojis[selected_idx]} {labels[selected_idx]}</h2>
            <p>Your feedback helps us serve you better!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Add Comment", type="secondary"):
                st.session_state.show_comment_option = True
                st.session_state.show_thank_you = False
                st.rerun()
        
        with col2:
            if st.button("✅ All Done", type="primary"):
                reset_form()
                st.rerun()

if __name__ == "__main__":
    main()