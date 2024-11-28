import httpx
import logging

logger = logging.getLogger(__name__)

class UserAuthService:
    BASE_URL = "http://user_auth_service:8000/user"

    async def signup(self, user_data: dict):
      try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/signup", json=user_data)
            logger.debug(f"Request sent to {self.BASE_URL}/signup with data: {user_data}")
            logger.debug(f"Response: {response.status_code}, {response.text}")
            return response.json() if response.status_code == 200 else None
      except httpx.RequestError as e:
        logger.error(f"HTTPX Request Error: {e}")
        raise

    async def login(self, user_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/login", json=user_data)
        return response.json() if response.status_code == 200 else None
