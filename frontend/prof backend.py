from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from pypdf import PdfReader # For PDF parsing

# Configure Google Gemini API
# Replace with your actual API key or load from environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

app = FastAPI()

# CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"], # Adjust as per your frontend server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini model
# Use a suitable model for text generation
text_model = genai.GenerativeModel('gemini-1.5-flash') 
# For document understanding, you might use a model capable of multimodal input if available,
# or process text extracted from PDFs.

@app.get("/")
async def read_root():
    return {"message": "HealthInsure AI Backend is running!"}

# ------------------------- ASK AI Endpoint -------------------------
@app.post("/ask")
async def ask_question(question: str = Form(...), policyDate: str = Form(None), userInfo: str = Form(None)):
    try:
        prompt = f"As a health insurance AI assistant, answer the following question based on typical health insurance policies. Be concise, helpful, and professional.\n\n"
        prompt += f"Question: {question}\n"
        if policyDate:
            prompt += f"Policy Date Coverage Context: {policyDate}\n"
        if userInfo:
            prompt += f"User Context: {userInfo}\n"
        prompt += "Provide a clear and direct answer."

        response = text_model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "answer": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

# ------------------------- DOCUMENT INTELLIGENCE Endpoint -------------------------
@app.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Read PDF content
        pdf_content = await file.read()
        reader = PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        if not text.strip():
            return JSONResponse(content={"status": "error", "message": "Could not extract text from PDF."})

        # Summarize text using Gemini
        summary_prompt = f"Summarize the following health insurance policy document. Highlight key coverages, exclusions, waiting periods, and claim procedures. Keep it concise and easy to understand.\n\nDocument Text:\n{text[:10000]}..." # Limit text to avoid token limits

        summary_response = text_model.generate_content(summary_prompt)
        return JSONResponse(content={"status": "success", "summary": summary_response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing error: {str(e)}")

# ------------------------- CLAIM ASSISTANCE Endpoint -------------------------
@app.post("/check-claim")
async def check_claim(
    claim_type: str = Form(...),
    expense_description: str = Form(...),
    hospital_preference: str = Form(None),
    bill: UploadFile = File(None)
):
    try:
        prompt = f"As a health insurance claim assistant, evaluate the potential eligibility for a claim based on the following details. Provide a clear assessment and any necessary next steps or common considerations.\n\n"
        prompt += f"Claim Type: {claim_type}\n"
        prompt += f"Expense Description: {expense_description}\n"
        if hospital_preference:
            prompt += f"Preferred Hospital/City: {hospital_preference}\n"
        
        # If a bill is uploaded, you'd ideally process it with a multimodal model or OCR
        # For now, we'll just mention its presence in the prompt
        if bill:
            prompt += f"Medical bill uploaded: Yes (needs further analysis if content is required)\n"
            # In a real scenario, you'd send the image/PDF of the bill to a multimodal model
            # or use OCR to extract text and then send the text to Gemini.
            # Example (conceptual, requires actual image processing/multimodal model):
            # bill_content = await bill.read()
            # multimodal_prompt = [prompt, {"mime_type": bill.content_type, "data": bill_content}]
            # response = text_model.generate_content(multimodal_prompt)
        
        prompt += "Is this claim likely eligible? What are the typical steps or documents needed?"

        response = text_model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "result": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claim processing error: {str(e)}")

# ------------------------- POLICY RECOMMENDATIONS Endpoint -------------------------
@app.post("/recommend-policy")
async def recommend_policy(
    user_age: int = Form(...),
    user_gender: str = Form(...),
    health_conditions: str = Form(None),
    coverage: str = Form(...),
    budget: int = Form(...)
):
    try:
        prompt = f"As a health insurance policy recommender, suggest suitable policy types or features based on the following user profile. Provide 2-3 distinct recommendations with brief explanations.\n\n"
        prompt += f"Age: {user_age}\n"
        prompt += f"Gender: {user_gender}\n"
        prompt += f"Health Conditions: {health_conditions if health_conditions else 'None'}\n"
        prompt += f"Desired Coverage: {coverage}\n"
        prompt += f"Annual Budget: ₹{budget}\n\n"
        prompt += "Recommend specific policy types (e.g., Individual Basic Plan, Family Floater, Senior Citizen Plan, Critical Illness Rider) and explain why they fit."

        response = text_model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "recommendations": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")

# ------------------------- WELLNESS & INSIGHTS Endpoint (NEW) -------------------------
@app.post("/wellness-insights")
async def get_wellness_insights(
    wellness_goal: str = Form(None),
    health_data: UploadFile = File(None) # This would be complex to parse in a real app
):
    try:
        prompt = f"As a health and wellness AI, provide insights and actionable advice based on the following. Assume general health principles if no specific data is provided.\n\n"
        if wellness_goal:
            prompt += f"User's Wellness Goal: {wellness_goal}\n"
        if health_data:
            # In a real application, you'd parse CSV/JSON, or use a multimodal model for images.
            # For this example, we'll just acknowledge the data.
            prompt += f"Health data file uploaded ({health_data.filename}).\n"
            prompt += "Based on general knowledge and the user's goal, provide actionable steps for wellness."
        else:
            prompt += "No specific health data provided. Provide general wellness tips for achieving the goal."

        response = text_model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "insights": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wellness insights error: {str(e)}")

# ------------------------- BLOCKCHAIN & SECURITY Endpoint (NEW - Conceptual) -------------------------
@app.post("/blockchain-action")
async def blockchain_action(action: str = Form(...), record_id: str = Form(None)):
    # This is a highly conceptual endpoint.
    # In a real blockchain integration, this would involve:
    # 1. Connecting to a blockchain node (e.g., Web3.py for Ethereum, Hyperledger SDK).
    # 2. Interacting with smart contracts (e.g., to store policy hashes, verify claim status).
    # 3. Handling cryptographic operations.

    try:
        result_message = ""
        if action == "view-records":
            result_message = "This feature would connect to a blockchain explorer to show immutable policy records. (Conceptual: No actual blockchain integration here)."
            if record_id:
                result_message += f"\nAttempting to retrieve record for ID: {record_id}"
            result_message += "\n\nExample: Transaction Hash: 0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b\nData Hash: abcdef1234567890"
        elif action == "verify-claim":
            result_message = "This feature would verify a claim's status against a blockchain ledger for tamper-proof validation. (Conceptual: No actual blockchain integration here)."
            if record_id:
                result_message += f"\nVerifying claim with ID: {record_id}"
            result_message += "\n\nExample: Claim Status: Approved on Blockchain (Transaction: 0x...)"
        else:
            raise HTTPException(status_code=400, detail="Invalid blockchain action.")
        
        return JSONResponse(content={"status": "success", "result": result_message})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain action error: {str(e)}")

# To run this backend:
# 1. Save it as main.py
# 2. Set your GEMINI_API_KEY environment variable (or replace "YOUR_GEMINI_API_KEY" directly)
#    Example: export GEMINI_API_KEY="your_api_key_here"
# 3. Run from your terminal: uvicorn main:app --reload --port 8000
