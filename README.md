# Smart-task-analyzer

# Smart Task Analyzer

A simple Django + DRF project that scores and prioritizes tasks using a configurable heuristic. It accepts task lists (JSON), calculates a priority score for each task, detects circular dependencies, and returns sorted results. The repository contains the backend (Django), frontend (HTML/CSS/JS), unit tests, and setup instructions.

---

## Setup Instructions

1. **Clone repository**
  
  git clone <your-repo-url>
  
  cd task-analyzer
  
2. Create and activate virtual environment

python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1

3. Install dependencies pip install -r requirements.txt

4. Run migrations python manage.py migrate

5. Run tests (optional but recommended) python manage.py test

6. Run the development server python manage.py runserver
 
7. Open the frontend Navigate to http://127.0.0.1:8000/ and paste a JSON array of tasks into the input area, or call the API endpoints directly.




