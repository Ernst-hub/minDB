from fastapi import APIRouter, Query
from typing import Optional, Dict, Any, List
import logging

from minDB.db.basic_db import BasicDBM
from minDB.api.util.decorator import ensure_dbm_initialized_async, ensure_db_selected_async

class Controller(object):
  """FastAPI controller for the minDB database manager
  
  Methods:
    list_dbs: list all databases
    create_db: create a new database
    select_db: select a database
    delete_db: delete a database
    populate_db: populate a database
    view_db: view a database  
  """
  
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.INFO)
    self.dbm: Optional[BasicDBM] = None
    
    self.router = APIRouter()
    self.router.add_api_route("/dbm/list_dbs", self.list_dbs, methods=["GET"])
    self.router.add_api_route("/dbm/create_db", self.create_db, methods=["POST"])
    self.router.add_api_route("/dbm/select_db", self.select_db, methods=["POST"])
    self.router.add_api_route("/dbm/del_db", self.delete_db, methods=["DELETE"])
    self.router.add_api_route("/dbm/db/populate", self.populate_db, methods=["POST"])
    self.router.add_api_route("/dbm/db/view", self.view_db, methods=["GET"]) 
     
  @ensure_dbm_initialized_async
  async def list_dbs(self) -> List[str]:
    self.logger.info("listing db ...")
    return self.dbm.list_dbs()
  
  @ensure_dbm_initialized_async
  async def create_db(self, name: str):
    self.logger.info("creating db ...")
    self.logger.info(f"db name: {name}")
    return self.dbm.create_db(name)
  
  @ensure_dbm_initialized_async
  async def select_db(self, name):
    self.logger.info("selecting database ...")
    return self.dbm.select_db(name)
  
  @ensure_dbm_initialized_async
  async def delete_db(self, name):
    self.logger.info("deleting database ...")
    return self.dbm.del_db(name)
  
  @ensure_db_selected_async
  async def populate_db(self, req: Dict[str, Any]):
    self.logger.info("populating index ...")
    return self.dbm.db.populate(req)
  
  @ensure_db_selected_async
  async def view_db(self):
    self.logger.info("viewing db ...")
    return self.dbm.db.view()
