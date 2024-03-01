import os
import logging
import yaml
from typing import Dict, Union, List, Any

class BasicDBM:
  """Basic db class that does: 
    1) list available databases
    2) creates a new database
  """
  def __init__(self, root: str):
    """Initialize database manager 
    
    Args: 
        root (str): the root folder containing the database files
    """
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)
    self.root = root
    self.dbs = self._get_dbs()
    self.db = None
    
  def _get_dbs(self) -> Union[Dict[str, str], str]:
    self.logger.info("Getting databases ...")
    try:
      # key = name, value = abspath, only for yml files (db file format)
      kv = [(db.split("/")[-1].split(".yml")[0], db) for db in [os.path.abspath(os.path.join(self.root, apath)) for apath in os.listdir(self.root)] if db.endswith(".yml")]
      return {key: value for key, value in kv}
    except Exception as e:
      msg = f"Could not fetch database list due to error: {e}" ; self.logger.error(msg)
  
  def list_dbs(self) -> List[str]:
    """List all available databases (files)"""
    self._get_dbs()
    return list(self.dbs.keys())
  
  def create_db(self, name: str) -> str:
    """creates a database file"""
    self.logger.debug(f"name: {name}")
    self.logger.debug(f"list of dbs: {list(self.dbs.keys())}")
    if name in list(self.dbs.keys()):
      msg = f"Name {name} already exists, delete the db first or create a new one"
      self.logger.exception(msg) ; return msg
    else:
      filename = f"{os.path.join(self.root, name)}.yml"
      self.logger.debug(f"Creating db: {filename}")
      open(filename, "w").close() # create empty database file
      self.dbs[name] = os.path.abspath(filename)
      return f"Created an empty database named: {name}"
    
  def select_db(self, name: str) -> str:
    """Select a database"""
    if name not in list(self.dbs.keys()):
      msg = f"name {name} does not exist in the database repo {list(self.dbs.keys())}" 
      self.logger.exception(msg) ; return msg
    else: 
      self.db = BasicDB(db_name=name, db_path=self.dbs[name])
      return f"Selected database: {name}"
  
  def del_db(self, name: str) -> str:
    """Deletes a database"""
    if name not in list(self.dbs.keys()):
      msg = f"Could not find db: {name} in the list of databases {list(self.dbs.keys())}"
      self.logger.exception(msg) ; return msg
    else:
      try:
        os.remove(self.dbs[name]) ; del self.dbs[name] # remove the file and the key from the dictionary
        self.db = None if self.db != None and self.db.name == name else self.db # if self.db is the one being deleted, set it to None
        return f"db: {name}, successfully deleted"
      except Exception as e: 
        msg = f"Could not delete database, error: {e}"
        self.logger.error(msg) ; return msg

class BasicDB:
  """
  Basic database that allows you to do very very basic db manipulation
  """ 
  def __init__(self, db_name: str , db_path: str):
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    self.name = db_name
    self.db = db_path
    self.ids = []
    
  def _load_db_indexes(self) -> str:
    """loads the indexes"""
    with open(self.db, "r") as database:
      db_content = yaml.safe_load(database)
      self.logger.debug(db_content)
    self.ids = list(db_content.keys()) if db_content != None else []
         
  def populate(self, req: Dict[str, Any]):
    """populates the database with some content"""
    self._load_db_indexes()
    field = {
      len(self.ids) : req
    }
    try:
      content = yaml.dump(field) # convert from json to yml
    except Exception as e:
      msg = f"Could not fetch content due to error: {e}"
      self.logger.error(msg) ; return msg
    self.logger.debug(f"content: {content}")
    
    try:
      with open(self.db, "a") as database:
        database.write(content)
      return f"content successfully added to db: {self.name}"
    except Exception as e:
      msg = f"Could not write content to database due to error: {e}"
      self.logger.error(msg) ; return msg
  
  def view(self):
    """view the whole database"""
    with open(self.db, "r") as f:
      database = yaml.safe_load(f)
    return database
  
if __name__ == "__main__":
  import datetime ; import sys
  cwd = os.getcwd() ; r = os.path.join(cwd, "test")
  dbm = BasicDBM(r)
  dbs = dbm.list_dbs()
  print(dbs)
  dbm.select_db(name="db1")
  
  content ="Hi qbear"
  user = "kristian"
  x = {
    "metadata": {
      "time": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
      "size": sys.getsizeof(content)
    }, 
    "content": content,
    "role": user,
    "vector": None,
    "md5": None # TODO: implement MD5 algorithm
  }
  print(dbm.db.populate(req=x))
  y = dbm.db.view()
  [print(y[key]) for key in list(y.keys())]
  dbm.del_db("db1")
  
