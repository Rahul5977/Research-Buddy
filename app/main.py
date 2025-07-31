# fastapi app
from fastapi import FastAPI,UploadFile,File,BackgroundTasks
from dotenv import load_dotenv
from .utils import file_handler
import os
import time
load_dotenv()

app=FastAPI(title="Research Buddy")

def simulate_ai_response(email:str,file_path:str):
    "a dummy function that simulates an AI response"
    print(f"starting AI response for {email} with file {file_path}")
    time.sleep(10)
    print(f"Processing complete! Sending results to {email}.")

@app.get("/")
def read_root():
    return {"message":"Welcome to AI research assistant"}

# endpoint for uploading files
@app.post("/porcess-documents")
async def process_document(file:UploadFile=File(...)):
    # defines path to save file
    save_path = f"output/{file.filename}"
    os.makedirs("output",exist_ok=True)
    # saves file
    file_handler.save_file(file,save_path)
    
    # Running background task
    background_tasks = BackgroundTasks()
    background_tasks.add_task(simulate_ai_response,"user@example.com",file.filename,save_path)
    
    return {"message": "File upload successful. Processing has started in the background."}
    