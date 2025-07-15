from starlette.config import Config

config = Config(".env")
class Settings:
    SECRET_KEY = config("SECRET_KEY", cast=str, default="secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    DATABASE_URL = config("DATABASE_URL", cast=str)
    FRONTEND_URL = config("FRONTEND_URL", cast=str)

settings = Settings()