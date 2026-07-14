from fastapi import FastAPI

app = FastAPI(title="career copilotAPI")
app.get("/")
def home():
	return (
"message":"Career Copilot Backend Running "
)

