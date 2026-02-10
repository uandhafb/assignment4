# minimal-flask-app
Minimal code for Flask app making calls to the OpenAI API


```
# Create virtual environment
python3 -m venv ./venv

# Activate your virtual environment
source venv/bin/activate

# Install the required packages. For example
pip3 install flask openai python-dotenv

# Rename the file .env-bup to .env 
# Add your OPENAI_API_KEY to the .env file.

# Run the app
python3 app.py

## User interaction and interface Modification

1. The user selects a language (English or PT-BR).
2. The user enters a dream description in a text field.
3. Upon submission, the application generates:
   - a Jungian-style textual interpretation (to be implemented)
   - a symbolic image inspired by the dream (to be implemented)
4. Both outputs are displayed side by side in a visually framed layout.
