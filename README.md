
# RAG MCQ Generator

This project is a Retrieval-Augmented Generation (RAG) system for generating multiple-choice questions (MCQs). It consists of a TypeScript React frontend and a FastAPI backend.

## Project Structure

```

project-root/
│
├── frontend/         # React frontend (TypeScript, .tsx files)
│
├── mcqs_rag/         # Backend (FastAPI)
│   ├── main.py
│   └── ...
│
├── requirements.txt  # Backend dependencies
│
└── .env              # Environment variables (see below)

````

## Setup

### Backend

1. Navigate to the backend folder:

```bash
cd mcqs_rag
````

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
```

4. Create a `.env` file in the **root folder**, at the same level as `mcqs_rag`, and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

5. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

### Frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

## Environment Variables

* `GOOGLE_API_KEY`: Required for accessing Google APIs used in the backend.

## Notes

* Ensure that the `.env` file is located at the same level as the `mcqs_rag` folder.
* The frontend communicates with the backend via API endpoints exposed by FastAPI. Update the API URL in the frontend if necessary.

```

I can also add sections for **Usage**, **Deployment**, and **License** if you want a more complete professional README. Do you want me to do that?
```
