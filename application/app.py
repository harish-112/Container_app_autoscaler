#i created a simple FastAPI application to containerize and run it inside azure container app

import time

from fastapi import FastAPI
import uvicorn
import random

app = FastAPI()

@app.get("/site-safety")
def check_safety():
    conditions = ["Clear Skies - Safe to Work", "Heavy Rain - Stop Outdoor Work", "High Winds - Stand Down Cranes"]
    current_status = random.choice(conditions)
    return {
        "company": "KYRO AI Operations",
        "site_status": current_status,
        "monitoring": "Active"
    }
@app.get("/stress")
def stress(seconds: int = 60):
    end = time.time() + seconds

    while time.time() < end:
        x = 0
        for i in range(100000):
            x += i * i

    return {"message": "Stress complete"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
