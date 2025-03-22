from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this import

import os
from dotenv import load_dotenv
import openai
import io
from PIL import Image
import base64

app = FastAPI()
 
origins = [
    "http://localhost",  # Allow frontend to connect
    "http://127.0.0.1",  # Allow frontend to connect
    "http://localhost:3000",  # Or the port your frontend runs on
]

# Add the middleware to the app to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins in the list above
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.post("/generate")
async def generate_image(
    image: UploadFile = File(...),
    annotation: str = Form(...),
    annotationDetail: str = Form(...)
):


    image_data = await image.read()
    base64_image = base64.b64encode(image_data).decode("utf-8") 

    # print("extracting image features...")
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": 
            "You analyze images and generate **concise, natural descriptions** that summarize the most important visual aspects. "
            "The response should be short (1-3 sentences) and capture the essence of the image in a way that is useful for AI image generation."
            },
            {"role": "user", "content": [
                {"type": "text", "text": f"""
                    User Request: "{annotation}"  
                    Additional Context: "{annotationDetail}"  
                    
                    Extract a **concise, natural description** of the key elements relevant to the user’s request.  
                    Keep it **brief and readable** (1-3 sentences). Avoid technical breakdowns.
                """},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=400
    )



    extracted_features = response.choices[0].message.content 
    # print("EXTRACTED FEATURES FROM IMAGE: ")
    # print(extracted_features)
    # print("CREATING FINAL PROMPT...")

# 
    # print("FINAL PROMPT: ")
    # print(enhanced_prompt)

    return {
        "message": "Image analyzed",
        "prompt": extracted_features
    }

@app.post("/generate_prompt")
async def generate_prompt(
    extracted_features: str = Form(...),
    prompt: str = Form(...)
    ):

    final_prompt_response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": 
                "Your task is to create a **concise, high-quality AI image prompt** by strictly following the user's instructions "
                "and integrating extracted details from reference images. DO NOT add unnecessary elements—only describe what is given."
            },
            {"role": "user", "content": f"""
                - **User's Request**: {prompt}  
                - **Extracted Image Details**: {extracted_features}  

                **Create a concise, controlled prompt that merges these elements naturally.**
                - **Do not add new objects, characters, or scenery unless explicitly mentioned.**
                - **Ensure the final prompt reads smoothly but remains focused on the given details.**
                - **Keep the length reasonable—focus on clarity over excess description.**
            """}
        ],
        max_tokens=500  
    )


    enhanced_prompt = final_prompt_response.choices[0].message.content

    return {
        "message": "Image analyzed",
        "prompt": enhanced_prompt
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8012)
