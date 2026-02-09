import os
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_file, session
import pandas as pd
from ai_extractor import extract_story_components
from generator import generate_test_cases

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "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")


@app.route("/", methods=["GET"])
def index():
    # Clear session to ensure a fresh start on reload
    session.clear()
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    story = request.form.get("story", "").strip()
    if not story:
        return redirect(url_for("index"))
    api_key = os.environ.get("HF_API_KEY", "")
    components = extract_story_components(story, api_key)
    role = components.get("role", "")
    feature = components.get("feature", "")
    benefit = components.get("benefit", "")

    # If extraction failed (all empty), hide the components section in UI
    if not role and not feature and not benefit:
        components = None

    test_cases = generate_test_cases(role, feature, benefit, api_key=api_key, story=story)
    session["components"] = components
    session["test_cases"] = test_cases
    session["story"] = story
    return render_template("index.html", components=components, test_cases=test_cases, story=story)


@app.route("/download", methods=["GET"])
def download():
    test_cases = session.get("test_cases")
    if not test_cases:
        return redirect(url_for("index"))
    df = pd.DataFrame(test_cases, columns=[
        "Test Case ID",
        "Description",
        "Preconditions",
        "Test Steps",
        "Expected Result",
        "Test Type",
    ])
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="generated_test_cases.csv",
        mimetype="text/csv",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
