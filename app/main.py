import uvicorn
from fastapi import FastAPI
from routers import transactions

app = FastAPI(
    title="Financial Analyzer APIs",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.include_router(transactions.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Successful Connection"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)