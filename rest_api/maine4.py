from fastapi import FastAPI

app = FastAPI()

# Правильний формат словника
tasks = {"a": "add", "b": "in", "d": "ist", "f": "foot"}

@app.get('/append/{task}/{task1}')
async def n(task: str, task1: str):
    # Додаємо новий елемент до словника
    tasks[task] = task1
    return { 'tasks': tasks}
@app.get('/update/{tas}/{tas1}')
async def b(tas: str, tas1: str):
    tasks.update({tas:tas1})
    return { 'tasks': tasks}

@app.get('/delete/{ta}')
async def d(ta: str):
    tasks.del[ta]
    return { 'tasks': tasks}

