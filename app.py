import streamlit as st
import requests
import io

# --- FUNCTION TO LOAD CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- HUGGING FACE API SETUP ---
try:
    HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
except FileNotFoundError:
    st.warning("Hugging Face API token not found in st.secrets. Please enter it below.", icon="🔑")
    HF_API_TOKEN = st.text_input("Enter your Hugging Face API Token:", type="password")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def query_image_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error from API: {response.status_code} - {response.text}")
        return None

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Dream Weaver AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LOAD OUR CREATIVE CSS ---
local_css("style.css")

# --- APP INTERFACE ---
st.title("📖 Dream Weaver AI Story Generator")

# Use columns for a more creative layout
col1, col2 = st.columns([1, 2]) # Input column is 1/3 of the width

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
                # --- STORY & IMAGE GENERATION ---
                generated_story = f"In a world of {genre}, a {story_idea} This story has a {tone} tone and is for {audience}."
                image_prompt = f"A {tone} {genre} digital art masterpiece of: {story_idea}"
                
                image_bytes = query_image_api({"inputs": image_prompt})

                # --- DISPLAY RESULTS in the second column ---
                with col2:
                    st.subheader("📜 Your Generated Story")
                    st.write(generated_story)

                    if image_bytes:
                        st.subheader("🎨 A Glimpse into Your World")
                        st.image(image_bytes, caption="AI-generated image from your imagination.", use_column_width=True)
                    else:
                        st.error("Could not conjure an image. The magic may have fizzled. Please try again.")

# A placeholder for the second column before generation
with col2:
    if "generated_story" not in st.session_state:
        st.info("Your story and image will appear here once generated...")
        # You could add a default image here if you like
        # st.image("placeholder.jpg", caption="Your imagination's canvas awaits...")



