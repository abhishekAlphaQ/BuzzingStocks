# STOCK_APPSYNC_API_ENDPOINT_URL=https://dggszxzqobefvhtmipn6zd6pqa.appsync-api.ap-south-1.amazonaws.com/graphql
# STOCK_APPSYNC_API_KEY=da2-ggytyqmyqrfybbm2zgj24bpx4y

import json

import aiohttp


class AppSync(object):
    def __init__(self, data):
        endpoint = data["endpoint"]
        self.APPSYNC_API_ENDPOINT_URL = endpoint
        self.api_key = data["api_key"]
        # self.session = aiohttp.ClientSession()

    async def graphql_operation(self, query, input_params):
      async with aiohttp.ClientSession() as session:
        response = await session.request(
            url=self.APPSYNC_API_ENDPOINT_URL,
            method='POST',
            headers={'x-api-key': self.api_key},
            json={'query': query, 'variables': {"input": input_params}}
        )
        # session.close()

        return await response.json()

async def fetchAppSyncGraphQL(apiUrl:str,apiKey:str,gqlQuery:str):
    APPSYNC_API_ENDPOINT_URL = apiUrl
    APPSYNC_API_KEY = apiKey
    init_params = {"endpoint": APPSYNC_API_ENDPOINT_URL,
                   "api_key": APPSYNC_API_KEY}
    app_sync = AppSync(init_params)

#     gqlBktQuery = """
#    query listPynamoBasketAPIS {
#   listPynamoBasketAPIS(filter: {advisorMode: {eq: true}, basketStatus: {eq: "PUBLISHED"}}) {
#     items {
#       basketId
#       userId
#     }
#   }
# }
#     """

#     gqlStkQuery = """query listPynamoStocks{listPynamoStocks {items {id basketId userId entryTxnId exitTxnId ticker}}}"""

    input_params = {}

    response = await app_sync.graphql_operation(gqlQuery, input_params)
    # print(json.dumps(response, indent=3)) 
    # resp = json.dumps(response)
    return response