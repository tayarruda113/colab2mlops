from fastapi import FastAPI

# Instantiate the app.
app = FastAPI()

# Define a GET on the specified endpoint.
#rota principal é no /
@app.get("/")
async def say_hello():
    return {"greeting": "Hello World!"}

# A GET that in this case just returns the item_id we pass, 
#parametro da rota é o item_id
@app.get("/items/{item_id}")
#sugerido que item_id seja tipo inteiro, ele sempre vai tentar forçar pra esse tipo 
async def get_items(item_id: int, count: int = 1):
    return {"fetch": f"Fetched {count} of {item_id}"}