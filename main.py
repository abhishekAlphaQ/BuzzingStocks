from fastapi import FastAPI
from routes.db_route.dbcalls import user
from helpers.pyobjid import PyObjectId
from helpers.db_tasks import aiodynamo_crud as ac
from models.db_models.user import saveBookmark
import asyncio,json
from routes.db_route.dbcalls import user as u

app = FastAPI()

app.include_router(user.routes)