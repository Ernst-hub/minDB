from functools import wraps

def ensure_dbm_initialized_async(func):
  @wraps(func)
  async def wrapper(self, *args, **kwargs):
    assert self.dbm is not None, "DBM has not been initialized"
    return await func(self, *args, **kwargs)
  return wrapper

def ensure_db_selected_async(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
      assert self.dbm is not None, "DBM has not been initialized"
      assert self.dbm.db is not None, "No database has been selected"
      return await func(self, *args, **kwargs)
    return wrapper

