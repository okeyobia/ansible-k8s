from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Simple FastAPI App",
    description="A simple FastAPI application",
    version="0.1.0",
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello, World!"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    """Read an item by ID"""
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
