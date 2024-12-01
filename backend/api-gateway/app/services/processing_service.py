import httpx
import os

PORT = int(os.getenv("PORT", 8000))

class QuestProcessingService:
    BASE_URL = f"http://quest-processing-service:{PORT}"    

    async def process_daily_login(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/user-quests/daily-login",
                json={"user_id": user_id}
            )
        return response.json() if response.status_code == 200 else None

    async def sign_in_three_times(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/user-quests/sign-in-three-times",
                json={"user_id": user_id}
            )
        return response.json() if response.status_code == 200 else None

    async def create_user_quest(self, user_id: int, quest_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/user-quests/",
                json={"user_id": user_id, "quest_id": quest_id}
            )
        return response.json() if response.status_code == 200 else None

    async def update_user_quest(self, user_id: int, quest_id: int, progress: int):
        async with httpx.AsyncClient() as client:
            """Call the /user-quests/{user_id}/{quest_id} endpoint to update progress."""
            response = await client.put(
                f"{self.BASE_URL}/user-quests/{user_id}/{quest_id}",
                json={"progress": progress}
            )
        return response.json() if response.status_code == 200 else None
