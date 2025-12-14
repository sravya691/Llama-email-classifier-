# Email Classifier - Intent and Category Detection

This project is a **Streamlit-based email classification and analysis system** powered by a **local LLaMA model via Ollama**.

It goes beyond simple classification by providing:
- Explainable reasoning
- Evidence-based highlights
- Confidence scores
- Robust handling of real-world email formats (`.txt`, `.eml`)
- Prompt-driven intelligence (no hard-coded ML logic)

---

## Key Features

- **Email Classification**
  - Classifies emails into known categories
  - Can dynamically create new categories when needed

- **Explainable AI**
  - Returns a short explanation for every classification
  - Highlights exact phrases used to justify the decision

- **Confidence Scoring**
  - Model-generated confidence score (0–100%)

- **Robust JSON Handling**
  - Automatically extracts valid JSON from LLaMA outputs
  - Prevents crashes caused by extra explanatory text

- **Email File Support**
  - Upload `.txt` or `.eml` files
  - Safely extracts plain text from `.eml` emails

- **Model Controls**
  - Select LLaMA model (via Ollama)
  - Adjust temperature for deterministic vs creative output

- **Fully Local Inference**
  - No external APIs
  - Email data never leaves your machine

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** – UI and interaction
- **Ollama** – Local LLM serving
- **LLaMA** – Language model
- **Requests** – HTTP calls to Ollama API



##  How to Run the Project

### Start Ollama
Make sure Ollama is running locally:

```bash
ollama serve

Verify model availability:

ollama list

Install Dependencies
pip install -r requirements.txt

Run the Streamlit App
streamlit run app.py


Open in browser:

http://localhost:8501


How It Works (High Level)

User uploads or pastes an email

Email text is cleaned (headers removed for .eml)

A structured prompt is sent to LLaMA via Ollama

LLaMA returns a JSON-like response

The app:

Extracts valid JSON

Parses fields safely

Displays category, confidence, explanation, and highlights

All decision-making logic lives in the prompt, not in Python code.



Example Output
{
  "category": "Lost and Found",
  "confidence": 90,
  "highlights": ["lost OnePlus neckband", "main campus"],
  "explanation": "The email describes a lost personal item and provides contact information."
}