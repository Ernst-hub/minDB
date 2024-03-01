import os
import logging
from fastapi import FastAPI

from minDB.api.controller import Controller
from minDB.db.basic_db import BasicDBM



logging.basicConfig(level=logging.DEBUG)
cwd = os.getcwd()
datafolder = "databases"
root = os.path.join(cwd, datafolder)

app = FastAPI()
controller = Controller()
controller.dbm = BasicDBM(root)
app.include_router(controller.router)

    
