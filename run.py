import uvicorn
from src.config.config import settings


if __name__ == "__main__":
    uvicorn.run("src.main:app", 
                host=settings.HOST, 
                port=settings.PORT, 
                reload=settings.RELOAD)