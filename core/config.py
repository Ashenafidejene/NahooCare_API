from dotenv import load_dotenv
import os

load_dotenv()

load_dotenv(dotenv_path=".env")  # Explicitly specify the .env file path

class Settings:
    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING")
    #MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    #JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    OPENAI_API_KEY : str = os.getenv("OPENAI_API_KEY")
settings = Settings()