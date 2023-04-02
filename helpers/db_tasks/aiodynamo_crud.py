from aiohttp import ClientSession
from aiodynamo.client import Client
from aiodynamo.credentials import Credentials
from aiodynamo.http.aiohttp import AIOHTTP


async def aiodynamoQuery(table,exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        # result =  await client.query(table,exp)
        result = [item async for item in client.query(table,exp)]
        return result
# async def create_user, get_user, get_users, delete_user, update_user


async def aiodynamoGet(table, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        result =  await client.get_item(table,key=exp)
        return result

async def aiodynamoCount(table, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        result = await client.scan_count(table, filter_expression=exp)
        return result

async def aiodynamoScan(table, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        result = [item async for item in client.scan(table, filter_expression=exp)]
        return result

async def aiodynamoScanAll(table):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        table = client.table(table)
        result = [item async for item in table.scan()]
        return result

async def aiodynamoUpdateItem(table,pk:dict, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        # result = [item async for item in client.scan(table, filter_expression = exp)]
        table = client.table(table)
        result = await table.update_item(pk, exp)
        return result
        
async def aiodynamoPut(table, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        # result = [item async for item in client.scan(table, filter_expression=exp)]
        table = client.table(table)
        await table.put_item(exp)

        # result = await table.get_item(pk)
        # return result

async def aiodynamoDelete(table, exp):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), "ap-south-1")
        # result = [item async for item in client.scan(table, filter_expression=exp)]
        result = await client.delete_item(table,key=exp)
        return result

async def aiodynamoBatchGetItem(request, region):
    async with ClientSession() as session:
        client = Client(AIOHTTP(session), Credentials.auto(), region)
        # result = [item async for item in client.scan(table, filter_expression=exp)]
        result = await client.batch_get(request)
        return result.items