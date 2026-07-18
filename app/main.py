from fastapi import FastAPI
from app.database import models

# Import all routers
from app.api.user import router as user_router
from app.api.resume import router as resume_router
from app.api.resume_version import router as resume_version_router
from app.api.resume_analysis import router as resume_analysis_router
from app.api.job import router as job_router
from app.api.compatibility_report import router as compatibility_report_router
from app.api.cover_letter import router as cover_letter_router
from app.api.application import router as application_router

app = FastAPI(title="career copilotAPI")

# Register routers
app.include_router(user_router)
app.include_router(resume_router)
app.include_router(resume_version_router)
app.include_router(resume_analysis_router)
app.include_router(job_router)
app.include_router(compatibility_report_router)
app.include_router(cover_letter_router)
app.include_router(application_router)

@app.get("/")
def home():
    return {
        "message": "Career Copilot Backend Running "
    }
