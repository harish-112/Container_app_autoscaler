#i created a simple FastAPI application to containerize and run it inside azure container app

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
