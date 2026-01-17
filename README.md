# HealthInsure AI Assistant 🚑🤖

An intelligent, AI-powered health insurance assistant built for **HackRx 6.0** – organized by Bajaj Finserv. This project simplifies the insurance journey for users by leveraging Google Gemini AI, FastAPI, and modern frontend technologies.

## 🌟 Features

### 🔍 Ask AI (General & Document-Specific)
- Ask health insurance-related questions using Google Gemini.
- Upload policy documents and query based on the document context.

### 📄 Document AI
- Upload your health insurance PDF.
- Automatically extract full text and summary using PyMuPDF.
- Ask questions related to your policy.

### 🧾 Claim Check
- Submit claim details and dummy bills.
- AI evaluates eligibility, explains reasoning, and lists required documents.

### 📋 Policy Recommendations
- Input personal and medical data to receive AI-recommended insurance policies.

### 🏥 Hospital Finder
- Find cashless network hospitals in your city via Gemini queries.

### 📊 Analytics Dashboard
- View mock analytics for claim stats, approval rates, and policy insights.

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Tailwind CSS for styling
- Responsive design for all devices

### Backend
- Python 3.8+
- FastAPI web framework
- SQLite database
- PyMuPDF for PDF processing
- Google Gemini Pro API for AI capabilities

### Dependencies
- FastAPI
- Uvicorn (ASGI server)
- PyMuPDF
- Google Generative AI
- Python-dotenv
- Other dependencies listed in `hackrx-backend/requirements.txt`

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js and npm (for frontend development)
- Google Gemini API key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd hackrx-backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the `hackrx-backend` directory with your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup
1. Open `hackrx-frontend/frontend.html` in your web browser
2. Alternatively, use a local development server like Live Server in VS Code

## 📁 Project Structure

```
.
├── hackrx-backend/           # Backend server code
│   ├── __pycache__/         # Python bytecode cache
│   ├── .env                 # Environment variables
│   ├── backend.py           # Main backend logic
│   ├── main.py              # FastAPI application
│   ├── project.db           # SQLite database
│   └── requirements.txt     # Python dependencies
│
├── hackrx-frontend/         # Frontend code
│   ├── frontend.html        # Main frontend interface
│   ├── try.html             # Alternative frontend page
│   └── README.md            # Frontend documentation
│
└── README.md                # This file
```

## 📝 API Endpoints

### Health Check
- `GET /` - Basic health check endpoint

### AI Chat
- `POST /ask` - Process user questions with AI
- `POST /ask_document` - Process questions about uploaded documents

### Document Processing
- `POST /upload` - Upload and process insurance documents
- `GET /document/{doc_id}` - Get document details

### Claims
- `POST /check_claim` - Check claim eligibility
- `GET /claims` - List all claims

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- [Your Name]
- [Team Member 2]
- [Team Member 3]

## 📅 Project Status

- Hackathon: HackRx 6.0
- Organizer: Bajaj Finserv
- Submission Date: August 07, 2025

---

💡 **Note**: This project was developed as part of a hackathon and is for demonstration purposes only.
