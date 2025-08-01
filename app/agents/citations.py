import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def citations(text:str)->str:
    "Identifies key concepts in text and generates plausible academic citations."
    if not text:
        return "No text provided"
    system_prompt = "You are a helpful assistant that generates academic citations."
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("user", "Please generate academic citations for the following text:\n\n{text}".format(text=text)),
        ]   
    )
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.6)
    chain=llm | prompt | StrOutputParser()
    citations=chain.invoke({"text":text})
    return citations
    
