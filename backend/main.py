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
    replicate: str = Form(...),
    add: str = Form(...)
):

    image_data = await image.read()
    base64_image = base64.b64encode(image_data).decode("utf-8") 

    # print("extracting image features...")
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Describe this image in detail for AI-generated prompts."},
            {"role": "user", "content": [
            {"type": "text", "text": f"From this image, extract only the details related to: {replicate}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=500
    )


    extracted_features = response.choices[0].message.content 
    # print("EXTRACTED FEATURES FROM IMAGE: ")
    print(extracted_features)
    # print("CREATING FINAL PROMPT...")

    final_prompt_response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Combine the extracted image details with the user's additional instructions into a high-quality prompt for AI image generation."},
            {"role": "user", "content": f"""
                - Extracted Reference Image Details: {extracted_features}
                - User Wants to Create Image of: {add}
                - Goal: Combine both into a natural, high-quality prompt for AI-generated images.
                - Make sure the prompt is clear, descriptive, and formatted naturally.
            """}
        ],
        max_tokens=300
    )

    enhanced_prompt = final_prompt_response.choices[0].message.content

    # print("FINAL PROMPT: ")
    # print(enhanced_prompt)

    return {
        "message": "Image analyzed",
        "prompt": enhanced_prompt
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8012)
