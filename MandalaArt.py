import streamlit as st
# import openai  # Comment this out temporarily
import requests
from PIL import Image
import io
import base64
from datetime import datetime

# Test page to verify other imports work
st.set_page_config(
    page_title="Mandala Art Generator - Test",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Import Test")
st.write("If you see this page, the basic imports are working!")
st.write("Streamlit: ✅")
st.write("Requests: ✅")
st.write("PIL: ✅")
st.write("IO: ✅")
st.write("Base64: ✅")
st.write("Datetime: ✅")

# Test if we can import OpenAI
try:
    import openai
    st.write("OpenAI: ✅")
    st.success("All imports successful! You can now use the full app.")
except ImportError as e:
    st.write("OpenAI: ❌")
    st.error(f"OpenAI import failed: {str(e)}")
    st.info("This confirms the OpenAI package installation issue.")

st.markdown("---")
st.markdown("### Next Steps:")
st.markdown("1. If OpenAI import fails, try the alternative requirements.txt")
st.markdown("2. Check the Streamlit Cloud logs for detailed error messages")
st.markdown("3. Ensure requirements.txt is in the repository root")