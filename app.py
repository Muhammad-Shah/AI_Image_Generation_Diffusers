import streamlit as st
import io
from PIL import Image
import PIL
import requests
from dotenv import load_dotenv
import os
import numpy as np

dotenv_path = r'env'
load_dotenv(dotenv_path)

# Access environment variables
HF_API = os.getenv('HF_API')


def generate_image(prompt, style, color_palette, image_size, background):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_API}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    image_bytes = query({
        "inputs": f"{prompt}",
        "style": style,
        "color_palette": color_palette,
        "image_size": image_size,
        "background": background,
    })

    try:
        image = Image.open(io.BytesIO(image_bytes))
        return image
    except PIL.UnidentifiedImageError as e:
        st.error(f"Error: {e} 😞")
        return None


st.title('AI Image Generation App 🎨')
with st.expander('About the image 📚'):
    st.write('Given a text prompt, it will generate an image 📸')

st.subheader('Image Generation using Hugging Face Diffuser 🔥')
input_prompt = st.text_input(
    label='Enter your text input for image Generation 💬', placeholder='text goes here...'
)

style_options = ["Realistic", "Cartoonish", "Abstract"]
style = st.selectbox("Select image style 🎭", style_options)

color_palette_options = ["Bright and Bold", "Pastel", "Monochromatic"]
color_palette = st.selectbox("Select color palette 🎨", color_palette_options)

image_size_options = [256, 512, 1024]
color_palette = st.selectbox("Select color palette 🎨", image_size_options)
image_size = st.slider("Select image size 🔍", min_value=256, max_value=1024)

background_options = ["Solid Color", "Gradient", "Texture"]
background = st.selectbox("Select background style 🌈", background_options)

if input_prompt is not None:
    if st.button('Generate Image 🔮'):
        image = generate_image(prompt=input_prompt, style=style,
                               color_palette=color_palette, image_size=image_size, background=background)
        if image is not None:
            st.image(image)
            st.success("Image generated successfully! 🎉")
        else:
            st.error("Error generating image 😞")

        # Create a download button
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Image 💾",
            data=byte_im,
            file_name="generated_image.png",
            mime="image/png"
        )
