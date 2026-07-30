from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os
import markdown

from PIL import Image
from pypdf import PdfReader

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/app", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        text = request.form.get("text", "")
        audience = request.form.get(
            "audience",
            "General public"
        )

        uploaded_file = request.files.get("file")

        content = ""

        # ---------- TEXT ----------
        if text.strip():
            content += text

        # ---------- FILE ----------
        if uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename.lower()

            # PDF
            if filename.endswith(".pdf"):

                reader = PdfReader(uploaded_file)

                pdf_text = ""

                for page in reader.pages:
                    pdf_text += page.extract_text() or ""

                content += "\n\n" + pdf_text

            # IMAGE
            elif filename.endswith((".png", ".jpg", ".jpeg")):

                image = Image.open(uploaded_file)

                prompt = f"""
You are BridgeAI, an accessibility assistant.

Analyze this image.

Audience:
{audience}

Provide:

## Simple Explanation

## Key Points

## Important Actions
"""

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[prompt, image]
                )

                result = markdown.markdown(response.text)

                return render_template(
                    "index.html",
                    result=result
                )

        # ---------- NO INPUT ----------
        if not content.strip():

            result = """
<p>Please upload a PDF, image, or paste text first.</p>
"""

        # ---------- TEXT/PDF ----------
        else:

            prompt = f"""
You are BridgeAI, an accessibility assistant.

Simplify the following information.

Audience:
{audience}

Provide:

## Simple Explanation

## Key Points

## Important Actions

Information:

{content}
"""

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            result = markdown.markdown(response.text)

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
