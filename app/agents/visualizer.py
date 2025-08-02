import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def create_diagram_from_text(text:str)->str:
    "genrate flowchart, graphs from the text of the Research paper"
    if not text:
        return "No text provided"
    system_prompt = "You are a helpful assistant that generates flowcharts and graphs from text."
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("user", "Please generate flowcharts and graphs from the following text:\n\n{text}".format(text=text)),
        ]   
    )
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
    chain=llm | prompt | StrOutputParser()
    dotcode=chain.invoke({"text":text})
    if "```dot" in dot_code:
        dot_code = dot_code.split("```dot")[1].split("```")[0]
    elif "```" in dot_code:
        dot_code = dot_code.split("```")[1].split("```")[0]
    return dotcode