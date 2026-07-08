# Health Prediction App — React + Python Flask

A health prediction application with a React frontend and a Python Flask REST API backend,
integrated with Google Gemini AI for health risk prediction based on patient blood test values.

## Project Structure

```
health_react/
├── backend/
│   ├── app.py            # Flask REST API (5 endpoints)
│   ├── database.py       # SQLite setup and connection
│   ├── ai_service.py     # Google Gemini AI call
│   ├── requirements.txt
│   └── .gitignore
└── frontend/
    └── index.html        # React app (single file, no build step needed)
```

## Tech Stack

| Layer    | Technology                              |
|----------|-----------------------------------------|
| Frontend | React 18 (via CDN, no build step)       |
| Backend  | Python 3.10+, Flask, Flask-CORS         |
| Database | SQLite                                  |
| AI/ML    | Google Gemini API (gemini-1.5-flash)    |

## API Endpoints

| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| GET    | /api/patients        | List all patients    |
| POST   | /api/patients        | Create new patient   |
| GET    | /api/patients/:id    | Get single patient   |
| PUT    | /api/patients/:id    | Update patient       |
| DELETE | /api/patients/:id    | Delete patient       |



<img width="676" height="463" alt="Screenshot 2026-07-08 225405" src="https://github.com/user-attachments/assets/a7183fe4-371f-417d-94d8-0053792ddbca" />


<img width="676" height="463" alt="Screenshot 2026-07-08 225405" src="https://github.com/user-attachments/assets/53704807-484e-4143-b268-02a58b1d0193" />


<img width="676" height="463" alt="Screenshot 2026-07-08 225405" src="https://github.com/user-attachments/assets/23fa16c7-e738-4bd6-8e34-47a46f635880" />


## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:
```
GEMINI_API_KEY=your_key_here
```

Get a free key from https://aistudio.google.com/app/apikey

Run the Flask server:
```bash
python app.py
```

Backend runs at http://localhost:5000

### Frontend

Open `frontend/index.html` directly in your browser.
No npm, no build step, no Node.js required.

Make sure the Flask backend is running first.

## Notes

- All API keys are in `.env` which is listed in `.gitignore` and never committed to GitHub.
- Patient data is stored locally in `patients.db` which is also excluded from GitHub.
- The React app uses CDN imports so no build tool is needed.
- This is for educational/assessment purposes. AI predictions are not medical advice.
