from fastapi import FastAPI
import solara.server.fastapi
from dotenv import load_dotenv

from .api import data_router

# Load environment variables
load_dotenv()

# Initialize FastAPI-Solara server
app = FastAPI()

# Mount the router
app.include_router(data_router, prefix="/api")

# Mount the Solara server
app.mount("/", app=solara.server.fastapi.app)
