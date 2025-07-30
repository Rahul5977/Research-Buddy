# fastapi app
from fastapi import FastAPI,UploadFile,File
from dotenv import load_dotenv
load_dotenv()

app=FastAPI(title="Research Buddy")

@app.get("/")
def read_root():
    return {"message":"Welcome to AI research assistant"}

# endpoint for uploading files
@app.post("/porcess-documents")
async def process_document(file:UploadFile=File(...)):
    return {"filename":file.filename,"content-type":file.content_type}
    