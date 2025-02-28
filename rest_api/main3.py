from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_calculator(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calculate")
async def calculate(operation: str, num1: float, num2: float):
    result = None
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 != 0:
            result = num1 / num2
        else:
            return {"error": "Ділення на нуль неможливе"}

    return {"result": result}

