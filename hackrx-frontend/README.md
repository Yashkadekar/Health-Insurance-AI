# HealthInsure AI Assistant 🚑🤖

An intelligent, AI-powered health insurance assistant built for **HackRx 6.0** – organized by Bajaj Finserv. This project simplifies the insurance journey for users by leveraging Google Gemini AI, FastAPI, and modern frontend technologies.

---

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

---

## 🛠️ Tech Stack

| Layer       | Technology             |
|-------------|-------------------------|
| Frontend    | HTML, Tailwind CSS, JavaScript |
| Backend     | FastAPI (Python)        |
| AI/LLM      | Google Gemini Pro API   |
| Vector DB   | (Planned) ChromaDB      |
| File Parser | PyMuPDF (`fitz`)        |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/healthinsure-ai.git
cd healthinsure-ai
```

### 2. Install backend requirements
```bash
pip install -r requirements.txt
```

### 3. Run FastAPI backend
```bash
uvicorn backend:app --reload
```

### 4. Open `frontend.html` in your browser

---

## 📁 Folder Structure
```
.
├── backend.py
├── frontend.html
├── Dummy_Hospital_Bill.pdf
├── requirements.txt
├── README.md
└── assets/
    └── demo_thumbnail.png
```

---

## 🎥 Demo

Watch the full demo here: [YouTube Demo](https://youtube.com/your-demo-link)

---

## 👨‍💻 Team

- Gaurav Gavali
- [Add Team Members if any]

---

## 📅 Submission

- Hackathon: HackRx 6.0
- Organizer: Bajaj Finserv
- Submitted on: August 07, 2025

---

## 📜 License

This project is open source for educational and hackathon use.
