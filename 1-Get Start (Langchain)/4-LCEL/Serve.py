from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers  import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

grog_key = os.getenv("GROG_API_KEY")
grog_key

model = ChatGroq(model="gemma2-9b-it", api_key=grog_key)
model

from langserve import add_routes


system_template =  "translate sentence into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), 
     ("user","{text}")
     ]
    )

parser = StrOutputParser()

chain = prompt_template|model|parser

#route
app  =  FastAPI(title="langchain Server",
                version="1.0",
                description="it is first langchain api serve")
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1',port=8000)