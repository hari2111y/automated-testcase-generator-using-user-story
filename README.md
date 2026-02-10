# AI Test Case Generator

A powerful web application that uses Artificial Intelligence to automatically generate comprehensive QA test cases from user stories.

## Features

- **Smart Parsing**: Instantly extracts Role, Feature, and Benefit from your user story as you type.
- **AI-Powered Generation**: Uses Meta's Llama-3 model to generate 12-15 diverse test cases (Positive, Negative, Boundary, Security, etc.).
- **Structured Output**: Presents test cases in a clean, professional table with distinct categories.
- **CSV Export**: Download your generated test cases directly to CSV for use in Jira, Excel, or other test management tools.
- **Responsive UI**: Modern interface built with Bootstrap 5 and dynamic JavaScript interactions.

## Prerequisites

- Python 3.8+
- A Hugging Face API Token (currently configured in `ai_engine.py`)

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:

```bash
python app.py
```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

3. Enter a user story in the standard format:
   > "As a **[role]**, I want **[feature]** so that **[benefit]**."

4. Click **Generate Test Cases** to receive a structured list of test scenarios.

## Project Structure

- `app.py`: Main Flask application handling routes and UI rendering.
- `ai_engine.py`: Core logic for interacting with the AI model and processing data.
- `templates/index.html`: The frontend user interface.
- `requirements.txt`: Python dependencies.

## Technologies

- **Backend**: Python, Flask, Pandas, Hugging Face Inference API
- **Frontend**: HTML5, Bootstrap 5, JavaScript
