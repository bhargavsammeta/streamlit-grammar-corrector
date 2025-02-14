import streamlit as st
import google.generativeai as genai

# Set up Google Gemini API Key
API_KEY = "AIzaSyB5oRfOPtnk5lmV3r0Z6StReam8GoQ-lw8"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# Initialize session state variables to store multiple iterations
if "corrected_text" not in st.session_state:
    st.session_state.corrected_text = ""

if "refined_texts" not in st.session_state:
    st.session_state.refined_texts = []  # Stores multiple iterations

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Function to correct grammar using Google Gemini
@st.cache_data
def correct_grammar(text):
    """Uses Google Gemini API to correct grammar and improve clarity."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Correct the grammar and improve clarity: {text}")
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Function to refine text iteratively
@st.cache_data
def refine_text(previous_text, user_feedback):
    """Refines the text iteratively based on user feedback."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        The user wants to refine the following sentence iteratively:
        "{previous_text}"

        User's refinement request: "{user_feedback}"
        
        Apply the requested refinement and return the improved version.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("📖 AI Grammar Corrector with Iterative Refinements")
st.write("Enter any English sentence, and AI will correct its grammar and improve clarity.")

# User Input for original sentence
user_input = st.text_area("Enter your sentence:", value=st.session_state.corrected_text or "")

# Button to process grammar correction
if st.button("Correct Grammar"):
    if user_input.strip():
        with st.spinner("Correcting grammar..."):
            st.session_state.corrected_text = correct_grammar(user_input)
            st.session_state.refined_texts = [st.session_state.corrected_text]  # Start iteration tracking
            st.session_state.button_clicked = True  # Track that button was clicked

# Display initial correction
if st.session_state.button_clicked and st.session_state.corrected_text.strip():
    st.subheader("✅ Corrected Version:")
    st.text_area("Edit the corrected text:", st.session_state.corrected_text, height=150, key="corrected_text_display")

# Option for user to tweak the output iteratively
if st.session_state.button_clicked and st.session_state.corrected_text.strip():
    st.subheader("🔄 Refine Your Output Iteratively")
    user_feedback = st.text_area("Describe how you want to refine the text (e.g., make it more formal, simplify, etc.)")

    if st.button("Apply Refinement"):
        if user_feedback.strip():
            with st.spinner("Refining text..."):
                refined_text = refine_text(st.session_state.refined_texts[-1], user_feedback)
                st.session_state.refined_texts.append(refined_text)  # Store iteration history

# Display all iterations
if len(st.session_state.refined_texts) > 1:
    st.subheader("🔍 Refinement History")
    for i, text in enumerate(st.session_state.refined_texts):
        st.text_area(f"Iteration {i+1}:", text, height=100, key=f"iteration_{i}")

# Optional: Download the final refined text
if len(st.session_state.refined_texts) > 0:
    st.download_button("Download Final Corrected Text", st.session_state.refined_texts[-1], file_name="final_corrected_text.txt")
