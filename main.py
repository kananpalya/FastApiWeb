from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from models import User, Task
from uuid import uuid4
from datetime import datetime
from typing import List
import asyncio
from scraper import scrape_walmart_product

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['scraper_db']
users_collection = db['users']
tasks_collection = db['tasks']
products_collection = db['products']

@app.post("/users/", response_model=User)
async def create_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    user_dict = user.model_dump()
    users_collection.insert_one(user_dict)
    return user

@app.get("/users/")
async def get_all_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return users

@app.post("/scrape/")
async def initiate_scrape(url: str, user_id: str):
    if not users_collection.find_one({"email": user_id}):
        raise HTTPException(status_code=404, detail="User not found")

    task_id = str(uuid4())
    task = {
        "task_id": task_id,
        "user_id": user_id,
        "url": url,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    tasks_collection.insert_one(task)

    async def run_scraper():
        try:
            product = await asyncio.to_thread(scrape_walmart_product, url)
            if product:
                tasks_collection.update_one(
                    {'task_id': task_id},
                    {'$set': {'status': 'success',
                              'product_id': product.get('product_id'),
                              'result': product,
                              'updated_at': datetime.utcnow()}}
                )
            else:
                tasks_collection.update_one(
                    {'task_id': task_id},
                    {'$set': {'status': 'failed',
                              'result': 'Scraping returned no data',
                              'updated_at': datetime.utcnow()}}
                )
        except Exception as e:
            tasks_collection.update_one(
                {'task_id': task_id},
                {'$set': {'status': 'failed', 'result': str(e), 'updated_at': datetime.utcnow()}}
            )
    asyncio.create_task(run_scraper())
    return {"task_id": task_id, "status": "pending"}

@app.get("/tasks/", response_model=List[Task])
async def list_tasks(user_id: str):
    if not users_collection.find_one({"email": user_id}):
        raise HTTPException(status_code=404, detail="User not found")
    tasks = list(tasks_collection.find({"user_id": user_id}, {'_id': 0}))
    return [Task.model_validate(task) for task in tasks]
