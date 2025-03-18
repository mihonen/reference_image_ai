# Reference guided AI image generation

## Overview

This project includes a **frontend** built with **Nuxt 3** and **Vue.js** and a **backend** built with **Python** and **FastAPI**. The frontend communicates with the backend to generate AI-based images using reference images and user prompts.



## Requirements

### Frontend (Nuxt 3 / Vue.js)

1. **Install dependencies**:
    ```bash
    cd frontend
    npm install
    ```

2. **Run the development server**:
    ```bash
    npm run dev
    ```

    - The frontend will be available at `http://localhost:3000`.

### Backend (Python / FastAPI)

1. **Create and activate a virtual environment** (if you haven't already):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the required Python dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. **Run the backend server**:
    ```bash
    python3 main.py
    ```

    - The backend will be available at `http://127.0.0.1:8012`.

## Usage

- The frontend will allow users to upload reference images and input text prompts.
- Once the user submits the form, the frontend sends the data to the backend.
- The backend processes the reference image and prompt, combining them to create a high-quality image generation prompt.
- The backend then returns the prompt to client.


