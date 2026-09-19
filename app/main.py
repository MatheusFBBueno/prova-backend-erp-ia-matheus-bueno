from fastapi import FastAPI
import asyncio
from app.core.service_caller import ServiceCaller


app = FastAPI()



@app.get('/question3')
async def call_services():
    
    gatherer = ServiceCaller()
    return await gatherer.call_and_wait_services()

