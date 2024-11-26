import httpx

class QuestCatalogService:
    BASE_URL = "http://quest_catalog_service:8000/catalog"

    async def list_quests(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/quests/")
        return response.json() if response.status_code == 200 else None
      
    async def get_quest(self, quest_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/quests/{quest_id}")
        return response.json() if response.status_code == 200 else None

    async def create_quest(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/quests/", json=data)
        return response.json() if response.status_code == 200 else None

    async def update_quest(self, quest_id: int, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{self.BASE_URL}/quests/{quest_id}", json=data)
        return response.json() if response.status_code == 200 else None

    async def delete_quest(self, quest_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.BASE_URL}/quests/{quest_id}")
        return response.json() if response.status_code == 200 else None
      
    async def list_rewards(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/rewards/")
        return response.json() if response.status_code == 200 else None

    async def get_reward(self, reward_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/rewards/{reward_id}")
        return response.json() if response.status_code == 200 else None

    async def create_reward(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/rewards/", json=data)
        return response.json() if response.status_code == 200 else None

    async def delete_reward(self, reward_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.BASE_URL}/rewards/{reward_id}")
        return response.json() if response.status_code == 200 else None

    async def track_user_quest_rewards(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/user_quest_rewards/", json=data)
        return response.json() if response.status_code == 200 else None

    async def get_user_quest_rewards(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/user_quest_rewards/{user_id}")
        return response.json() if response.status_code == 200 else None