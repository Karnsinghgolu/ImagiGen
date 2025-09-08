import streamlit as st
import requests
from gtts import gTTS  # NEW: Import the gTTS library
import base64          # NEW: To encode the audio for autoplay

# --- TEXT-TO-SPEECH FUNCTION ---
def text_to_speech_autoplay(text):
    """Generates an audio file from text and creates an autoplaying HTML audio player."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        # Save the audio to a temporary in-memory file
        audio_fp = "welcome_audio.mp3"
        tts.save(audio_fp)
        
        # Encode the audio file for embedding in HTML
        with open(audio_fp, "rb") as f:
            audio_bytes = f.read()
        
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Create an HTML5 audio player that autoplays
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            """
        return audio_html
    except Exception as e:
        st.error(f"Failed to generate welcome audio: {e}")
        return ""


# --- FUNCTION TO LOAD EXTERNAL CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found. Make sure it's in the same folder as the app.")

# --- HUGGING FACE API SETUP ---
import streamlit as st # Make sure streamlit is imported

# Get the token from Streamlit's secrets manager
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

# --- API Endpoints ---
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
TEXT_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


# --- API Query Functions ---
def query_image_api(prompt):
    full_prompt = f"photorealistic, highly detailed, 8k, cinematic lighting, {prompt}"
    payload = {"inputs": full_prompt}
    response = requests.post(IMAGE_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error from Image API: {response.status_code} - {response.text}")
        return None

def query_text_api(prompt):
    story_prompt = f"Write a very short, evocative story (about 50-70 words) inspired by this scene: '{prompt}'."
    payload = {"inputs": story_prompt, "parameters": {"max_new_tokens": 100}}
    response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        result = response.json()
        if result and isinstance(result, list) and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text']
            return generated_text.replace(story_prompt, "").strip()
        return "Failed to parse generated story."
    else:
        st.error(f"Error from Text API: {response.status_code} - {response.text}")
        return "Failed to generate story."

# --- PAGE CONFIGURATION & UI ---
st.set_page_config(page_title="Virtual World Creator", page_icon="🔊", layout="wide")

# LOAD THE EXTERNAL CSS FILE
local_css("style.css")

# --- GENERATE AND PLAY WELCOME AUDIO ---
welcome_text = "Welcome to the Virtual World"
audio_player_html = text_to_speech_autoplay(welcome_text)
st.markdown(audio_player_html, unsafe_allow_html=True)

# WELCOME TITLE
st.title("✨ Welcome to the Virtual World ✨")
st.markdown("<p style='text-align: center; color: #b0b0b0;'>Describe any scene, and the AI will create an image and a short story.</p>", unsafe_allow_html=True)


# --- INITIALIZE SESSION STATE ---
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'generated_story_text' not in st.session_state:
    st.session_state.generated_story_text = None

# --- LAYOUT AND FORM ---
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Describe Your Vision")
    with st.form("generation_form"):
        prompt_idea = st.text_area(
            "Enter your scene description:",
            "A hidden library inside an ancient, giant tree.",
            height=150
        )
        submitted = st.form_submit_button("Create My World")

# --- GENERATION LOGIC ---
if submitted:
    if not HF_API_TOKEN:
        st.warning("Please enter your Hugging Face API Token in the sidebar to proceed.", icon="⚠️")
    else:
        with st.spinner("The AI is building your world..."):
            image_bytes = query_image_api(prompt_idea)
            st.session_state.generated_image = image_bytes
            
            if image_bytes:
                story_text = query_text_api(prompt_idea)
                st.session_state.generated_story_text = story_text
            else:
                st.session_state.generated_story_text = "Story generation skipped due to image error."

# --- OUTPUT DISPLAY ---
with col2:
    if st.session_state.generated_image:
        st.subheader("Your Generated World")
        st.image(st.session_state.generated_image, caption="A glimpse into your imagination.", use_column_width=True)
        
        if st.session_state.generated_story_text:
            st.subheader("A Tale from this World")
            st.markdown(f'<div class="handwritten-story">{st.session_state.generated_story_text}</div>', unsafe_allow_html=True)
    else:
        st.info("Your world will appear here once you describe it...")
