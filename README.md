# VEDA-2K26 AI Agent Challenge

This project is a full-stack web application for the VEDA-2K26 AI Agent Challenge portal. It keeps the original UI design intact while separating the frontend and backend responsibilities.

## Project Structure

```txt
veda/
├── backend/
│   ├── app.py
│   └── test_api.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── styles.css
│   └── assets/
├── requirements.txt
└── README.md
```

## Features

- Responsive event landing page for VEDA-2K26
- Problem statements dashboard
- Registration and project submission forms
- Backend API for data and form handling
- Frontend served through the backend for a real full-stack flow

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- API support: Flask-CORS

## Prerequisites

- Python 3.10+
- pip

## Installation

1. Open a terminal in the project root.
2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv


3. Activate the virtual environment:

- Windows:

```bash
cd venv\Scripts
activate.bat
```

- macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root, run:

```bash
python backend/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Endpoints

- `GET /api/health` — backend health check
- `GET /api/problems` — returns challenge problem statements
- `POST /api/register` — registers a team
- `POST /api/submit` — submits a project

## Backend Validation

You can run the API smoke test using:

```bash
python backend/test_api.py
```

## Notes

- The frontend UI design was not changed.
- The backend acts as a simple full-stack layer for serving the existing interface and handling form/API logic.
- This is a lightweight development setup and can be expanded with a database or a larger frontend framework later.

## License

This project is intended for educational and hackathon use.
