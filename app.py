import streamlit as st
from openai import OpenAI
import requests
import os
from audio_recorder_streamlit import audio_recorder

# Must be the first Streamlit command
st.set_page_config(page_title="Mallam Chatbot", page_icon="🌙", layout="wide")

# Add custom CSS for a more professional look
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
    }
    .speech-text-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def speech_to_text(audio_file_path):
    """Convert speech to text using Mesolitica API"""
    url = "https://api.mesolitica.com/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {st.session_state.api_key}"
    }
    
    data = {
        "model": "base",
        "response_format": "text",
        "timestamp_granularities": "segment",
        "enable_diarization": "false",
        "speaker_similarity": "0.5",
        "speaker_max_n": "5",
        "chunking_method": "naive",
        "vad_method": "silero",
        "minimum_silent_ms": "200",
        "minimum_trigger_vad_ms": "1500",
        "reject_segment_vad_ratio": "0.9",
        "stream": "false"
    }

    with open(audio_file_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error in transcription: {response.text}")
        return None

# Initialize api_key in session state if not present
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar for API key input
with st.sidebar:
    st.title("⚙️ Settings")
    sidebar_api_key = st.text_input("Enter your Mesolitica API key", type="password", key="sidebar_api_key")
    if st.button("Submit API Key"):
        st.session_state.api_key = sidebar_api_key

# Set page title
st.title("🌙 Mallam Chatbot 🤖")
st.markdown("Welcome to Mallam Chatbot! Ask me anything through text or voice.")

# Main page API key input if not provided
if not st.session_state.api_key:
    st.warning("Please enter your API key in the sidebar of this application. If you don't have one, get it from [Mesolitica Playground](https://playground.mesolitica.com/)")
    st.stop()

# Initialize the OpenAI client with Mesolitica's base URL
client = OpenAI(
    base_url="https://llm-router.nous.mesolitica.com",
    api_key=st.session_state.api_key
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice Input Section
st.markdown("### 🎙️ Voice Input")
with st.expander("Click to expand voice input"):
    st.markdown("Click the microphone button below to start recording your message")
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        # Save temporary audio file
        temp_audio = "temp_audio.mp3"
        with open(temp_audio, "wb") as f:
            f.write(audio_bytes)
        
        with st.spinner("Transcribing your speech..."):
            transcription = speech_to_text(temp_audio)
            if transcription:
                st.success("Transcription complete!")
                prompt = transcription
                
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    try:
                        completion = client.chat.completions.create(
                            model="mallam-small",
                            messages=[
                                {"role": "system", "content": "Anda merupakan seorang assistant AI, dan akan mendapat beberapa soalan daripada pengguna. Sila jawab soalan mereka dengan betul dan berfakta."},
                                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                            ]
                        )
                        response = completion.choices[0].message.content
                        message_placeholder.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                
        # Clean up temp file
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

# Text Input Section
if prompt := st.chat_input("Type your message or use voice input above"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            completion = client.chat.completions.create(
                model="mallam-small",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            response = completion.choices[0].message.content
            message_placeholder.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

# Add a footer
st.markdown("---")
st.markdown("Powered by [Mesolitica](https://mesolitica.com/)'s Mallam API, built with 💖 by [Faris Faiz](https://www.linkedin.com/in/muhammad-faris-ahmad-faiz-ab9b35212/)")
