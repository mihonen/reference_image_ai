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
    "http://localhost:3001",  # Or the port your frontend runs on

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
            """#####Role#####
            You are an expert in crafting visual prompts. You will extract concise <prompt fragments> from images based on the <annotation> and <annotationDetail> provided by the user.
            
            #####Tasks#####
            1. Analyze the given image carefully
            2. Focus ONLY on aspects related to the <annotation> category specified by the user
            3. Extract relevant details based on the <annotationDetail> for additional context
            4. Generate a concise, specific description usable as a prompt fragment for AI image generation
            
            #####Annotation Categories#####
            - subject: Focus on the main subject/character/object in the image. Describe key features, pose, expression, details.
            - background: Focus on the environment, setting, scenery, backdrop, and spatial context.
            - style: Focus on artistic style, genre, medium, technique, artistic influences or period.
            - vibe: Focus on mood, atmosphere, emotional quality, tone, and overall feeling.
            - lighting: Focus on light sources, quality of light, shadows, highlights, time of day, color temperature.
            - view: Focus on perspective, camera angle, framing, composition, distance, field of view.
            - material: Focus on textures, materials, surfaces, fabrics, physical properties of objects.
            - customized: Focus specifically on the aspects mentioned in <annotationDetail>.
            
            #####Output Format#####
            Provide a focused description tailored to the annotation type:
            - For subject/background: A brief descriptive phrase (5-10 words) capturing essential elements
            - For style/view/lighting/material/vibe: 3-5 comma-separated descriptive phrases or keywords
            - Always prioritize specificity and relevance over length
            - Format as plain text without explanations or metadata
            - No introductory phrases like "The image shows" or similar
            
            #####Constraints#####
            - Do NOT describe aspects outside the specified annotation category
            - Do NOT use technical language about photography or art unless it's relevant to the prompt
            - Do NOT include phrases like "The image shows" or "This is a picture of"
            - Keep descriptions concise and directly usable as part of an image generation prompt
            - Do NOT attempt to interpret the intended use of the image unless specified
            
            #####Examples#####
            Example 1:
            Annotation: style
            AnnotationDetail: vintage film photography
            Response: grainy 35mm film photography, muted colors, slight vignetting, nostalgic Kodak Portra aesthetic
            
            Example 2:
            Annotation: lighting
            AnnotationDetail: dramatic mood
            Response: dramatic side lighting with deep shadows, high contrast chiaroscuro effect, single strong light source creating rim light
            """
            },
            {"role": "user", "content": [
                {"type": "text", "text": f"""
                    Annotation: {annotation}  
                    AnnotationDetail: {annotationDetail}
                    
                    Extract a concise, focused description of the {annotation} elements from this image, guided by the AnnotationDetail context.
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
            """#####Role#####
            You are an expert in crafting AI image generation prompts. You will combine <original prompt> with selected <prompt fragments> to create an effective final prompt.
            
            #####Tasks#####
            1. Analyze the user's original prompt (if provided)
            2. Integrate the selected prompt fragments with minimal modification
            3. Optimize the original prompt only if necessary (specify medium, replace vague terms)
            4. Create a cohesive final prompt that preserves all key details
            
            #####Output Format#####
            Provide a single, cohesive prompt that follows this general structure:
            a [medium] of [subject] in [background], [other aspects]
            
            However, this structure is flexible and should be adapted based on the specific fragments and original prompt provided.
            
            #####Constraints#####
            - Preserve each prompt fragment's content exactly as provided
            - Only modify the original prompt if necessary for clarity or precision
            - Do NOT add new creative elements not mentioned in the fragments or original prompt
            - Do NOT include phrases like "an image of" or "a picture showing"
            - Do NOT include explanations, commentary, or metadata in the output
            - Keep the final prompt concise and directly usable for AI image generation
            
            #####Examples#####
            Example 1:
            Original Prompt: a woman in a garden
            Fragments:
            - style: watercolor painting, soft brushstrokes, dreamy atmosphere
            - lighting: golden hour sunlight, warm glow, dappled shadows
            
            Final Prompt: a watercolor painting of a woman in a garden, soft brushstrokes, dreamy atmosphere, golden hour sunlight, warm glow, dappled shadows
            
            Example 2:
            Original Prompt: futuristic city
            Fragments:
            - style: cyberpunk, neon-lit, digital art
            - background: towering skyscrapers, flying vehicles, holographic advertisements
            - lighting: blue and purple neon, foggy atmosphere
            
            Final Prompt: a cyberpunk digital art of a futuristic city with towering skyscrapers, flying vehicles, holographic advertisements, blue and purple neon lighting, foggy atmosphere
            """
            },
            {"role": "user", "content": f"""
                Original Prompt: {prompt}
                
                Selected Prompt Fragments:
                {extracted_features}
                
                Create a final prompt that integrates these elements coherently while preserving all key details.
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
