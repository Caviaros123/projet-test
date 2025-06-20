from fastapi import FastAPI
from pertimm_client import runApp

app = FastAPI()

@app.get("/start")
async def start_endpoint():
    result = await runApp()
    return result