from fastapi import FastAPI
import os
import json

website = os.environ.get("WEBSITE", None)
app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

if not website :
    raise ValueError("Environemnt website must be specific.")

data_path = os.path.join(current_dir, "data", website + ".json")
f = open(data_path, 'r')
data = json.load(f)

@app.get("/api/items")
async def items():
    return data
