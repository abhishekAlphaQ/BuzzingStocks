from fastapi import FastAPI
from routes.db_route.dbcalls import user
from models.db_models.user import buzzTableModel
from helpers.db_tasks import aiodynamo_crud as ac
# from core.settings.configs import DynamoDBSettings as s
import asyncio
from datetime import datetime
from aiodynamo.expressions import F

today = datetime.today()
app = FastAPI()
BUZZ_TABLE="prod-buzzStock"
VIDHYA_TABLE="vidhya_AI"


app.include_router(user.routes)

async def getVidhyaStocks():
    resp = await ac.aiodynamoScanHbd(table=VIDHYA_TABLE, exp=F("date").equals(today.strftime('%d %b %Y')))
    vid_ids = [item['id'] for item in resp]
    sorted_ids = (sorted(vid_ids,reverse=True))[:10]
    filtered_data =  [d for d in resp if d['id'] in sorted_ids]
    return [buzzTableModel(**d) for d in filtered_data]

asyncio.run(getVidhyaStocks())