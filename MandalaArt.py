import streamlit as st
import openai
import requests
from PIL import Image
import io
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E2E2E;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 2rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .generated-image {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_mandala_image(api_key, inspiration_word):
    """Generate mandala image using DALL-E 3 (OpenAI v0.28.1)"""
    try:
        # Set OpenAI API key
        openai.api_key = api_key
        
        # Create detailed prompt for mandala generation
        prompt = f"""Create a detailed black and white mandala inspired by the word '{inspiration_word}'. 
        The mandala should be:
        - Completely black and white (no colors)
        - Intricate and symmetrical
        - Featuring geometric patterns and designs
        - Inspired by the essence and meaning of '{inspiration_word}'
        - Suitable for meditation and relaxation
        - High contrast with clean lines
        - Circular mandala format
        - Artistic and beautiful"""
        
        # Generate image using DALL-E 3
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get image URL
        image_url = response['data'][0]['url']
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_response.content))
        
        return image, None
        
    except Exception as e:
        return None, str(e)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🎨 Mandala Art Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your inspiration into beautiful black and white mandala art</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'inspiration_word' not in st.session_state:
        st.session_state.inspiration_word = ""
    
    # API Key input
    st.markdown("### 🔑 OpenAI API Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        help="You can get your API key from https://platform.openai.com/api-keys"
    )
    
    if api_key:
        st.success("✅ API Key provided!")
    
    st.markdown("---")
    
    # Inspiration word input
    st.markdown("### 💭 Your Inspiration")
    inspiration_word = st.text_input(
        "Enter one word that inspires you:",
        placeholder="e.g., peace, love, nature, strength, harmony...",
        help="This word will inspire the design of your mandala"
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🎨 Generate Mandala", use_container_width=True)
    
    # Generate mandala
    if generate_button:
        if not api_key:
            st.error("❌ Please enter your OpenAI API key first!")
        elif not inspiration_word.strip():
            st.error("❌ Please enter an inspiration word!")
        elif len(inspiration_word.split()) > 1:
            st.warning("⚠️ Please enter only one word for inspiration!")
        else:
            with st.spinner(f"🎨 Creating your mandala inspired by '{inspiration_word}'..."):
                image, error = generate_mandala_image(api_key, inspiration_word.strip())
                
                if error:
                    st.error(f"❌ Error generating image: {error}")
                else:
                    st.session_state.generated_image = image
                    st.session_state.inspiration_word = inspiration_word.strip()
                    st.success(f"✅ Mandala created successfully inspired by '{inspiration_word}'!")
    
    # Display generated image
    if st.session_state.generated_image:
        st.markdown("---")
        st.markdown("### 🖼️ Your Generated Mandala")
        
        # Display image
        st.image(
            st.session_state.generated_image,
            caption=f"Mandala inspired by: {st.session_state.inspiration_word}",
            use_column_width=True
        )
        
        # Download button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mandala_{st.session_state.inspiration_word}_{timestamp}.png"
            
            # Convert image to bytes for download
            img_buffer = io.BytesIO()
            st.session_state.generated_image.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            st.download_button(
                label="⬇️ Download Mandala",
                data=img_bytes,
                file_name=filename,
                mime="image/png",
                use_container_width=True
            )
    
    # Instructions and tips
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Get your OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. **Enter your API key** in the field above
    3. **Enter one inspiring word** (e.g., peace, love, nature, strength)
    4. **Click Generate** to create your unique mandala
    5. **Download** your beautiful black and white mandala art
    """)
    
    st.markdown("### 💡 Tips for Better Results")
    st.markdown("""
    - Use **meaningful single words** like emotions, nature elements, or concepts
    - Try words like: *serenity, cosmos, growth, balance, wisdom, fire, ocean*
    - Each generation creates a unique interpretation of your word
    - The mandala will be optimized for relaxation and meditation
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        Made with ❤️ using Streamlit and DALL-E 3<br>
        Perfect for meditation, decoration, or personal inspiration
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()