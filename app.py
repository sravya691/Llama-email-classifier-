import streamlit as st
import json

from llama_client import classify_email
from prompt import SYSTEM_PROMPT
from highlight import highlight_text

import re

def extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return None

# helper for handling eml
from email import policy
from email.parser import BytesParser



def extract_email_body(uploaded_file):
    msg = BytesParser(policy=policy.default).parse(uploaded_file)

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_content()
    else:
        return msg.get_content()

    return ""


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Email Classifier",
    layout="wide"
)

st.title("Email Classification")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("Settings")

model_name = st.sidebar.selectbox(
    "Language Model",
    ["llama3:latest"],
    index=0
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05
)

# -------------------------------------------------
# Initialize state (CRITICAL)
# -------------------------------------------------
email_text = ""

# -------------------------------------------------
# Main layout
# -------------------------------------------------
input_col, result_col = st.columns([1.2, 1])

# -------------------- USER INPUT --------------------
with input_col:
    st.subheader("Email Input")

    uploaded_file = st.file_uploader(
        "Upload an email file (.txt or .eml)",
        type=["txt", "eml"]
    )

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".eml"):
            email_text = extract_email_body(uploaded_file)
        else:
            email_text = uploaded_file.read().decode("utf-8", errors="ignore")

        st.text_area("Email content", email_text, height=260)
    else:
        email_text = st.text_area(
            "Email content",
            height=300,
            placeholder="Paste the email text here..."
        )

# -------------------- RESULTS --------------------
with result_col:
    st.subheader("Results")
    analyze_clicked = st.button("Analyze Email", use_container_width=True)

# -------------------------------------------------
# Main logic
# -------------------------------------------------
if analyze_clicked:
    if not email_text.strip():
        st.warning("Please enter an email.")
    else:
        with st.spinner("Analyzing with LLaMA..."):
            full_prompt = f"{SYSTEM_PROMPT}\n\nEmail:\n{email_text}"
            raw_output = classify_email(
                full_prompt,
                model=model_name,
                temperature=temperature
            )

        try:
            json_text = extract_json(raw_output)

            if not json_text:
                raise json.JSONDecodeError("No JSON found", raw_output, 0)

            result = json.loads(json_text)

            # -------- Results display --------
            with result_col:
                st.success(f"Category: {result['category']}")
                st.metric("Confidence", f"{result['confidence']}%")

                st.markdown("### Why this category?")
                st.info(result["explanation"])

            # -------- Highlighted email --------
            st.markdown("---")
            st.subheader("Highlighted Email")

            highlighted = highlight_text(
                email_text,
                result.get("highlights", [])
            )

            st.markdown(highlighted, unsafe_allow_html=True)

        except json.JSONDecodeError:
            st.error("LLaMA returned invalid JSON.")
            st.code(raw_output)
