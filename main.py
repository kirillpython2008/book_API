from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from routers import router
from config import Config
from middlewares import middleware

config = Config(host="127.0.0.1", port=8000)

app = FastAPI()
app.middleware("http")(middleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:63342"])
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(prefix="/book", router=router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
