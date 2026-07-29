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



        # TEXT INPUT

        if text.strip():

            content += text





        # FILE INPUT

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

            elif filename.endswith(
                (".png",".jpg",".jpeg")
            ):


                image = Image.open(uploaded_file)



                prompt = f"""

You are BridgeAI, an accessibility assistant.

Analyze this image/document.

Audience:
{audience}


Explain:

1. Simple explanation

2. Key points

3. Important actions


"""


                response = client.models.generate_content(

                    model="gemini-3.5-flash",

                    contents=[
                        prompt,
                        image
                    ]

                )


                result = markdown.markdown(
                    response.text
                )


                return render_template(
                    "index.html",
                    result=result
                )






        if not content.strip():


            result = """
            Please upload a file or paste text first.
            """



        else:



            prompt = f"""

You are BridgeAI, an accessibility assistant.

Simplify complex information.

Audience:
{audience}



Provide:


## Simple Explanation

Explain clearly.


## Key Points

Give the important information.


## Important Actions

Explain what the user should do.



Information:

{content}

"""



            response = client.models.generate_content(

                model="gemini-3.5-flash",

                contents=prompt

            )



            result = markdown.markdown(
                response.text
            )




    return render_template(
        "index.html",
        result=result
    )





if __name__ == "__main__":

    app.run(debug=True)