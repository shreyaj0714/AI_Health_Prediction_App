AI Health Prediction Application

Project Overview
The AI Health Prediction Application is a Python-based application that helps manage patient records and generates AI-based health remarks using blood test information.

Features
- Add new patient records.
- View all saved patient records.
- Update patient information.
- Delete patient records.
- Validate email addresses and dates of birth.
- Validate numeric and non-negative blood test values.
- Generate AI-based health remarks using Google's Gemini API.
- Store patient information using an SQLite database.

Technologies Used
- Python
- Streamlit
- SQLite
- Google Gemini API
- Pandas

Project Structure
- `app.py` – Main application and user interface.
- `database.py` – Database operations.
- `validation.py` – Input validation.
- `ai_service.py` – AI API integration.
- `requirements.txt` – Project dependencies.

Installation and Setup

1. Clone the repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Open the project folder:
   ```bash
   cd AI_Health_Prediction_App
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   python -m streamlit run app.py
   ```

Note
AI-generated remarks are intended for informational purposes only and should not be considered a medical diagnosis.

Author
Shreya Jain
