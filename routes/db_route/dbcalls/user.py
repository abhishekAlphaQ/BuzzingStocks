from fastapi import APIRouter, Depends,  Body, HTTPException
from models.db_models.user import OutModel,buzzTableModel
from helpers.db_tasks import aiodynamo_crud as ac
from helpers.buzzing_tasks import buzzingMain as bz
# from core.settings.configs import DynamoDBSettings as s
import asyncio,json
from datetime import datetime
from helpers.pyobjid import PyObjectId
from aiohttp import ClientSession
from aiodynamo.client import Client
from aiodynamo.credentials import Credentials
from aiodynamo.expressions import F
from aiodynamo.http.aiohttp import AIOHTTP
from aiodynamo.models import BatchGetRequest

today = datetime.today()
routes = APIRouter()
BUZZ_TABLE="prod-buzzStock"
VIDHYA_TABLE="vidhya_AI"

@routes.get("/Get top 10 buzzing stock", response_model=OutModel)
async def getTop10BuzzingStock():
    try:
        data = await getLatestBuzzStocks()   
        out = OutModel(status="success",
                    status_code=200,
                    comment="Data retrieved successfully",
                    data= data)
        return out
    except Exception as e:
        out = OutModel(status="failed",
                       status_code=400,
                       comment="Data Fetched Failed",
                       data=e)
          
async def getVidhyaStocks():
    resp = await ac.aiodynamoScanHbd(table=VIDHYA_TABLE, exp=F("date").equals(today.strftime('%d %b %Y')))
    vid_ids = [item['id'] for item in resp]
    sorted_ids = (sorted(vid_ids,reverse=True))[:10]
    filtered_data =  [d for d in resp if d['id'] in sorted_ids]
    return [buzzTableModel(**d) for d in filtered_data]

async def getLatestBuzzStocks():
    vid_list = getVidhyaStocks()
    count = len(vid_list)
    if count >= 10:
        return vid_list
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(setBuzzStocks(10 - count))
        loop.close()

        resp = await ac.aiodynamoScan(table=BUZZ_TABLE, exp=F("date").equals(today.strftime('%d %b %Y')))
        buzz_ids = [item['buzzId'] for item in resp]
        sorted_ids = (sorted(buzz_ids,reverse=True))[:10]
        filtered_data =  [d for d in resp if d['buzzId'] in sorted_ids]
        return [buzzTableModel(**d) for d in filtered_data]
    
async def setBuzzStocks(count):
    bz_list = bz.getBuzzStocks(count)
    for z in bz_list:
        c = buzzTableModel(
            buzzId = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            date =  today.strftime('%d %b %Y'),
            duration = z[1],
            logo =  z[2],
            reason =  z[3],
            target =  '',
            ticker =  z[0],
            vidhyaId = ''
        )
        await ac.aiodynamoPut(table=  BUZZ_TABLE, pk={"buzzId": c.buzzId}, exp=c.dict())