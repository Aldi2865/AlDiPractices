from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def f1():
    return {"Hello, World!"}

@app.get("/user")
def f2():
    return {"name": "John", "age": 30, "city": "New York"}

@app.get("/user/{user_id}")
def f3(user_id: int):
    return {"user_id": user_id, "name": "Vasya", "age": 100, "city": "Kyiv"}

@app.get("/user/{user_id}/items/{item_id}")
def f4(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id, "name": "Vasya", "age": 100, "city": "Kyiv"}