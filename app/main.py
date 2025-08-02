# fastapi app
from fastapi import FastAPI,UploadFile,File,BackgroundTasks,HTTPException,Request
from dotenv import load_dotenv
from .utils import file_handler
from . import schemas
import os
import time
import uuid
from .graphs.supervisor import app as research_assistant_app
load_dotenv()

app=FastAPI(title="Research Buddy")
app.mount("/output",FastAPI.static_files("output"),name="output")
SESSION={}

def simulate_ai_response(email:str,file_path:str):
    "a dummy function that simulates an AI response"
    print(f"starting AI response for {email} with file {file_path}")
    time.sleep(10)
    print(f"Processing complete! Sending results to {email}.")

def invoke_graph(job_id:str):
    pass
@app.get("/")
def read_root():
    return {"message":"Welcome to AI research assistant"}

# endpoint for uploading files
@app.post("/porcess-documents")
async def process_document(background_tasks: BackgroundTasks,file:UploadFile):
    job_id=str(uuid.uuid4())
    # defines path to save file
    save_path = f"output/{job_id}"
    os.makedirs("output",exist_ok=True)
    file_path=os.path.join(save_path,file.filename)
    # saves file
    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())
    
    SESSION[job_id]={
        "job_id":job_id,
        "file_path":file_path
    }
    # Running background task
    background_tasks.add_task(invoke_graph,job_id)
    
    return {"message":"Document processing started successfully","job_id":job_id}
    
@app.get("/status/{job_id}")
async def get_status(job_id:str,request:Request):
    session=SESSION.get(job_id)
    if not session:
        raise HTTPException(status_code=404,detail="Job not found")
    booklet_url=None
    if session.get("booklet_path"):
        # Construct a full URL for the client
        booklet_url = str(request.base_url) + session.get("booklet_path")
    return {
        "job_id":session.get("job_id"),
        "current_mode":session.get("current_mode"),
        "summary":session.get("summary"),
        "citations":session.get("citations"),
        "dot_code":session.get("dot_code"),
        "booklet_url":booklet_url,
        "error_message":session.get("error_message")
    }

@app.post("/chat")
async def chat(request:schemas.ChatQuery):
    job_id = request.job_id
    session = SESSION.get(job_id)

    if not session or session.get("current_mode") != "chatting":
        raise HTTPException(status_code=400, detail="Document not ready for chat or job not found.")

    session["user_query"] = request.query

    # Invoke the graph again, this time for a chat response
    updated_session = research_assistant_app.invoke(session)
    SESSION[job_id] = updated_session

    return {"answer": updated_session.get("chatbot_response")}
