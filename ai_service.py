
import os
from dotenv import load_dotenv
from google import genai

# Load the private API key from the .env file
load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_health_remarks(
    glucose, haemoglobin, cholesterol
):
    """Generate informational health observations using Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return False, "Gemini API key is missing. Check your .env file."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an informational health assistant.

        Review these patient blood test values:

        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        Provide:
        1. A brief observation about each value.
        2. Any values that may need medical attention.
        3. A short recommendation to consult a qualified
           healthcare professional when appropriate.

        Important rules:
        - Do not diagnose any disease.
        - Do not claim that a condition is confirmed.
        - Do not prescribe medicines or treatments.
        - Do not invent missing patient information.
        - Explain that interpretation depends on units,
          laboratory reference ranges and clinical context.
        - Keep the response clear and concise.
        """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            return False, "The AI returned an empty response."

        return True, response.text.strip()

    except Exception as error:
        return False, f"AI API error: {str(error)}"