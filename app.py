import streamlit as st
from openai import OpenAI

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
</style>
""", unsafe_allow_html=True)

# Sidebar for API key input
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter your Mesolitica API key", type="password")
    if not api_key:
        st.warning("Please enter your API key. If you don't have one, get it from [Mesolitica Playground](https://playground.mesolitica.com/)")
        st.stop()

# Initialize the OpenAI client with Mesolitica's base URL
client = OpenAI(
    base_url="https://llm-router.nous.mesolitica.com",
    api_key=api_key
)

# Set page title
st.title("🌙 Mallam Chatbot 🤖")
st.markdown("Welcome to Mallam Chatbot! Ask me anything and I'll help you out.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
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