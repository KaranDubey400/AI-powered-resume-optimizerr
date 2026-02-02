

**AI-powered resume optimizer**

# Craftify
tt is an AI-powered platform designed to assist job seekers in optimizing their resumes for Applicant Tracking Systems (ATS) and tailoring them for specific job descriptions. It also includes features for job searching and provides personalized job suggestions.

---

## Quick summary

* **What it does:** Scans resumes for ATS compatibility, pulls out and highlights ATS keywords, suggests tailored edits for job descriptions, and surfaces job suggestions.
* **Audience:** Students, freshers, and early-career devs who want their resumes to pass ATS and stand out to recruiters.
* **Why it helps:** Many resumes get filtered by ATS. CareerCraft AI helps you match the job description and improves keyword alignment.

---

## Tech stack

**HTML | CSS | Firebase | Python | Streamlit | SpaCy | NLTK | Pandas | Plotly**

---

## Features

* **ATS Scanner:** NLP-based scoring that checks your resume for ATS-friendly structure and keyword coverage.
* **Resume Tailoring:** Upload a job description and get targeted suggestions to add or rephrase content in your resume.
* **ATS Keyword Highlight:** Side-by-side view that highlights overlapping keywords between resume and JD.
* **Job Suggestions:** Basic job matching using keyword similarity and heuristics (link outs to external job sites).
* **User-friendly UI:** Built with Streamlit for fast iteration and easy local hosting.

---

## Repo structure (suggested)

```
careercraft-ai/
├─ backend/
│  ├─ services/
│  └─ ...
├─ frontend/
│  └─ assets/
├─ streamlit_app.py        # main Streamlit entry (or run main.py if present)
├─ main_page.py            # main UI components
├─ requirements.txt
├─ README.md
└─ assets/
```

---

## Installation (local)

1. Clone the repo:

```bash
git clone <REPO_URL>
cd careercraft-ai
```

2. Create a Python venv and activate it (optional but recommended):

```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows (powershell)
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables (Firebase etc.)

Create a `.env` file in the project root with at least:

```
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
# any other Firebase or app-specific keys
```

5. Run the app:

```bash
# if your entry is streamlit_app.py
streamlit run streamlit_app.py
# or if main.py is the entry
streamlit run main.py
```

Open the URL printed in your terminal (usually [http://localhost:8501](http://localhost:8501)).

---

## Usage guide

1. **Sign in** (if Firebase auth is configured).
2. **ATS Scanner:** Go to the ATS Scanner page → upload your resume (PDF or DOCX) → press `Analyze` → view score and recommendations.
3. **Resume Tailoring:** Paste the job description → `Tailor Resume` → see suggested bullet edits and keywords to add.
4. **Keyword View:** Compare resume vs JD — overlapping keywords are highlighted.
5. **Job Suggestions:** Use the job search feature (if enabled) to see tailored job links; follow the link to apply on the original site.

---

## Recommended file formats

* Resumes: PDF or DOCX
* Job Descriptions: PDF or DOCX

---

## Extending the app (developer notes)

* **Improve matching:** Plug in an embedding model + cosine similarity for better JD-resume matching.
* **Persistence:** Add a DB to save user profiles, resume history and tailored versions.
* **Analytics:** Track common missing skills and create personalized study plans.
* **CI/CD:** Deploy to Streamlit Cloud, Vercel (frontend) + Cloud Functions for heavy NLP tasks.

---



## Sample `requirements.txt` (starter)

```
streamlit
spacy
nltk
pandas
plotly
python-dotenv
firebase-admin
pdfminer.six
python-docx
```

will add these later

* Add embeddings-based semantic matching (better than keyword matching).
* Resume version history + export tailored resume as new PDF.
* Automated cover letter generator.
* CLI tool to bulk-tailor resumes for many JDs.

---








