import streamlit as st
import requests
import io
import os

# --- CONFIG ---
HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # safer: set as environment variable
if not HF_API_TOKEN:
    HF_API_TOKEN = st.text_input("Enter your Hugging Face API Token:", type="password")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# --- HELPER FUNCTIONS ---
def local_css(file_name):
    """Load custom CSS"""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def generate_story(story_idea, genre, tone, audience):
    """Generate story text (simple placeholder – can connect to a text model too)"""
    return f"In a world of {genre}, {story_idea}. This story has a {tone} tone and is for {audience}."

def generate_image(prompt):
    """Call Hugging Face API for image generation"""
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error from Hugging Face API: {response.status_code} - {response.text}")
        return None

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dream Weaver AI", page_icon="📖", layout="wide")
local_css("style.css")

# --- APP INTERFACE ---
st.title("📖 Dream Weaver AI Story Generator")

col1, col2 = st.columns([1, 2])  # Left input, right output

with col1:
    st.subheader("✨ Craft Your Tale")
    story_idea = st.text_area("Enter your story idea:", "A lonely robot discovers a hidden garden on Mars.", height=150)
    genre = st.selectbox("Choose Genre:", ["Fantasy", "Sci-Fi", "Mystery", "Fairy Tale"])
    tone = st.selectbox("Choose Tone:", ["Whimsical", "Dark", "Epic", "Humorous"])
    audience = st.selectbox("Target Audience:", ["Kids", "Teens", "Adults"])

    if st.button("🔮 Weave My Story!"):
        if not HF_API_TOKEN:
            st.warning("Please enter your Hugging Face API Token to proceed.", icon="⚠️")
        else:
            with st.spinner("The AI is dreaming up your story..."):
                # Backend logic runs here
                generated_story = generate_story(story_idea, genre, tone, audience)
                image_prompt = f"A {tone} {genre} digital art masterpiece of: {story_idea}"
                image_bytes = generate_image(image_prompt)

                # Display output
                with col2:
                    st.subheader("📜 Your Generated Story")
                    st.write(generated_story)

                    if image_bytes:
                        st.subheader("🎨 A Glimpse into Your World")
                        st.image(image_bytes, caption="AI-generated image from your imagination.", use_column_width=True)
                    else:
                        st.error("Could not generate an image. Try again.")

# Default right column content before generation
with col2:
    if "generated_story" not in st.session_state:
        st.info("Your story and image will appear here once generated...")
