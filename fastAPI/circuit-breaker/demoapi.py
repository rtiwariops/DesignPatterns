from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

@app.post("/data")
async def create_item(item: Item):
    return {"name": item.name, "description": item.description}

if __name__ == '__main__':
    uvicorn.run("demoapi:app", host="0.0.0.0", port=5001, reload=True, workers=2)