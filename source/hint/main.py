# Import Union since our Item object will have tags that can be strings or a list.
from typing import Union 

from fastapi import FastAPI
# BaseModel from Pydantic is used to define data objects.
#pydantic atua na checagem dos tipos de dados passados e recebidos
from pydantic import BaseModel

# Declare the data object with its components and their type.
#sempre q vamos enviar alguma coisa pra o servidor temos q criar uma classe pra receber
class TaggedItem(BaseModel):
    name: str
    tags: Union[str, list] 
    item_id: int

app = FastAPI()

# This allows sending of data (our TaggedItem) via POST to the API.
#funcao assincrona
@app.post("/items/")
async def create_item(item: TaggedItem):
    return item