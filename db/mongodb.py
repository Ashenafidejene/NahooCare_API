from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

try:
    client = AsyncIOMotorClient(
        settings.MONGO_CONNECTION_STRING,
        tls=True,
        tlsAllowInvalidCertificates=True  # If SSL certificates are causing issues
    )
    database = client["SBNHCRSWFAA"]
    print("✅ MongoDB client created successfully!")
except Exception as e:
    print(f"❌ Error creating MongoDB client: {e}")

async def check_database_connection():
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False
