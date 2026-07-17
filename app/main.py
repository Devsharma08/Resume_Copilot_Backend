from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.resume import router as resume_router

app = FastAPI(title="career copilotAPI")

# Register user router
app.include_router(user_router)
# add the router to main app
app.include_router(resume_router)



@app.get("/")
def home():
	return {
		"message":"Career Copilot Backend Running "
	}

