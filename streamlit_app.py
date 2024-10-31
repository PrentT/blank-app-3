import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# Streamlit App
st.title("Chat with GPT-4o")

# API Key input from user
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# System context input from user
system_context = st.text_area("Enter system context (optional):")

# Text input from user
text_input = st.text_area("Enter your text prompt:")

# Image input from user
uploaded_images = st.file_uploader("Upload images (optional):", type=["png", "jpg", "jpeg", "webp", "gif"], accept_multiple_files=True)

# Button to submit the request
if st.button("Generate Response"):
    if api_key and text_input:
        # Prepare the message content
        messages = []
        if system_context:
            messages.append({"role": "system", "content": system_context})
        messages.append({"role": "user", "content": text_input})
        
        # If images are uploaded, encode and add them
        if uploaded_images:
            for uploaded_image in uploaded_images:
                # Reduce image quality and size further
                image = Image.open(uploaded_image)
                image = image.resize((512, 512))  # Resize image to 512x512 pixels
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG", quality=30)  # Reduce quality to 30%
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                messages.append({
                    "role": "user",
                    "content": f"data:image/jpeg;base64,{base64_image}"
                })
        
        # Prepare the headers and payload for the API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 300
        }
        
        # Make the API call
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                response_data = response.json()
                st.success("Generated Response:")
                st.write(response_data["choices"][0]["message"]["content"])
            else:
                st.error(f"An error occurred: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    elif not api_key:
        st.warning("Please provide your OpenAI API key.")
    else:
        st.warning("Please provide a text prompt to generate a response.")
