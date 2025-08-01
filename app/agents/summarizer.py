from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def summarize_text(text:str)->str:
    "Generate summary of the text"
    if not text:
        return "No text provided"
    system_prompt = "You are a helpful assistant that summarizes text."
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("user", "Please summarize the following text:\n\n{text}".format(text=text)),
        ]   
    )
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
    chain=llm | prompt | StrOutputParser()
    summary=chain.invoke({"text":text})
    return summary
    
    pass


