from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()


app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




@app.route("/", methods=["GET", "POST"])
def index():
   result = None
   selected_color = None
   prompt = None
   lang = "en"
   image_data_url = None


   if request.method == "POST":
       prompt = (request.form.get("prompt") or "").strip()
       selected_color = (request.form.get("color") or "").strip()
       lang = request.form.get("lang", "en")


       if not selected_color:
           selected_color = "Cool Blue"


       if not prompt:
           prompt = "(No dream text provided.)" if lang == "en" else "(Nenhum texto de sonho foi fornecido.)"


       try:
           # 1) TEXT MODEL → exactly 2 lines
           text_resp = client.chat.completions.create(
               model="gpt-4.1",
               messages=[
                   {
                       "role": "developer",
                       "content": (
                           "You are a world-class Jungian Psychiatrist and Psychologist with a deep mastery of Analytical Psychology "
                           "and Alchemical symbolism. You specialize in the 'Insights Discovery' four-color model "
                           "(Fiery Red, Sunshine Yellow, Earth Green, and Cool Blue) and how these energies map to Jung’s psychological functions.\n\n"
                           "Reference Guide:\n"
                           "Fiery Red: (Thinking/Extroverted) Decisive, bold, assertive.\n"
                           "Sunshine Yellow: (Intuition/Extroverted) Cheerful, enthusiastic, sociable.\n"
                           "Earth Green: (Feeling/Introverted) Calm, loyal, supportive.\n"
                           "Cool Blue: (Sensation/Introverted) Analytical, precise, detached.\n\n"
                           "LANGUAGE RULE:\n"
                           "- If lang = pt-BR, write in Brazilian Portuguese.\n"
                           "- If lang = en, write in English.\n\n"
                           "OUTPUT FORMAT (MUST FOLLOW EXACTLY):\n"
                           "Return EXACTLY 2 lines.\n"
                           "Line 1: ONE short, witty, fun therapist-style sentence combining dream + color.\n"
                           "Line 2: EXACTLY 3 evocative words separated by comma+space.\n"
                           "No extra text."
                       ),
                   },
                   {"role": "user", "content": f"Dream: {prompt}\ncolor: {selected_color}\nlang: {lang}"},
               ],
               temperature=0.6,
               max_tokens=160,
           )


           result = text_resp.choices[0].message.content.strip()


           # 2) Take ONLY the second line (no word extraction)
           lines = [ln.strip() for ln in result.splitlines() if ln.strip()]
           if len(lines) < 2:
               raise ValueError("The text model did not return 2 lines, so there is no second line for the image prompt.")


           second_line = lines[1]  # <-- THIS is the prompt for the image model


           # 3) IMAGE MODEL receives EXACTLY the second line as prompt
           img = client.images.generate(
               model="gpt-image-1",
               prompt=second_line,
               n=1,
               size="1024x1024",
               
           )


           # 4) Send image to HTML as a data URL
           image_data_url = f"data:image/png;base64,{img.data[0].b64_json}"


       except Exception as e:
           result = f"Error: {str(e)}"
           image_data_url = None


   return render_template(
       "index.html",
       result=result,
       color=selected_color,
       prompt=prompt,
       lang=lang,
       image_data_url=image_data_url
   )




if __name__ == "__main__":
   app.run(debug=True)