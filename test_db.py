import asyncio
from app.config.database import Database
import logging

logging.basicConfig(level=logging.INFO)

async def test_connection():
    await Database.connect_to_database()
    await Database.close_database_connection()

if __name__ == "__main__":
    asyncio.run(test_connection())