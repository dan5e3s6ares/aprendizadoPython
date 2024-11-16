from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from prompts import Smart
from schemas import BasicLearn

app = FastAPI(allow_origins=["*"])

env = Environment(loader=FileSystemLoader("templates"))

smart = Smart()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def question(payload: BasicLearn):
    response = smart.reply(payload.text)
    if "This statement is true." in response:
        if "formal" in response or "Formal" in response:
            smart.learn(payload.text)
    return response


@app.get("/chat")
async def chat():
    template = env.get_template("chat.html")
    return HTMLResponse(template.render())


@app.get("/learned")
async def learned():
    return {"learned": smart.search_user_statements()}
