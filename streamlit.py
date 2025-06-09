from google import genai
import streamlit as st

# Initialize the Gemini client
client = genai.Client(api_key="AIzaSyD9REPxKUXcIvBCAvBcI6frw9OypNEnv54")

# Summarizer function using Gemini API
def generate_summary(input_text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # Replace with the appropriate Gemini model ID
        contents=f"Summarize the following text:\n\n{input_text}",
    )
    return response.text

# Validator function using Gemini API
def validate_summary(input_text, summary_text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Does this summary accurately capture the main points of the text? "
            f"Provide a 'yes' or 'no' and explain why.\n\nOriginal Text:\n{input_text}\n\nSummary:\n{summary_text}"
        ),
    )
    evaluation = response.text.strip()
    is_valid = "yes" in evaluation.lower()
    return is_valid, evaluation

# Regeneration loop
def regenerate_until_valid(input_text, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        summary = generate_summary(input_text)
        is_valid, explanation = validate_summary(input_text, summary)
        if is_valid:
            return summary, explanation
        attempts += 1
    return None, "Validation failed after multiple attempts."

# Streamlit App
st.title("Abstract Summarizer with Validation")
st.subheader("Generate validated summaries using Gemini API!")

# Input Section
input_text = st.text_area("Enter the text to summarize:", height=300)

if st.button("Generate Validated Summary"):
    if input_text.strip():
        with st.spinner("Generating and validating the summary..."):
            final_summary, validation_feedback = regenerate_until_valid(input_text)
            if final_summary:
                st.success("Validated Summary:")
                st.write(final_summary)
                st.info(f"Validation Feedback: {validation_feedback}")
            else:
                st.error("Could not generate a valid summary after multiple attempts.")
    else:
        st.warning("Please enter some text to summarize.")
