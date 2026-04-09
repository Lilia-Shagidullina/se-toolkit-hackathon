import uvicorn
from src.app.settings import Settings

settings = Settings()

app = __import__("src.app.main", fromlist=["app"]).app

if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
