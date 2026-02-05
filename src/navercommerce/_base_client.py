from httpx import Client, AsyncClient



class BaseClient:
    def __init__(self, client: Client | AsyncClient):
        self.client = client

    def request(self, method: str, url: str, **kwargs):
        
        return self.client.request(method, url, **kwargs)

    def get(self, url: str, **kwargs):
        return self.client.get(url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.client.post(url, **kwargs)



class BaseAsyncClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def request(self, method: str, url: str, **kwargs):
        return await self.client.request(method, url, **kwargs)

    async def get(self, url: str, **kwargs):
        return await self.client.get(url, **kwargs)

    async def post(self, url: str, **kwargs):
        return await self.client.post(url, **kwargs)