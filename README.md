# AI Research Assistant 🤖

An advanced, LLM-powered agent designed to deconstruct and simplify complex academic research papers. This tool takes a PDF as input, generates a clean, structured booklet with summaries and citations, and provides an interactive chat interface for Q\&A.

This project was developed for the Intra IIT Tech Meet at IIT Bhilai.

-----

## Features ✨

  * **Intelligent Document Parsing:** Uses `unstructured` to parse PDFs, extracting text, tables, and images.
  * **Automated Booklet Generation:** Creates a professional, multi-page PDF booklet containing:
      * A concise, AI-generated summary of the paper.
      * A list of generated citations for key concepts.
      * Extracted tables and image captions.
  * **Stateful Agentic Workflow:** Built with LangGraph, using a supervisor architecture to robustly manage the processing pipeline, chat interactions, and error handling.
  * **Interactive RAG Chat:** After processing, a chat interface is enabled, allowing users to ask specific questions about the paper's content.
  * **Modular & Asynchronous Backend:** Built with FastAPI to handle requests efficiently, offloading heavy processing to background tasks.

-----

## Architecture Overview

The application uses a state-machine architecture managed by a LangGraph "supervisor." This ensures a clear separation between the document processing pipeline and the interactive chat loop, providing a smooth and predictable user experience.

    graph TD
    subgraph "Phase 1: Document Processing Pipeline"
        A[User uploads PDF via UI/API] --> B{FastAPI Endpoint: /process_document};
        B -- Triggers --> C{LangGraph Workflow};
        C --> D(1. Parse Document);
        D --> E(2. Index Content for RAG);
        E --> F(3. Summarize Paper);
        F --> G(4. Generate Citations);
        G --> H(5. Compile PDF Booklet);
        H --> I((State Updated: Chat Ready ✅));
        end

    subgraph "Phase 2: Interactive Chat Loop"
        J[User asks question via UI/API] --> K{FastAPI Endpoint: /chat};
        K -- Uses RAG Index from E --> L[RAG Chain Retrieves Context];
        L --> M[LLM Generates Answer];
        M --> N((Response Sent to User));
    end

-----

## Tech Stack 🛠️

  * **Backend:** FastAPI
  * **AI Orchestration:** LangGraph
  * **LLM Interaction:** LangChain, Google Gemini
  * **Document Parsing:** `unstructured`
  * **Vector Database:** ChromaDB
  * **Embeddings:** HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
  * **PDF Compilation:** WIP

-----

## Setup and Installation ⚙️

Follow these steps to set up and run the project locally.

### 1\. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2\. Create a Virtual Environment

```bash
# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Install System Dependencies

This project requires two key system-level dependencies:

  * **Poppler (for `unstructured`):**
      * **macOS:** `brew install poppler`
      * **Debian/Ubuntu:** `sudo apt-get install poppler-utils`
  * **LaTeX (for PDF compilation):**
      * **macOS:** [MacTeX](https://www.tug.org/mactex/)
      * **Windows:** [MiKTeX](https://miktex.org/)
      * **Debian/Ubuntu:** `sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra`

### 4\. Install Python Packages

Create a `requirements.txt` file with the content below and install it.

```
Got to requirements.txt file and copy paste
```

```bash
pip install -r requirements.txt
```

### 5\. Set Up Environment Variables

Create a file named `.env` in the project root directory and add your Google API key.

```
# .env
GOOGLE_API_KEY="your_google_api_key_here"
```

-----

## How to Use 🚀

1.  **Start the Backend Server:**
    Run the following command from the project's root directory:

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

2.  **Access the Interactive API Docs:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs`.

3.  **Process a Document:**

      * Expand the `/process_document` endpoint.
      * Click "Try it out" and upload a PDF file.
      * Execute the request. You will receive a `job_id`.

4.  **Check Status & Get Booklet:**

      * Expand the `/status/{job_id}` endpoint.
      * Enter the `job_id` from the previous step and execute.
      * Once the `current_mode` shows `"chatting"`, a `booklet_url` will be available to download the generated PDF.

5.  **Chat with the Document:**

      * Expand the `/chat` endpoint.
      * Enter the same `job_id` and your question in the request body.
      * Execute to receive an AI-generated answer based on the document's content.

-----

## Project Structure

```
/project_root
├── app/
│   ├── agents/
│   │   ├── summarizer.py
│   │   └── citation_generator.py
│   ├── graphs/
│   │   ├── supervisor.py
│   │   ├── processing_nodes.py
│   │   ├── chat_nodes.py
│   │   └── error_nodes.py
│   ├── utils/
│   │   ├── parser.py
│   │   └── pdf_compiler.py
│   ├── schemas.py
│   └── main.py
├── outputs/        # Generated booklets and images will appear here
├── templates/
│   └── booklet_template_v2.tex
├── .env
└── requirements.txt
```
