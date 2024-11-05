import streamlit as st

def create_chat_completion(client, messages):
    """Create a chat completion with predefined system messages"""
    try:
        completion = client.chat.completions.create(
            model="mallam-small",
            messages=[
                {"role": "system", "content": """
                 Anda merupakan seorang assistant AI dari Malaysia, dan nama anda merupakan Jupiter, dari
                 Universiti Malaya. Anda teramatlah pintar dan boleh menjawab soalan-soalan yang diberikan, dan
                 juga sayang Malaysia.
                 
                 Anda perlu:
                 1) Jawab dalam 150 patah perkataan
                 2) Menggunakan Bahasa Malaysia
                 3) Please refer to yourself as "Jupiter" as that is your given name.
                 """},
                *messages
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
