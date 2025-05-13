from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
import pytest
import asyncpg

app = FastAPI()

@pytest.mark.asyncio
async def test_db_connection():
    try:
        conn = await asyncpg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            port="5432"
        )
        await conn.close()
        assert True
    except Exception as e:
        print(f"Database connection error: {e}")
        assert False
