"""
Welcome to Youtube Autonomous API Module.

Please, take a look at this project to get inspiration:
https://github.com/htbrandao/fastemplate/blob/master/fastemplate/__init__.py
"""
from yta_api.dependencies import is_authorized_with_api_key
from yta_api.routers import audio
from yta_general_utils.programming.env import load_current_project_dotenv
from fastapi import FastAPI, Depends


load_current_project_dotenv()

app = FastAPI(dependencies = [
    Depends(is_authorized_with_api_key)
])
#app = FastAPI()

# Include routers here
app.include_router(audio.router)