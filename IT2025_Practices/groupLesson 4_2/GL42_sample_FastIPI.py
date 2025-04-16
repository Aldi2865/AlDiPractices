from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def my_function():
    return {"Hello, World!"}

@app.get("/user")
def my_function():
    return {"name": "John", "age": 30, "city": "New York"}


my_list = [269, 270, 271, 272, 273]

@app.get("/id")
def get_ids():
    return {"ids": my_list}

@app.get("/id/{id}")
def get_user_by_id(id: int):
    if id < 0 or id >= len(my_list):
        return {"error": "Index out of range"}
    else:
        return {"id": id, 
                "counts": my_list[id],
                "square": my_list[id]**2,
                "cube": my_list[id]**3,}