from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
from io import BytesIO
import fitz  # PyMuPDF

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Shared memory for uploaded PDF
DOCUMENT_MEMORY = ""

# Initialize app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for /ask endpoint
class AskRequest(BaseModel):
    question: str
    policyDate: str = None
    userInfo: str = None

    # Pydantic model
class UserLogin(BaseModel):
    email: str
    password: str

# Login endpoint
@app.post("/login")
async def login_user(user: UserLogin):
    if user.email == "test@example.com" and user.password == "password123":
        # Simulated JWT token
        fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        return JSONResponse(content={
            "status": "success",
            "message": "Login successful!",
            "token": fake_token
        })
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# ------------------- /ask -------------------
@app.post("/ask")
async def ask_question(data: AskRequest):
    global DOCUMENT_MEMORY

    prompt = f"""
You are a helpful insurance assistant.
User Info: {data.userInfo}
Policy Date: {data.policyDate}
Question: {data.question}
Relevant Policy Document:
{DOCUMENT_MEMORY}
"""
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        body = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        if "candidates" in result:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            answer = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

# ------------------- /upload-doc -------------------
@app.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    global DOCUMENT_MEMORY
    contents = await file.read()

    try:
        with fitz.open(stream=BytesIO(contents), filetype="pdf") as doc:
            pdf_text = "".join([page.get_text() for page in doc])

        DOCUMENT_MEMORY = pdf_text  # Store for reuse

        prompt = f"Summarize the key coverage features from the following insurance policy document:\n\n{pdf_text}"
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        body = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        if "candidates" in result:
            summary = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            summary = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"

        return {
            "status": "success",
            "filename": file.filename,
            "summary": summary
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ------------------- /check-claim -------------------
@app.post("/check-claim")
async def check_claim(
    claim_type: str = Form(...),
    expense_description: str = Form(...),
    hospital_preference: str = Form(None),
    bill: UploadFile = File(None)
):
    try:
        combined_input = f"""
Claim Type: {claim_type}
Expense Description: {expense_description}
Preferred Hospital: {hospital_preference or 'N/A'}
Bill Attached: {"Yes" if bill else "No"}

Please analyze this information and determine whether this claim is likely eligible under the uploaded insurance policy terms.
Policy Document:
{DOCUMENT_MEMORY}
"""
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        body = {
            "contents": [{"parts": [{"text": combined_input}]}]
        }

        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        if "candidates" in result:
            decision = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"status": "success", "result": decision}
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ------------------- /recommend-policy -------------------
@app.post("/recommend-policy")
async def recommend_policy(
    user_age: str = Form(...),
    user_gender: str = Form(...),
    health_conditions: str = Form(...),
    coverage: str = Form(...),
    budget: str = Form(...)
):
    prompt = f"""
You are a health insurance advisor AI.
User Age: {user_age}
Gender: {user_gender}
Health Conditions: {health_conditions}
Desired Coverage: {coverage}
Budget: ₹{budget}

Based on this profile, suggest 2-3 suitable insurance policy types or plan features.
"""
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        body = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        if "candidates" in result:
            recommendations = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"status": "success", "recommendations": recommendations}
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    from fastapi import Form

@app.post("/recommend-policy")
async def recommend_policy(
    user_age: str = Form(...),
    user_gender: str = Form(...),
    health_conditions: str = Form(...),
    coverage: str = Form(...),
    budget: str = Form(...)
):
    prompt = f"""
You are a smart insurance advisor. Based on the following profile, suggest 2-3 personalized insurance policies or plan features:
- Age: {user_age}
- Gender: {user_gender}
- Health Conditions: {health_conditions}
- Desired Coverage: {coverage}
- Budget: ₹{budget}

Please keep the suggestions realistic for the Indian market and include reasoning for each.
"""

    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        body = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        if "candidates" in result:
            recommendations = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"status": "success", "recommendations": recommendations}
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    


    