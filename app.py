import os
from flask import Flask, render_template, request, send_file, Response
from ai_engine import generate_testcases, convert_to_dataframe

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    user_story = request.form.get("user_story")

    try:
        raw_output = generate_testcases(user_story)
        df = convert_to_dataframe(raw_output)
        results = df.to_dict(orient="records")
        csv_content = df.to_csv(index=False)

        return render_template(
            "index.html",
            results=results,
            csv_content=csv_content,
            user_story=user_story
        )

    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/download")
def download():
    return "Download not available via this route."


if __name__ == "__main__":
    app.run(debug=True)