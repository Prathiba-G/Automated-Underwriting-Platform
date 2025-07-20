from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from routers import document_parser, vision_analyzer, risk_assessor
import uvicorn

app = FastAPI(
    title="Automated Underwriting API",
    description="AI-powered property risk assessment engine",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document_parser.router, prefix="/documents", tags=["Document Analysis"])
app.include_router(vision_analyzer.router, prefix="/images", tags=["Computer Vision"])
app.include_router(risk_assessor.router, prefix="/risk", tags=["Risk Assessment"])

@app.get("/")
def read_root():
    return {"message": "Automated Underwriting API is running 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

