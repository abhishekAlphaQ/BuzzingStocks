from fastapi import APIRouter, Depends,  Body, HTTPException
from models.db_models.user import OutModel,saveBookmark
from helpers.db_tasks import aiodynamo_crud as ac
import asyncio,json
from helpers.pyobjid import PyObjectId
from aiohttp import ClientSession
from aiodynamo.client import Client
from aiodynamo.credentials import Credentials
from aiodynamo.expressions import F
from aiodynamo.http.aiohttp import AIOHTTP
from aiodynamo.models import BatchGetRequest

table_name="pynamo-buzzStock"
routes = APIRouter()

@routes.get("/Get top 10 buzzing stock", response_model=OutModel)
def getTop10BuzzingStock():
    try:
        get10Data()       
    except Exception as e:
        out = OutModel(status="failed",
                       status_code=400,
                       comment="Data Fetched Failed",
                       data=e)
        
def get10Data():
    data = ac.aiodynamoScanAll(table_name)
    if data:
        out = OutModel(status="success",
                    status_code=200,
                    comment="Data retrieved successfully",
                    data=data[:10])
        return out
    
def getVidhyaStocks():
    data = ac.aiodynamoScanAll(table_name)

def getLatestBuzzStocks():
    data = ac.aiodynamoScanAll(table_name)

def saveLatestBuzz():
    data = ac.aiodynamoScanAll(table_name)

def fetchTopBuzzForUI():
    data = ac.aiodynamoScanAll(table_name)