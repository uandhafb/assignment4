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
   image_data_url1 = None
   image_data_url2 = None
   line2 = None
   line1 = None
   jung_text = None


   if request.method == "POST":
       prompt = (request.form.get("prompt") or "").strip()
       selected_color = (request.form.get("color") or "").strip()
       lang = request.form.get("lang", "en")


       if not selected_color:
           selected_color = "Cool Blue"


       if not prompt:
           prompt = "(No dream text provided.)" if lang == "en" else "(Nenhum texto de sonho foi fornecido.)"


       try:
           # 1) TEXT MODEL → JUNGIAN PSYCHOTHERAPIST + DREAM ANALYSIS + INSIGHTS DISCOVERY COLOR MODEL
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
                           "Return EXACTLY 3 lines.\n"
                           "Line 1: ONE short, witty, fun therapist-style sentence combining dream + color.\n"
                           "Line 2: EXACTLY 3 evocative words separated by comma+space.\n"
                           "Line 3: A short, concise, and insightful interpretation of the dream in relation description given from the input of the user.\n"
                           "the Jungian interpretation (can be multiple lines, but MUST start on line 3).\n"
                           "IMPORTANT: Never stop at 2 lines. Always include the Jungian interpretation.\n"

                       ),
                   },
                   {"role": "user", "content": f"Dream: {prompt}\ncolor: {selected_color}\nlang: {lang}"},
               ],
               temperature=0.6,
               #max_tokens=250,
           )


           result = text_resp.choices[0].message.content.strip()


           # 2) safety check: ensure EXACTLY 3 lines are returned, otherwise raise an error
           lines = [ln.strip() for ln in result.splitlines() if ln.strip()]
           if len(lines) < 3:
               raise ValueError("The model did not return 3 lines.")

           line1 = lines[0]
           line2 = lines[1] 
           jung_text= "\n".join(lines[2:])  


           # 3) IMAGE MODEL1: receives the second line as prompt, which contains 3 evocative words, and generates an image based on that. We will use the "gpt-image-1" model for this. The prompt will be exactly the 3 words separated by commas, without any additional text. For example, if line2 is "mysterious, dark, forest", then the prompt for the image model will be exactly "mysterious, dark, forest". This will create a visual representation of the emotional tone of the dream as interpreted by the therapist model.
           img1 = client.images.generate(
               model="gpt-image-1",
               prompt=line2,
               n=1,
               size="1024x1024",
               
           )
           # 4) Send image to HTML as a data URL
           image_data_url1 = f"data:image/png;base64,{img1.data[0].b64_json}"

           # 5) IMAGE MODEL2 receives the Jungian interpretation as prompt and generates an alchemical symbolic representation of the dream analysis. We will use the "gpt-image-1-mini" model for this, which is a more abstract and artistic image generator. The prompt will be the full Jungian interpretation text (line 3 and beyond), which may contain multiple lines. This will create a symbolic art piece that visually represents the deeper insights of the dream analysis.
           img2 = client.images.generate(
               model="gpt-image-1-mini",
               prompt=f"A symbolic alchemical art piece representing: {jung_text}",
               n=1,
               size="1024x1024",
               
           )
           # 6) Send image to HTML as a data URL
           image_data_url2 = f"data:image/png;base64,{img2.data[0].b64_json}"
  
       except Exception as e:
           result = f"Error: {str(e)}"
           image_data_url1 = None
           image_data_url2 = None



   return render_template(
       "index.html",
       result=result,
       color=selected_color,
       prompt=prompt,
       lang=lang,
       image_data_url1=image_data_url1,
       image_data_url2=image_data_url2,
       line1=line1,
       line2=line2,
       jung_text=jung_text,
   )

if __name__ == "__main__":
   app.run(debug=True)